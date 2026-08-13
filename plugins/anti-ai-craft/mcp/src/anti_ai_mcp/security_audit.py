from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .evidence import (
    CheckError,
    CheckResult,
    CheckStatus,
    Confidence,
    Evidence,
    EvidenceKind,
    Finding,
    Severity,
)
from .git import DiffMode, GitAddedLine, GitInspector, GitRemovedLine
from .paths import resolve_within_repository


MAX_SECURITY_SOURCE_BYTES = 256 * 1024
MAX_SECURITY_SOURCE_FILES = 100
MAX_SECURITY_EVIDENCE = 100
PYTHON_SUFFIX = ".py"
SENSITIVE_FILES = {
    ".env",
    "credentials.json",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
}
SECRET_NAME = re.compile(
    r"(?:api[_-]?key|access[_-]?key|client[_-]?secret|password|passwd|private[_-]?key|secret|token)",
    re.IGNORECASE,
)
PRIVATE_KEY = re.compile(
    r"-----BEGIN\s+(?:(?:RSA|EC|OPENSSH)\s+)?PRIVATE\s+KEY-----"
)
AWS_ACCESS_KEY = re.compile(
    r"(?<![A-Z0-9])(?:A3T[A-Z0-9]|AKIA|ASIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASCA)[A-Z0-9]{16}(?![A-Z0-9])"
)
GITHUB_TOKEN = re.compile(r"(?<![A-Za-z0-9])gh[pousr]_[A-Za-z0-9]{20,255}(?![A-Za-z0-9])")
CONTROL_REMOVAL = re.compile(
    r"\b(?:authorize|authorization|check_access|csrf|is_authenticated|permission|"
    r"require_auth|resolve_within_repository|sanitize|validate|verify_signature)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class SecuritySignal:
    rule_id: str
    category: str
    severity: Severity
    confidence: Confidence
    kind: EvidenceKind
    message: str
    payload: dict[str, Any]
    location: dict[str, Any]
    suggestion: str

    def evidence(self) -> Evidence:
        return Evidence(self.kind, "current Git change", self.payload)


class SecurityAuditService:
    def __init__(self, repository_root: Path, git_inspector: GitInspector) -> None:
        self.repository_root = repository_root.resolve(strict=True)
        self.git_inspector = git_inspector

    def audit(self, *, mode: DiffMode = "combined") -> CheckResult:
        try:
            snapshot = self.git_inspector.snapshot(mode)
            added_lines, added_truncated = self.git_inspector.added_lines(mode)
            removed_lines, removed_truncated = self.git_inspector.removed_lines(mode)
        except (OSError, RuntimeError, ValueError) as exc:
            return CheckResult(
                CheckStatus.ERROR,
                "Security audit could not inspect the current Git change.",
                errors=(CheckError("INVALID_INPUT", str(exc)),),
            )
        if not snapshot.files:
            return CheckResult(
                CheckStatus.NOT_APPLICABLE,
                "No current Git changes require defensive security auditing.",
                evidence=(Evidence(EvidenceKind.FACT, "git diff", {"changed_files": 0}),),
                metadata=self._metadata(
                    suppressed=0,
                    review_surfaces=(),
                    truncated=added_truncated or removed_truncated,
                    inspected_files=0,
                ),
            )

        signals: list[SecuritySignal] = []
        suppressed = 0
        signals.extend(self._sensitive_file_signals(snapshot.files))
        secret_signals, secret_suppressed = self._secret_signals(added_lines)
        signals.extend(secret_signals)
        suppressed += secret_suppressed

        added_by_path: dict[str, set[int]] = {}
        for line in added_lines:
            added_by_path.setdefault(line.path, set()).add(line.line_number)
        inspected_files = 0
        source_truncated = False
        for path, line_numbers in sorted(added_by_path.items()):
            if PurePosixPath(path).suffix.lower() != PYTHON_SUFFIX:
                continue
            if inspected_files >= MAX_SECURITY_SOURCE_FILES:
                source_truncated = True
                break
            candidate = resolve_within_repository(self.repository_root, path)
            if not candidate.is_file():
                continue
            if candidate.stat().st_size > MAX_SECURITY_SOURCE_BYTES:
                source_truncated = True
                continue
            inspected_files += 1
            text = candidate.read_text(encoding="utf-8", errors="replace")
            python_signals, python_suppressed = self._python_signals(
                path, text, line_numbers
            )
            signals.extend(python_signals)
            suppressed += python_suppressed

        signals.extend(self._removed_control_signals(removed_lines))
        signals = _deduplicate_signals(signals)
        findings = _group_findings(signals)
        truncated = added_truncated or removed_truncated or source_truncated
        review_surfaces = tuple(
            sorted(
                change.path
                for change in snapshot.files
                if _security_sensitive_path(change.path)
            )
        )
        warnings = []
        if truncated:
            warnings.append("Security inspection reached an explicit input or source-file limit.")
        return CheckResult(
            CheckStatus.WARNING if findings or truncated else CheckStatus.PASS,
            (
                f"Defensive security audit produced {len(findings)} finding(s) from "
                f"{len(snapshot.files)} changed file(s)."
            ),
            findings=findings,
            evidence=(
                Evidence(
                    EvidenceKind.FACT,
                    "git diff",
                    {
                        "mode": mode,
                        "changed_files": len(snapshot.files),
                        "added_lines_inspected": len(added_lines),
                        "removed_lines_inspected": len(removed_lines),
                    },
                ),
            ),
            metadata={
                **self._metadata(
                    suppressed=suppressed,
                    review_surfaces=review_surfaces,
                    truncated=truncated,
                    inspected_files=inspected_files,
                ),
                "warnings": warnings,
            },
        )

    def _sensitive_file_signals(self, changes) -> list[SecuritySignal]:
        signals = []
        for change in changes:
            if change.status not in {"added", "untracked"}:
                continue
            name = PurePosixPath(change.path).name.lower()
            suffix = PurePosixPath(change.path).suffix.lower()
            if name.endswith(".example") or name.endswith(".sample"):
                continue
            if name not in SENSITIVE_FILES and suffix not in {".key", ".pem", ".p12", ".pfx"}:
                continue
            signals.append(
                SecuritySignal(
                    "AA-SEC-SECRET-001",
                    "security-secrets",
                    Severity.MEDIUM,
                    Confidence.MEDIUM,
                    EvidenceKind.HEURISTIC,
                    "The current change adds a credential-sensitive file or credential-like value.",
                    {
                        "path": change.path,
                        "signal": "sensitive file added",
                        "credential_format": "sensitive-file",
                        "redacted_value": None,
                        "test_fixture": _is_test_path(change.path),
                        "cannot_prove": "that the file contains a live credential",
                    },
                    {"path": change.path},
                    "Remove the sensitive file or verify that it contains only documented placeholders.",
                )
            )
        return signals

    def _secret_signals(
        self, added_lines: tuple[GitAddedLine, ...]
    ) -> tuple[list[SecuritySignal], int]:
        signals: list[SecuritySignal] = []
        suppressed = 0
        for line in added_lines:
            for value, credential_format in _recognized_credentials(line.text):
                if _is_placeholder(value):
                    suppressed += 1
                    continue
                signals.append(_secret_signal(line.path, line.line_number, value, credential_format))
        return signals, suppressed

    def _python_signals(
        self,
        path: str,
        text: str,
        added_line_numbers: set[int],
    ) -> tuple[list[SecuritySignal], int]:
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError):
            return [], 0
        signals: list[SecuritySignal] = []
        suppressed = 0
        for node in ast.walk(tree):
            line = getattr(node, "lineno", None)
            if line not in added_line_numbers:
                continue
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
                names = _assignment_names(node)
                value_node = node.value
                if any(SECRET_NAME.search(name) for name in names):
                    if isinstance(value_node, ast.Constant) and isinstance(value_node.value, str):
                        value = value_node.value
                        recognized = _recognized_credentials(value)
                        if recognized:
                            for candidate, credential_format in recognized:
                                if _is_placeholder(candidate):
                                    suppressed += 1
                                else:
                                    signals.append(_secret_signal(path, line, candidate, credential_format))
                        elif _is_placeholder(value):
                            suppressed += 1
                        elif len(value) >= 8:
                            signals.append(_secret_signal(path, line, value, "hardcoded-secret-like-assignment"))
                    else:
                        suppressed += 1
            if not isinstance(node, ast.Call):
                if isinstance(node, (ast.Assign, ast.AnnAssign)) and _is_false_assignment(node, "check_hostname"):
                    signals.append(_weakening_signal(path, line, "TLS hostname checking set to false"))
                continue
            call_name = _call_name(node.func)
            if call_name in {"os.system", "os.popen"} or (
                call_name.startswith("subprocess.") and _literal_keyword(node, "shell") is True
            ):
                signals.append(
                    _call_signal(
                        "AA-SEC-SHELL-001",
                        "security-shell-execution",
                        Severity.HIGH,
                        path,
                        line,
                        call_name,
                        "Shell execution is explicitly enabled in the current change.",
                        "Use fixed argv with shell disabled, or document and strictly constrain the shell boundary.",
                    )
                )
            if call_name in {"eval", "exec", "builtins.eval", "builtins.exec"}:
                signals.append(
                    _call_signal(
                        "AA-SEC-DYNAMIC-EXEC-001",
                        "security-dynamic-execution",
                        Severity.HIGH,
                        path,
                        line,
                        call_name,
                        "The current change adds dynamic code execution.",
                        "Replace dynamic execution with a typed parser or a fixed operation allowlist.",
                    )
                )
            if call_name == "tempfile.mktemp":
                signals.append(
                    _call_signal(
                        "AA-SEC-TEMP-001",
                        "security-temporary-files",
                        Severity.MEDIUM,
                        path,
                        line,
                        call_name,
                        "The current change uses a race-prone temporary filename API.",
                        "Use NamedTemporaryFile, TemporaryDirectory, or mkstemp and keep the returned handle/descriptor.",
                    )
                )
            if _filesystem_sink(call_name) and any(
                _contains_parent_segment(value)
                for value in _constant_strings(node.args)
            ):
                signals.append(
                    SecuritySignal(
                        "AA-SEC-PATH-001",
                        "security-path-boundary",
                        Severity.MEDIUM,
                        Confidence.MEDIUM,
                        EvidenceKind.HEURISTIC,
                        "The current change passes an explicit parent traversal to a filesystem operation.",
                        {
                            "path": path,
                            "line": line,
                            "call": call_name,
                            "signal": "constant parent traversal at filesystem sink",
                            "cannot_prove": "that the resolved path escapes the repository or another intended root",
                        },
                        {"path": path, "line": line},
                        "Resolve the path against an explicit root and reject lexical and physical escape.",
                    )
                )
            if call_name == "ssl._create_unverified_context" or (
                _network_call(call_name) and _literal_keyword(node, "verify") is False
            ):
                signals.append(_weakening_signal(path, line, "TLS certificate verification disabled"))
        return signals, suppressed

    def _removed_control_signals(
        self, removed_lines: tuple[GitRemovedLine, ...]
    ) -> list[SecuritySignal]:
        signals = []
        for line in removed_lines:
            if _is_test_path(line.path) or not CONTROL_REMOVAL.search(line.text):
                continue
            stripped = line.text.strip()
            if not stripped or stripped.startswith(("#", "//", "*")):
                continue
            signals.append(
                SecuritySignal(
                    "AA-SEC-WEAKENING-001",
                    "security-control-weakening",
                    Severity.MEDIUM,
                    Confidence.MEDIUM,
                    EvidenceKind.MANUAL_REVIEW_REQUIRED,
                    "The current change removes or disables a recognizable security control.",
                    {
                        "path": line.path,
                        "line": line.line_number,
                        "signal": "security-sensitive line removed",
                        "control_terms": sorted({term.lower() for term in CONTROL_REMOVAL.findall(line.text)}),
                        "cannot_prove": "that an equivalent control was not moved or replaced",
                    },
                    {"path": line.path, "line": line.line_number},
                    "Confirm the replacement control and add a negative regression test for the protected operation.",
                )
            )
        return signals

    @staticmethod
    def _metadata(
        *,
        suppressed: int,
        review_surfaces: tuple[str, ...],
        truncated: bool,
        inspected_files: int,
    ) -> dict[str, Any]:
        return {
            "rules_evaluated": [
                "AA-SEC-SECRET-001",
                "AA-SEC-SHELL-001",
                "AA-SEC-DYNAMIC-EXEC-001",
                "AA-SEC-PATH-001",
                "AA-SEC-TEMP-001",
                "AA-SEC-WEAKENING-001",
            ],
            "policy": {
                "scope": "current Git additions/removals and configuration only",
                "network": "no network requests or exploitation",
                "secrets": "credential-like values are always redacted; liveness is never claimed",
                "review_surfaces": "sensitive filenames are observations unless a specific detector has evidence",
            },
            "security_sensitive_review_surfaces": list(review_surfaces),
            "suppressed_secret_candidates": suppressed,
            "limits": {
                "max_source_bytes": MAX_SECURITY_SOURCE_BYTES,
                "max_source_files": MAX_SECURITY_SOURCE_FILES,
                "max_finding_evidence": MAX_SECURITY_EVIDENCE,
                "source_files_inspected": inspected_files,
                "truncated": truncated,
            },
        }


