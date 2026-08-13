from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

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
from .git import DiffMode, GitFileChange, GitInspector
from .paths import PathBoundaryError, normalize_scope_pattern


MAX_SCOPE_PATTERNS = 100
MAX_SCOPE_VIOLATIONS = 100
MAX_SCOPE_PATHS_RETURNED = 500


@dataclass(frozen=True)
class ScopeContext:
    changes: tuple[GitFileChange, ...]


@dataclass(frozen=True)
class AllowedScopeRule:
    patterns: tuple[str, ...]
    exceptions: tuple[str, ...]
    id: str = "AA-SCOPE-001"
    category: str = "scope"
    description: str = "Every changed path endpoint must match the declared allowed scope."
    deterministic: bool = True

    def evaluate(self, context: ScopeContext) -> tuple[Finding, ...]:
        if not self.patterns:
            return ()
        violations: list[Evidence] = []
        for change in context.changes:
            for endpoint in change.endpoints():
                if not _matches_any(endpoint, self.patterns) or _matches_any(endpoint, self.exceptions):
                    violations.append(
                        Evidence(
                            EvidenceKind.FACT,
                            "Git path and scope declaration",
                            {
                                "path": endpoint,
                                "change_status": change.status,
                                "allowed": list(self.patterns),
                                "exceptions": list(self.exceptions),
                            },
                        )
                    )
        if not violations:
            return ()
        returned = tuple(violations[:MAX_SCOPE_VIOLATIONS])
        return (
            Finding(
                id=self.id,
                category=self.category,
                severity=Severity.HIGH,
                confidence=Confidence.HIGH,
                message=f"{len(violations)} changed path endpoint(s) are outside the allowed scope.",
                evidence=returned,
                location={"path": returned[0].payload["path"]},
                suggestion="Revert the out-of-scope change or explicitly amend the allowed scope.",
            ),
        )


@dataclass(frozen=True)
class DeniedScopeRule:
    patterns: tuple[str, ...]
    id: str = "AA-SCOPE-002"
    category: str = "scope"
    description: str = "No changed path endpoint may match an explicit deny pattern."
    deterministic: bool = True

    def evaluate(self, context: ScopeContext) -> tuple[Finding, ...]:
        violations: list[Evidence] = []
        for change in context.changes:
            for endpoint in change.endpoints():
                if _matches_any(endpoint, self.patterns):
                    violations.append(
                        Evidence(
                            EvidenceKind.FACT,
                            "Git path and scope declaration",
                            {
                                "path": endpoint,
                                "change_status": change.status,
                                "denied": list(self.patterns),
                            },
                        )
                    )
        if not violations:
            return ()
        returned = tuple(violations[:MAX_SCOPE_VIOLATIONS])
        return (
            Finding(
                id=self.id,
                category=self.category,
                severity=Severity.HIGH,
                confidence=Confidence.HIGH,
                message=f"{len(violations)} changed path endpoint(s) match an explicit deny rule.",
                evidence=returned,
                location={"path": returned[0].payload["path"]},
                suggestion="Remove the denied change; deny rules take precedence over allowed scope.",
            ),
        )


