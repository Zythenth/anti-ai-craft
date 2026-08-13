from __future__ import annotations

import io
import re
import tokenize
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .architecture import ArchitectureService
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
from .git import DiffMode, GitAddedLine, GitFileChange, GitInspector, GitRemovedLine
from .graph import GraphProvider, GraphProviderError
from .graph_evidence import GraphEvidenceNormalizer
from .paths import resolve_within_repository


MAX_AUDIT_SOURCE_BYTES = 256 * 1024
MAX_RULE_EVIDENCE = 100
MAX_NEW_SOURCE_FILES = 100
SOURCE_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".go",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".swift",
    ".ts",
    ".tsx",
    ".vue",
}


@dataclass(frozen=True)
class NewFileSignal:
    path: str
    line_count: int
    graph_nodes: int
    external_relations: int | None
    external_consumers: int | None
    has_abstraction: bool
    excluded_role: str | None


@dataclass(frozen=True)
class AntiAiAuditContext:
    changes: tuple[GitFileChange, ...]
    added_lines: tuple[GitAddedLine, ...]
    added_lines_truncated: bool
    removed_lines: tuple[GitRemovedLine, ...]
    removed_lines_truncated: bool
    new_files: tuple[NewFileSignal, ...]
    new_files_truncated: bool
    graph: GraphEvidenceNormalizer


@dataclass(frozen=True)
class PlaceholderRule:
    id: str = "AA-AI-PLACEHOLDER-001"
    category: str = "anti-ai-placeholder"
    description: str = "New diff lines should not introduce unresolved implementation placeholders."
    deterministic: bool = False

    def evaluate(self, context: AntiAiAuditContext) -> tuple[Finding, ...]:
        matches = [
            line
            for line in context.added_lines
            if PurePosixPath(line.path).suffix.lower() in SOURCE_EXTENSIONS
            and not _is_test_path(line.path)
            and _placeholder_kind(
                line.text, PurePosixPath(line.path).suffix.lower()
            )
        ]
        if not matches:
            return ()
        evidence = tuple(
            Evidence(
                EvidenceKind.HEURISTIC,
                "Git added line",
                {
                    "path": line.path,
                    "line": line.line_number,
                    "signal": _placeholder_kind(
                        line.text, PurePosixPath(line.path).suffix.lower()
                    ),
                    "text": line.text[:300],
                },
            )
            for line in matches[:MAX_RULE_EVIDENCE]
        )
        return (
            Finding(
                self.id,
                self.category,
                Severity.MEDIUM,
                Confidence.MEDIUM,
                f"The current diff introduces {len(matches)} placeholder signal(s).",
                evidence,
                location={"path": matches[0].path, "line": matches[0].line_number},
                suggestion="Implement or remove each new placeholder, or document why it is intentionally deferred.",
            ),
        )