def _secret_signal(path: str, line: int, value: str, credential_format: str) -> SecuritySignal:
    fixture = _is_test_path(path)
    return SecuritySignal(
        "AA-SEC-SECRET-001",
        "security-secrets",
        Severity.LOW if fixture else Severity.HIGH,
        Confidence.MEDIUM,
        EvidenceKind.MANUAL_REVIEW_REQUIRED if fixture else EvidenceKind.HEURISTIC,
        "The current change adds a credential-sensitive file or credential-like value.",
        {
            "path": path,
            "line": line,
            "credential_format": credential_format,
            "redacted_value": _redact(value),
            "test_fixture": fixture,
            "cannot_prove": "that the value is live or grants access",
        },
        {"path": path, "line": line},
        "Remove the value from version control and confirm rotation/revocation if it was ever usable.",
    )


def _call_signal(
    rule_id: str,
    category: str,
    severity: Severity,
    path: str,
    line: int,
    call: str,
    message: str,
    suggestion: str,
) -> SecuritySignal:
    return SecuritySignal(
        rule_id,
        category,
        severity,
        Confidence.HIGH,
        EvidenceKind.FACT,
        message,
        {"path": path, "line": line, "call": call},
        {"path": path, "line": line},
        suggestion,
    )


def _weakening_signal(path: str, line: int, signal: str) -> SecuritySignal:
    return SecuritySignal(
        "AA-SEC-WEAKENING-001",
        "security-control-weakening",
        Severity.HIGH,
        Confidence.HIGH,
        EvidenceKind.FACT,
        "The current change removes or disables a recognizable security control.",
        {"path": path, "line": line, "signal": signal},
        {"path": path, "line": line},
        "Restore the control or document the replacement and prove it with a negative test.",
    )


