from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypeVar

from .anti_ai_audit import AntiAiAuditService
from .architecture import ArchitectureService
from .baseline import BaselineError, BaselineService
from .checks import ProjectCheckService
from .evidence import CheckResult, CheckStatus
from .git import GitInspector
from .impact import ChangeImpactService
from .remediation import RemediationService
from .repository import RepositoryInspector
from .relevant_tests import RelevantTestService
from .scope import ScopeVerifier
from .security_audit import SecurityAuditService
from .status import AntiAiStatusService


EVIDENCE_BUNDLE_SCHEMA_VERSION = "1.0"
_TIMED_RESULT = TypeVar("_TIMED_RESULT")


class EvidenceBundleService:
    def __init__(
        self,
        repository_root: Path,
        status_service: AntiAiStatusService,
        repository_inspector: RepositoryInspector,
        git_inspector: GitInspector,
        scope_verifier: ScopeVerifier,
        check_service: ProjectCheckService,
        relevant_test_service: RelevantTestService,
        impact_service: ChangeImpactService,
        architecture_service: ArchitectureService,
        anti_ai_audit: AntiAiAuditService,
        security_audit: SecurityAuditService,
        remediation_service: RemediationService,
        baseline_service: BaselineService,
    ) -> None:
        self.repository_root = repository_root.resolve(strict=True)
        self.status_service = status_service
        self.repository_inspector = repository_inspector
        self.git_inspector = git_inspector
        self.scope_verifier = scope_verifier
        self.check_service = check_service
        self.relevant_test_service = relevant_test_service
        self.impact_service = impact_service
        self.architecture_service = architecture_service
        self.anti_ai_audit = anti_ai_audit
        self.security_audit = security_audit
        self.remediation_service = remediation_service
        self.baseline_service = baseline_service

    def collect(
        self,
        *,
        allowed: list[str] | None = None,
        denied: list[str] | None = None,
        exceptions: list[str] | None = None,
        baseline_path: str | None = None,
        previous_findings: list[dict[str, Any]] | None = None,
        execute: bool = False,
        timeout_seconds: float = 120.0,
    ) -> dict[str, Any]:
        started = time.monotonic()
        timings: dict[str, float] = {}
        errors: list[dict[str, str]] = []
        state_before = _timed(timings, "git_state", self._state_signature)
        status = _timed(timings, "status", self.status_service.get_status)
        repository = _timed(timings, "repository", self.repository_inspector.inspect)
        git = _timed(timings, "git_diff", lambda: self.git_inspector.inspect("combined"))
        scope = _timed(
            timings,
            "scope",
            lambda: self.scope_verifier.verify(
                allowed=allowed or (),
                denied=denied or (),
                exceptions=exceptions or (),
                mode="combined",
            ),
        )
        validation_plan = _timed(
            timings,
            "validation_selection",
            lambda: self.check_service.run(dry_run=True, timeout_seconds=timeout_seconds),
        )
        test_plan = _timed(
            timings,
            "test_selection",
            lambda: self.relevant_test_service.run(
                dry_run=True, timeout_seconds=timeout_seconds
            ),
        )
        if execute:
            validation = _timed(
                timings,
                "validation_execution",
                lambda: self.check_service.run(
                    dry_run=False, timeout_seconds=timeout_seconds
                ),
            )
            state_after_validation = self._state_signature()
            if (
                state_after_validation == state_before
                and _same_selection(validation_plan, test_plan)
            ):
                tests = _reused_test_result(test_plan, validation)
                timings["relevant_tests_execution"] = 0.0
            else:
                tests = _timed(
                    timings,
                    "relevant_tests_execution",
                    lambda: self.relevant_test_service.run(
                        dry_run=False, timeout_seconds=timeout_seconds
                    ).to_dict(),
                )
        else:
            validation = validation_plan
            tests = test_plan.to_dict()

        impact = _timed(timings, "impact", self.impact_service.analyze)
        architecture_inspection = _timed(
            timings, "architecture_inspection", self.architecture_service.inspect
        )
        architecture_audit = _timed(
            timings, "architecture_audit", self.architecture_service.audit
        )
        anti_ai = _timed(timings, "anti_ai", self.anti_ai_audit.audit)
        security = _timed(timings, "security", self.security_audit.audit)
        remediation = (
            _timed(
                timings,
                "remediation",
                lambda: self.remediation_service.verify(previous_findings).to_dict(),
            )
            if previous_findings
            else None
        )
        current_findings = _unique_findings(
            [
                *scope.findings,
                *validation.findings,
                *anti_ai.findings,
                *security.findings,
            ]
        )
        baseline = None
        if baseline_path:
            try:
                baseline = _timed(
                    timings,
                    "baseline",
                    lambda: self.baseline_service.compare_document(
                        self.baseline_service.load(baseline_path),
                        [finding.to_dict() for finding in current_findings],
                    ),
                )
            except (BaselineError, OSError, ValueError) as exc:
                errors.append({"code": "BASELINE_INVALID", "message": str(exc)})

        sections: dict[str, Any] = {
            "repository": repository.to_dict(),
            "git": git.to_dict(),
            "scope": scope.to_dict(),
            "validation": validation.to_dict(),
            "tests": tests,
            "impact": impact.to_dict(),
            "architecture": {
                "inspection": architecture_inspection.to_dict(),
                "audit": architecture_audit.to_dict(),
            },
            "anti_ai": anti_ai.to_dict(),
            "security": security.to_dict(),
            "remediation": remediation,
            "baseline": baseline,
        }
        overall = _overall_status(sections, errors)
        if baseline and baseline.get("overall_status") == "REGRESSION":
            overall = "FAIL"
        warnings = _collect_warnings(sections)
        truncation = _collect_truncation(sections)
        return {
            "schema_version": EVIDENCE_BUNDLE_SCHEMA_VERSION,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "overall_status": overall,
            "summary": _summary(overall, current_findings, warnings, errors),
            "state_signature": state_before,
            "cache_policy": "no_cross_call_cache",
            "repository": sections["repository"],
            "git": sections["git"],
            "scope": sections["scope"],
            "validation": sections["validation"],
            "tests": sections["tests"],
            "graph": status["graph"],
            "impact": sections["impact"],
            "architecture": sections["architecture"],
            "anti_ai": sections["anti_ai"],
            "security": sections["security"],
            "remediation": remediation,
            "baseline": baseline,
            "warnings": warnings,
            "errors": errors,
            "truncation": truncation,
            "performance": {
                "phase_seconds": {
                    name: round(duration, 6) for name, duration in timings.items()
                },
                "total_seconds": round(time.monotonic() - started, 6),
            },
        }

    def _state_signature(self) -> str:
        snapshot = self.git_inspector.snapshot("combined")
        payload = {
            "head": snapshot.head,
            "files": [
                {
                    "path": change.path,
                    "old_path": change.old_path,
                    "status": change.status,
                    "lines_added": change.lines_added,
                    "lines_removed": change.lines_removed,
                }
                for change in snapshot.files
            ],
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _same_selection(validation: CheckResult, tests: CheckResult) -> bool:
    validation_items = validation.metadata.get("selected_checks", [])
    test_items = tests.metadata.get("selected_checks", [])
    if not validation_items or not test_items:
        return False
    return _selection_signatures(validation_items) == _selection_signatures(test_items)


def _selection_signatures(items: list[dict[str, Any]]) -> tuple[tuple[str, tuple[str, ...]], ...]:
    return tuple(
        sorted(
            (
                str(item.get("cwd") or "."),
                tuple(str(part) for part in item.get("command", [])),
            )
            for item in items
            if isinstance(item, dict)
        )
    )


def _reused_test_result(plan: CheckResult, validation: CheckResult) -> dict[str, Any]:
    result = plan.to_dict()
    validation_dict = validation.to_dict()
    if validation.status in {CheckStatus.ERROR, CheckStatus.FAIL}:
        result["status"] = validation.status.value
    result["summary"] = (
        "Relevant-test execution reused validation because command, arguments, cwd, "
        "and repository state were identical."
    )
    result["evidence"] = [*result["evidence"], *validation_dict["evidence"]]
    result["errors"] = validation_dict["errors"]
    result["metadata"] = {
        **result["metadata"],
        "executions": validation_dict["metadata"].get("executions", []),
        "execution_reused_from": "validation",
        "deduplicated_commands": len(
            validation_dict["metadata"].get("executions", [])
        ),
    }
    return result


def _unique_findings(findings) -> tuple:
    unique = {}
    for finding in findings:
        payload = finding.to_dict()
        key = json.dumps(
            {
                "id": payload["id"],
                "location": payload.get("location"),
                "evidence": payload.get("evidence"),
            },
            sort_keys=True,
        )
        unique.setdefault(key, finding)
    return tuple(unique.values())


def _overall_status(sections: dict[str, Any], errors: list[dict[str, str]]) -> str:
    if errors:
        return "FAIL"
    statuses = []
    for value in sections.values():
        if isinstance(value, dict) and isinstance(value.get("status"), str):
            statuses.append(value["status"])
        elif isinstance(value, dict):
            statuses.extend(
                item["status"]
                for item in value.values()
                if isinstance(item, dict) and isinstance(item.get("status"), str)
            )
    if any(status in {"ERROR", "FAIL"} for status in statuses):
        return "FAIL"
    if "MANUAL_REVIEW_REQUIRED" in statuses:
        return "MANUAL_REVIEW_REQUIRED"
    if "WARNING" in statuses:
        return "WARNING"
    return "PASS"


def _collect_warnings(sections: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    for value in sections.values():
        _append_warnings(value, warnings)
    return list(dict.fromkeys(warnings))


def _append_warnings(value: Any, warnings: list[str]) -> None:
    if not isinstance(value, dict):
        return
    metadata = value.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("warnings"), list):
        warnings.extend(str(item) for item in metadata["warnings"])
    for nested in value.values():
        if isinstance(nested, dict) and "status" in nested:
            _append_warnings(nested, warnings)


def _collect_truncation(sections: dict[str, Any]) -> dict[str, bool]:
    result: dict[str, bool] = {}
    for name, value in sections.items():
        result[name] = _is_truncated(value)
    return result


def _is_truncated(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    metadata = value.get("metadata", {})
    if isinstance(metadata, dict):
        limits = metadata.get("limits", {})
        if isinstance(limits, dict) and limits.get("truncated") is True:
            return True
        graph = metadata.get("graph", {})
        if isinstance(graph, dict) and graph.get("truncated") is True:
            return True
    return any(_is_truncated(item) for item in value.values() if isinstance(item, dict))


def _summary(
    overall: str,
    findings,
    warnings: list[str],
    errors: list[dict[str, str]],
) -> str:
    return (
        f"Evidence bundle status {overall}: {len(findings)} unique finding(s), "
        f"{len(warnings)} warning(s), and {len(errors)} error(s)."
    )


def _timed(
    timings: dict[str, float],
    name: str,
    operation: Callable[[], _TIMED_RESULT],
) -> _TIMED_RESULT:
    started = time.monotonic()
    try:
        return operation()
    finally:
        timings[name] = time.monotonic() - started