@dataclass(frozen=True)
class TestBypassRule:
    id: str = "AA-AI-TEST-BYPASS-001"
    category: str = "anti-ai-test-bypass"
    description: str = "Current changes should not silently remove or newly skip test coverage."
    deterministic: bool = False

    def evaluate(self, context: AntiAiAuditContext) -> tuple[Finding, ...]:
        deleted = [
            change.path
            for change in context.changes
            if change.status == "deleted" and _is_test_path(change.path)
        ]
        skips = [line for line in context.added_lines if _is_skip_marker(line.text)]
        exclusions = [
            line
            for line in context.added_lines
            if _is_validation_exclusion(line.text, line.path)
        ]
        added_assertions = [
            line
            for line in context.added_lines
            if _is_test_path(line.path) and _is_assertion(line.text)
        ]
        removed_assertions = [
            line
            for line in context.removed_lines
            if _is_test_path(line.path) and _is_assertion(line.text)
        ]
        net_removed_assertions = max(0, len(removed_assertions) - len(added_assertions))
        removed_assertions = removed_assertions[:net_removed_assertions]
        if not deleted and not skips and not exclusions and not removed_assertions:
            return ()
        evidence: list[Evidence] = [
            Evidence(
                EvidenceKind.FACT,
                "Git diff",
                {"path": path, "change": "deleted test file"},
            )
            for path in deleted[:MAX_RULE_EVIDENCE]
        ]
        available = max(0, MAX_RULE_EVIDENCE - len(evidence))
        evidence.extend(
            Evidence(
                EvidenceKind.HEURISTIC,
                "Git added line",
                {
                    "path": line.path,
                    "line": line.line_number,
                    "signal": "new test skip/xfail marker",
                    "text": line.text[:300],
                },
            )
            for line in skips[:available]
        )
        available = max(0, MAX_RULE_EVIDENCE - len(evidence))
        evidence.extend(
            Evidence(
                EvidenceKind.HEURISTIC,
                "Git added line",
                {
                    "path": line.path,
                    "line": line.line_number,
                    "signal": "new coverage/validation exclusion",
                    "text": line.text[:300],
                },
            )
            for line in exclusions[:available]
        )
        available = max(0, MAX_RULE_EVIDENCE - len(evidence))
        evidence.extend(
            Evidence(
                EvidenceKind.HEURISTIC,
                "Git removed line",
                {
                    "path": line.path,
                    "line": line.line_number,
                    "signal": "removed test assertion",
                    "text": line.text[:300],
                },
            )
            for line in removed_assertions[:available]
        )
        return (
            Finding(
                self.id,
                self.category,
                Severity.HIGH,
                Confidence.MEDIUM,
                (
                    f"The current change deletes {len(deleted)} test file(s), introduces "
                    f"{len(skips)} skip/xfail marker(s), adds {len(exclusions)} validation "
                    f"exclusion(s), and removes {len(removed_assertions)} assertion(s)."
                ),
                tuple(evidence),
                location={
                    "path": (
                        deleted[0]
                        if deleted
                        else (skips or exclusions or removed_assertions)[0].path
                    )
                },
                suggestion="Restore the coverage or provide a reviewed reason and replacement validation.",
            ),
        )


@dataclass(frozen=True)
class FileProliferationRule:
    id: str = "AA-AI-FILE-PROLIFERATION-001"
    category: str = "anti-ai-file-proliferation"
    description: str = "Flag compound evidence of many small, structurally isolated production files."
    deterministic: bool = False

    def evaluate(self, context: AntiAiAuditContext) -> tuple[Finding, ...]:
        production = [item for item in context.new_files if item.excluded_role is None]
        small = [item for item in production if item.line_count <= 80]
        isolated = [
            item
            for item in production
            if item.graph_nodes > 0 and item.external_relations == 0
        ]
        if (
            len(production) < 6
            or len(small) < 4
            or len(isolated) < 3
            or len(isolated) * 2 < len(production)
        ):
            return ()
        evidence = Evidence(
            EvidenceKind.HEURISTIC,
            "Git new files plus graph adjacency",
            {
                "new_production_source_files": len(production),
                "small_files_at_or_below_80_lines": len(small),
                "structurally_isolated_files": [item.path for item in isolated],
                "freshness": context.graph.status.freshness.value,
                "cannot_prove": "that the files are unnecessary or should be merged",
            },
        )
        return (
            Finding(
                self.id,
                self.category,
                Severity.LOW,
                Confidence.LOW if context.graph.non_fresh else Confidence.MEDIUM,
                "The change creates a cluster of small production files with little observed external structure.",
                (evidence,),
                suggestion="Confirm each file has a distinct owner or boundary; keep generated/scaffolded files when required.",
            ),
        )


@dataclass(frozen=True)
class UnusedAbstractionRule:
    id: str = "AA-AI-ABSTRACTION-001"
    category: str = "anti-ai-abstraction"
    description: str = "Flag new abstractions with no observed external structural relationship."
    deterministic: bool = False

    def evaluate(self, context: AntiAiAuditContext) -> tuple[Finding, ...]:
        candidates = [
            item
            for item in context.new_files
            if item.excluded_role is None
            and item.has_abstraction
            and item.graph_nodes > 0
            and item.external_relations == 0
        ]
        if not candidates:
            return ()
        direction_known = context.graph.status.capabilities.dependents
        evidence = tuple(
            Evidence(
                EvidenceKind.HEURISTIC,
                "Git new file plus graph structure",
                {
                    "path": item.path,
                    "graph_nodes": item.graph_nodes,
                    "external_structural_relations": item.external_relations,
                    "external_consumers": item.external_consumers,
                    "direction": "KNOWN" if direction_known else "UNKNOWN",
                    "freshness": context.graph.status.freshness.value,
                    "cannot_prove": "that the abstraction is unused at runtime",
                },
            )
            for item in candidates[:MAX_RULE_EVIDENCE]
        )
        return (
            Finding(
                self.id,
                self.category,
                Severity.LOW,
                Confidence.LOW if context.graph.non_fresh or not direction_known else Confidence.MEDIUM,
                f"{len(candidates)} new abstraction file(s) have no observed external structural relationship.",
                evidence,
                location={"path": candidates[0].path},
                suggestion="Confirm a real consumer, entrypoint, fixture, or required interface; otherwise remove the unused abstraction.",
            ),
        )