def _group_findings(signals: list[SecuritySignal]) -> tuple[Finding, ...]:
    grouped: dict[str, list[SecuritySignal]] = {}
    for signal in signals:
        grouped.setdefault(signal.rule_id, []).append(signal)
    findings = []
    for rule_id in (
        "AA-SEC-SECRET-001",
        "AA-SEC-SHELL-001",
        "AA-SEC-DYNAMIC-EXEC-001",
        "AA-SEC-PATH-001",
        "AA-SEC-TEMP-001",
        "AA-SEC-WEAKENING-001",
    ):
        items = grouped.get(rule_id, [])
        if not items:
            continue
        first = items[0]
        findings.append(
            Finding(
                rule_id,
                first.category,
                max((item.severity for item in items), key=_severity_rank),
                max((item.confidence for item in items), key=_confidence_rank),
                f"{first.message} {len(items)} signal(s) observed.",
                tuple(item.evidence() for item in items[:MAX_SECURITY_EVIDENCE]),
                first.location,
                first.suggestion,
            )
        )
    return tuple(findings)


def _deduplicate_signals(signals: list[SecuritySignal]) -> list[SecuritySignal]:
    unique: dict[tuple[Any, ...], SecuritySignal] = {}
    for signal in signals:
        key = (
            signal.rule_id,
            signal.location.get("path"),
            signal.location.get("line"),
            signal.payload.get("credential_format"),
            signal.payload.get("call"),
            signal.payload.get("signal"),
        )
        unique.setdefault(key, signal)
    return list(unique.values())