class ScopeVerifier:
    def __init__(self, git_inspector: GitInspector) -> None:
        self.git_inspector = git_inspector

    def verify(
        self,
        *,
        allowed: Iterable[str] = (),
        denied: Iterable[str] = (),
        exceptions: Iterable[str] = (),
        mode: DiffMode = "combined",
    ) -> CheckResult:
        try:
            allowed_patterns = _normalize_patterns(allowed)
            denied_patterns = _normalize_patterns(denied)
            exception_patterns = _normalize_patterns(exceptions)
            snapshot = self.git_inspector.snapshot(mode)
        except (PathBoundaryError, RuntimeError, ValueError) as exc:
            return CheckResult(
                status=CheckStatus.ERROR,
                summary="Change scope could not be verified.",
                errors=(CheckError("AA-SCOPE-INPUT", str(exc)),),
            )

        context = ScopeContext(snapshot.files)
        rules = (
            DeniedScopeRule(denied_patterns),
            AllowedScopeRule(allowed_patterns, exception_patterns),
        )
        findings = tuple(finding for rule in rules for finding in rule.evaluate(context))
        violating_set = {
            endpoint
            for change in snapshot.files
            for endpoint in change.endpoints()
            if _matches_any(endpoint, denied_patterns)
            or (
                bool(allowed_patterns)
                and (
                    not _matches_any(endpoint, allowed_patterns)
                    or _matches_any(endpoint, exception_patterns)
                )
            )
        }
        violating_paths = sorted(violating_set)
        authorized = sorted({
            change.path
            for change in snapshot.files
            if not any(endpoint in violating_set for endpoint in change.endpoints())
        })
        output_truncated = (
            len(violating_paths) > MAX_SCOPE_PATHS_RETURNED
            or len(authorized) > MAX_SCOPE_PATHS_RETURNED
            or len(snapshot.files) > MAX_SCOPE_PATHS_RETURNED
            or len(violating_paths) > MAX_SCOPE_VIOLATIONS
        )
        evidence = Evidence(
            EvidenceKind.FACT,
            "Git diff and normalized scope declaration",
            {
                "mode": mode,
                "changed_files": len(snapshot.files),
                "allowed": list(allowed_patterns),
                "denied": list(denied_patterns),
                "exceptions": list(exception_patterns),
            },
        )
        return CheckResult(
            status=CheckStatus.FAIL if findings else CheckStatus.PASS,
            summary=(
                f"Scope verification found {len(violating_paths)} violating path endpoint(s)."
                if findings
                else f"All {len(snapshot.files)} changed file(s) satisfy the declared scope."
            ),
            findings=findings,
            evidence=(evidence,),
            metadata={
                "mode": mode,
                "authorized": authorized[:MAX_SCOPE_PATHS_RETURNED],
                "violations": violating_paths[:MAX_SCOPE_PATHS_RETURNED],
                "violation_count": len(violating_paths),
                "changed": [
                    change.to_dict() for change in snapshot.files[:MAX_SCOPE_PATHS_RETURNED]
                ],
                "scope": {
                    "allowed": list(allowed_patterns),
                    "denied": list(denied_patterns),
                    "exceptions": list(exception_patterns),
                    "deny_precedence": True,
                    "rename_policy": "both source and destination are evaluated",
                },
                "limits": {
                    "max_patterns_per_list": MAX_SCOPE_PATTERNS,
                    "max_violation_evidence": MAX_SCOPE_VIOLATIONS,
                    "max_paths_returned": MAX_SCOPE_PATHS_RETURNED,
                    "truncated": output_truncated,
                },
            },
        )


def _normalize_patterns(patterns: Iterable[str]) -> tuple[str, ...]:
    values = tuple(dict.fromkeys(normalize_scope_pattern(str(pattern)) for pattern in patterns))
    if len(values) > MAX_SCOPE_PATTERNS:
        raise ValueError(f"scope accepts at most {MAX_SCOPE_PATTERNS} patterns per list")
    try:
        for value in values:
            _glob_regex(value)
    except re.error as exc:
        raise ValueError(f"invalid scope glob: {exc}") from exc
    return values


def _matches_any(path: str, patterns: tuple[str, ...]) -> bool:
    return any(_glob_regex(pattern).fullmatch(path) is not None for pattern in patterns)


def _glob_regex(pattern: str) -> re.Pattern[str]:
    if not any(character in pattern for character in "*?["):
        return re.compile(rf"{re.escape(pattern)}(?:/.*)?")
    output = ""
    index = 0
    while index < len(pattern):
        character = pattern[index]
        if character == "*":
            if index + 1 < len(pattern) and pattern[index + 1] == "*":
                index += 1
                if index + 1 < len(pattern) and pattern[index + 1] == "/":
                    index += 1
                    output += "(?:.*/)?"
                else:
                    output += ".*"
            else:
                output += "[^/]*"
        elif character == "?":
            output += "[^/]"
        elif character == "[":
            closing = pattern.find("]", index + 1)
            if closing == -1:
                output += re.escape(character)
            else:
                content = pattern[index + 1 : closing]
                if content.startswith("!"):
                    content = "^" + content[1:]
                output += "[" + content.replace("\\", "\\\\") + "]"
                index = closing
        else:
            output += re.escape(character)
        index += 1
    return re.compile(output)