class AntiAiAuditService:
    def __init__(
        self,
        repository_root: Path,
        git_inspector: GitInspector,
        graph_provider: GraphProvider,
        architecture_service: ArchitectureService,
    ) -> None:
        self.repository_root = repository_root.resolve(strict=True)
        self.git_inspector = git_inspector
        self.graph_provider = graph_provider
        self.architecture_service = architecture_service
        self.rules = (
            PlaceholderRule(),
            TestBypassRule(),
            FileProliferationRule(),
            UnusedAbstractionRule(),
        )

    def audit(self, *, mode: DiffMode = "combined") -> CheckResult:
        try:
            snapshot = self.git_inspector.snapshot(mode)
            added_lines, lines_truncated = self.git_inspector.added_lines(mode)
            removed_lines, removed_lines_truncated = self.git_inspector.removed_lines(mode)
        except (RuntimeError, ValueError) as exc:
            return CheckResult(
                CheckStatus.ERROR,
                "Anti-AI audit could not inspect the current Git change.",
                errors=(CheckError("AA-AI-GIT", str(exc)),),
            )
        status = self.graph_provider.get_status()
        normalizer = GraphEvidenceNormalizer(status)
        new_files, new_files_truncated = self._new_file_signals(
            snapshot.files, normalizer
        )
        context = AntiAiAuditContext(
            snapshot.files,
            added_lines,
            lines_truncated,
            removed_lines,
            removed_lines_truncated,
            new_files,
            new_files_truncated,
            normalizer,
        )
        architecture = self.architecture_service.audit(mode=mode, graph_status=status)
        rule_findings = tuple(
            finding
            for rule in self.rules
            for finding in rule.evaluate(context)
        )
        architecture_findings = tuple(
            finding
            for finding in architecture.findings
            if finding.id not in {"AA-ARCH-001"}
        )
        findings = rule_findings + architecture_findings
        graph_metadata = normalizer.graph_metadata(
            truncated=lines_truncated or removed_lines_truncated or new_files_truncated,
            coverage={
                "new_source_files": len(context.new_files),
                "new_source_files_with_graph_nodes": sum(
                    item.graph_nodes > 0 for item in context.new_files
                ),
            },
        )
        warnings = normalizer.warnings()
        if lines_truncated:
            warnings.append("Added-line inspection reached its explicit limit.")
        if new_files_truncated:
            warnings.append("New-source-file inspection reached its explicit limit.")
        if not snapshot.files:
            return CheckResult(
                CheckStatus.NOT_APPLICABLE,
                "No current Git changes require Anti-AI auditing.",
                evidence=(Evidence(EvidenceKind.FACT, "git diff", {"changed_files": 0}),),
                metadata={
                    "graph": graph_metadata,
                    "warnings": warnings,
                    "rule_policies": _rule_policies(),
                },
            )
        result_status = (
            CheckStatus.WARNING
            if findings
            or not normalizer.usable
            or normalizer.non_fresh
            or lines_truncated
            or new_files_truncated
            else CheckStatus.PASS
        )
        return CheckResult(
            result_status,
            (
                f"Evaluated {len(self.rules)} Anti-AI rule(s) and conservative architecture signals; "
                f"produced {len(findings)} finding(s)."
            ),
            findings=findings,
            evidence=(
                Evidence(
                    EvidenceKind.FACT,
                    "Git diff",
                    {
                        "mode": mode,
                        "changed_files": len(snapshot.files),
                        "added_lines_inspected": len(added_lines),
                        "truncated": lines_truncated,
                    },
                ),
                Evidence(EvidenceKind.FACT, "graph provider status", graph_metadata),
            ),
            metadata={
                "graph": graph_metadata,
                "warnings": warnings,
                "rules_evaluated": [rule.id for rule in self.rules],
                "rule_policies": _rule_policies(),
                "deterministic_evidence_available": True,
                "graph_evidence_available": normalizer.usable,
                "architecture": architecture.metadata,
                "limits": {
                    "max_added_lines": 2_000,
                    "max_source_bytes": MAX_AUDIT_SOURCE_BYTES,
                    "max_new_source_files": MAX_NEW_SOURCE_FILES,
                    "max_rule_evidence": MAX_RULE_EVIDENCE,
                    "truncated": lines_truncated or new_files_truncated,
                },
            },
        )

    def _new_file_signals(
        self,
        changes: tuple[GitFileChange, ...],
        normalizer: GraphEvidenceNormalizer,
    ) -> tuple[tuple[NewFileSignal, ...], bool]:
        signals = []
        truncated = False
        for change in changes:
            if change.status not in {"added", "untracked"}:
                continue
            suffix = PurePosixPath(change.path).suffix.lower()
            if suffix not in SOURCE_EXTENSIONS:
                continue
            if len(signals) >= MAX_NEW_SOURCE_FILES:
                truncated = True
                break
            candidate = resolve_within_repository(self.repository_root, change.path)
            if not candidate.is_file() or candidate.stat().st_size > MAX_AUDIT_SOURCE_BYTES:
                continue
            text = candidate.read_text(encoding="utf-8", errors="replace")
            graph_nodes = 0
            external: set[str] = set()
            consumers: set[str] | None = set() if normalizer.status.capabilities.dependents else None
            if normalizer.usable:
                try:
                    file_nodes = self.graph_provider.get_nodes_for_file(change.path, limit=100)
                    graph_nodes = len(file_nodes.nodes)
                    for node in file_nodes.nodes:
                        neighbors = self.graph_provider.get_neighbors(
                            node.id, direction="both", limit=100
                        )
                        external.update(
                            related.id
                            for related in neighbors.nodes
                            if related.id != node.id and related.source_file != change.path
                        )
                        if consumers is not None:
                            dependents = self.graph_provider.get_dependents(
                                node.id, limit=100
                            )
                            consumers.update(
                                related.id
                                for related in dependents.nodes
                                if related.id != node.id and related.source_file != change.path
                            )
                except GraphProviderError:
                    graph_nodes = 0
                    external.clear()
                    consumers = None
            signals.append(
                NewFileSignal(
                    path=change.path,
                    line_count=len(text.splitlines()),
                    graph_nodes=graph_nodes,
                    external_relations=len(external) if graph_nodes else None,
                    external_consumers=len(consumers) if consumers is not None else None,
                    has_abstraction=_has_abstraction(text, suffix),
                    excluded_role=_excluded_role(change.path),
                )
            )
        return tuple(signals), truncated