def _recognized_credentials(value: str) -> list[tuple[str, str]]:
    matches: list[tuple[str, str]] = []
    for pattern, name in (
        (PRIVATE_KEY, "private-key-material"),
        (AWS_ACCESS_KEY, "aws-access-key-id"),
        (GITHUB_TOKEN, "github-token"),
    ):
        matches.extend((match.group(0), name) for match in pattern.finditer(value))
    return matches


def _redact(value: str) -> str:
    if len(value) <= 4:
        return "*" * len(value)
    if len(value) <= 8:
        return value[:2] + "*" * (len(value) - 4) + value[-2:]
    return value[:4] + "*" * (len(value) - 8) + value[-4:]


def _is_placeholder(value: str) -> bool:
    folded = value.casefold()
    markers = (
        "changeme",
        "dummy",
        "example",
        "fake",
        "not-a-real",
        "placeholder",
        "sample",
        "your-api",
        "your_api",
    )
    compact = re.sub(r"[^a-z0-9]", "", folded)
    return any(marker in folded for marker in markers) or (
        len(compact) >= 8 and len(set(compact)) <= 2
    )


def _assignment_names(node: ast.AST) -> tuple[str, ...]:
    if isinstance(node, ast.Assign):
        targets = node.targets
    elif isinstance(node, (ast.AnnAssign, ast.NamedExpr)):
        targets = [node.target]
    else:
        return ()
    names = []
    for target in targets:
        if isinstance(target, ast.Name):
            names.append(target.id)
        elif isinstance(target, ast.Attribute):
            names.append(target.attr)
    return tuple(names)


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        owner = _call_name(node.value)
        return f"{owner}.{node.attr}" if owner else node.attr
    return ""