def _placeholder_kind(text: str, suffix: str = "") -> str | None:
    if suffix == ".py":
        try:
            tokens = tuple(tokenize.generate_tokens(io.StringIO(text).readline))
        except (IndentationError, tokenize.TokenError):
            tokens = ()
        if any(
            token.type == tokenize.COMMENT
            and re.search(r"\b(?:TODO|FIXME)\b", token.string, re.IGNORECASE)
            for token in tokens
        ):
            return "TODO/FIXME"
        if any(
            token.type == tokenize.NAME
            and token.string in {"NotImplemented", "NotImplementedError"}
            for token in tokens
        ):
            return "NotImplemented"
        return None
    if re.search(r"(?:#|//|/\*|\*)[^\n]*\b(?:TODO|FIXME)\b", text, re.IGNORECASE):
        return "TODO/FIXME"
    if re.search(r"\bNotImplemented(?:Error)?\b", text):
        return "NotImplemented"
    if re.search(r"throw\s+new\s+Error\s*\([^)]*TODO", text, re.IGNORECASE):
        return "throw TODO error"
    return None


def _is_skip_marker(text: str) -> bool:
    return bool(
        re.search(
            r"pytest\.mark\.(?:skip|skipif|xfail)\b|"
            r"unittest\.(?:skip|skipIf|skipUnless)\b|"
            r"(?:describe|it|test)\.skip\s*\(",
            text,
        )
    )