def _literal_keyword(node: ast.Call, name: str) -> Any:
    for keyword in node.keywords:
        if keyword.arg == name and isinstance(keyword.value, ast.Constant):
            return keyword.value.value
    return None


def _constant_strings(nodes: list[ast.expr]) -> tuple[str, ...]:
    return tuple(
        node.value
        for node in nodes
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    )


def _contains_parent_segment(value: str) -> bool:
    return ".." in value.replace("\\", "/").split("/")


def _filesystem_sink(call_name: str) -> bool:
    return call_name in {
        "Path",
        "open",
        "os.listdir",
        "os.makedirs",
        "os.mkdir",
        "os.remove",
        "os.rename",
        "os.replace",
        "os.scandir",
        "os.unlink",
        "pathlib.Path",
    } or call_name.endswith(".open")


def _network_call(call_name: str) -> bool:
    return call_name.startswith(("httpx.", "requests.", "urllib3."))


def _is_false_assignment(node: ast.Assign | ast.AnnAssign, name: str) -> bool:
    value = node.value
    return name in _assignment_names(node) and isinstance(value, ast.Constant) and value.value is False


def _security_sensitive_path(path: str) -> bool:
    folded = path.casefold()
    return any(
        token in folded
        for token in (
            "auth",
            "cors",
            "cookie",
            "credential",
            "permission",
            "security",
            "session",
            "token",
            "upload",
        )
    )


def _is_test_path(path: str) -> bool:
    pure = PurePosixPath(path)
    parts = {part.lower() for part in pure.parts}
    name = pure.name.lower()
    return (
        "tests" in parts
        or "test" in parts
        or "__tests__" in parts
        or name.startswith("test_")
        or ".test." in name
        or ".spec." in name
    )


def _severity_rank(severity: Severity) -> int:
    return {
        Severity.INFO: 0,
        Severity.LOW: 1,
        Severity.MEDIUM: 2,
        Severity.HIGH: 3,
        Severity.CRITICAL: 4,
    }[severity]


def _confidence_rank(confidence: Confidence) -> int:
    return {Confidence.LOW: 0, Confidence.MEDIUM: 1, Confidence.HIGH: 2}[confidence]