def _is_validation_exclusion(text: str, path: str) -> bool:
    suffix = PurePosixPath(path).suffix.lower()
    if suffix == ".py":
        try:
            comments = " ".join(
                token.string
                for token in tokenize.generate_tokens(io.StringIO(text).readline)
                if token.type == tokenize.COMMENT
            )
        except (IndentationError, tokenize.TokenError):
            comments = ""
        return bool(
            re.search(
                r"pragma:\s*no\s*cover\b|#\s*noqa\b|"
                r"#\s*type:\s*ignore\b|mypy:\s*ignore-errors\b|ruff:\s*noqa\b",
                comments,
                re.IGNORECASE,
            )
        )
    return bool(
        re.search(
            r"pragma:\s*no\s*cover\b|istanbul\s+ignore\b|c8\s+ignore\b|"
            r"eslint-disable\b|ruff:\s*noqa\b|#\s*noqa\b|"
            r"#\s*type:\s*ignore\b|@ts-ignore\b|mypy:\s*ignore-errors\b",
            text,
            re.IGNORECASE,
        )
    )


def _is_assertion(text: str) -> bool:
    return bool(
        re.search(
            r"^\s*assert\b|\bself\.assert[A-Za-z]*\s*\(|\bexpect\s*\([^)]*\)\s*\.",
            text,
        )
    )


def _has_abstraction(text: str, suffix: str) -> bool:
    if suffix == ".py":
        return bool(re.search(r"^(?:class|def)\s+[A-Za-z_]", text, re.MULTILINE))
    return bool(
        re.search(
            r"\b(?:class|interface|abstract\s+class|function)\s+[A-Za-z_$]",
            text,
        )
    )


def _excluded_role(path: str) -> str | None:
    pure = PurePosixPath(path)
    name = pure.name.lower()
    if _is_test_path(path):
        return "test or fixture"
    if name in {"__init__.py", "__main__.py", "main.py", "cli.py", "manage.py"}:
        return "possible entrypoint"
    if any(token in name for token in ("fixture", "migration", "generated", "schema")):
        return "fixture/generated/framework file"
    if any(token in name for token in ("interface", "protocol", "types")):
        return "possible required interface"
    return None


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


def _rule_policies() -> dict[str, dict[str, Any]]:
    return {
        "AA-AI-PLACEHOLDER-001": {
            "detects": "new TODO/FIXME and explicit unimplemented-error signals in added diff lines",
            "cannot_prove": "that the placeholder is unintended or reachable",
            "known_false_positives": ["tracked work markers", "intentional abstract methods", "test fixtures"],
            "confidence": "MEDIUM; pre-existing lines are excluded",
        },
        "AA-AI-TEST-BYPASS-001": {
            "detects": "deleted test files, newly added skip/xfail or validation exclusions, and removed test assertions",
            "cannot_prove": "that validation was bypassed rather than intentionally replaced",
            "known_false_positives": ["obsolete tests", "quarantine with replacement coverage"],
            "confidence": "MEDIUM; the Git delta is factual, intent is not",
        },
        "AA-AI-FILE-PROLIFERATION-001": {
            "detects": "a compound cluster of new, small, structurally isolated production files",
            "cannot_prove": "that the files are unnecessary or should share one module",
            "known_false_positives": ["generated code", "framework scaffolding", "deliberate package boundaries"],
            "confidence": "LOW when stale, otherwise MEDIUM",
        },
        "AA-AI-ABSTRACTION-001": {
            "detects": "new abstraction files with graph nodes but no observed external relationship",
            "cannot_prove": "runtime use, dynamic imports, registration, reflection, or future required interfaces",
            "known_false_positives": ["entrypoints", "fixtures", "plugin registration", "dynamic consumers"],
            "confidence": "LOW for stale/undirected graphs; MEDIUM only with fresh directed evidence",
        },
    }
