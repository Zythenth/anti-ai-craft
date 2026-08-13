from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any

from .checks import (
    EXCLUDED_DIRECTORIES,
    MAX_EXECUTED_CHECKS,
    MAX_PROCESS_OUTPUT_BYTES,
    MAX_TIMEOUT_SECONDS,
    ProjectCheck,
    ProjectCheckService,
    result_from_executions,
)
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
from .execution import run_command
from .git import DiffMode, GitInspector
from .graph import GraphProvider
from .graph_evidence import GraphEvidenceNormalizer
from .impact import GraphImpactAnalyzer
from .paths import PathBoundaryError, normalize_repository_path


MAX_TEST_FILES = 5_000
MAX_SELECTED_TEST_PATHS = 200
MAX_SELECTION_REASONS = 500


class RelevantTestService:
    def __init__(
        self,
        repository_root: Path,
        git_inspector: GitInspector,
        check_service: ProjectCheckService,
        graph_provider: GraphProvider | None = None,
    ) -> None:
        self.repository_root = repository_root.resolve(strict=True)
        self.git_inspector = git_inspector
        self.check_service = check_service
        self.graph_provider = graph_provider
        self.impact_analyzer = GraphImpactAnalyzer(graph_provider) if graph_provider else None

    def run(
        self,
        *,
        mode: DiffMode = "combined",
        dry_run: bool = False,
        timeout_seconds: float = 120.0,
    ) -> CheckResult:
        if mode not in ("working_tree", "staged", "combined"):
            return CheckResult(
                status=CheckStatus.ERROR,
                summary="Relevant-test Git mode is invalid.",
                errors=(CheckError("AA-TEST-INPUT", f"unsupported diff mode: {mode}"),),
            )
        if not math.isfinite(timeout_seconds) or timeout_seconds <= 0 or timeout_seconds > MAX_TIMEOUT_SECONDS:
            return CheckResult(
                status=CheckStatus.ERROR,
                summary="Relevant-test timeout is outside the allowed range.",
                errors=(
                    CheckError(
                        "AA-TEST-INPUT",
                        f"timeout_seconds must be greater than 0 and at most {MAX_TIMEOUT_SECONDS}",
                    ),
                ),
            )
        try:
            snapshot = self.git_inspector.snapshot(mode)
        except (RuntimeError, PathBoundaryError, ValueError) as exc:
            return CheckResult(
                status=CheckStatus.ERROR,
                summary="Relevant tests could not be selected because Git inspection failed.",
                errors=(CheckError("AA-TEST-GIT", str(exc)),),
            )
        changes = tuple(change for change in snapshot.files if change.status != "deleted")
        if not changes:
            graph_metadata = None
            if self.graph_provider is not None:
                normalizer = GraphEvidenceNormalizer(self.graph_provider.get_status())
                graph_metadata = normalizer.graph_metadata(
                    coverage={"changed_files": 0, "matched_files": 0}
                )
                graph_metadata["warnings"] = normalizer.warnings()
            return CheckResult(
                status=CheckStatus.NOT_APPLICABLE,
                summary="No changed files require relevant-test selection.",
                evidence=(Evidence(EvidenceKind.FACT, "git diff", {"mode": mode, "changed_files": 0}),),
                metadata={
                    "dry_run": dry_run,
                    "selection_reason": [],
                    "executions": [],
                    "graph": graph_metadata,
                    "graph_added_tests": [],
                },
            )
        test_checks = tuple(
            check for check in self.check_service.discover() if check.category == "unit-tests"
        )
        selections, reasons, unmapped = self._select_direct(changes, test_checks)
        graph_metadata: dict[str, Any] | None = None
        graph_added_tests: list[str] = []
        graph_duplicate_tests = 0
        graph_non_fresh = False
        if self.graph_provider is not None and self.impact_analyzer is not None:
            graph_status = self.graph_provider.get_status()
            normalizer = GraphEvidenceNormalizer(graph_status)
            graph_non_fresh = normalizer.non_fresh
            impact = self.impact_analyzer.analyze(
                (change.path for change in changes),
                max_depth=2,
                include_tests=True,
                graph_status=graph_status,
            )
            graph_metadata = normalizer.graph_metadata(
                truncated=impact.truncated,
                coverage=impact.coverage,
            )
            graph_metadata["warnings"] = list(impact.warnings)
            if normalizer.usable:
                mutable = {check: set(paths) for check, paths in selections.items()}
                for candidate in impact.candidate_tests:
                    test_path = normalize_repository_path(candidate["test_path"])
                    owner = _closest_check(test_path, test_checks, self.repository_root)
                    if owner is None or owner.runner != "pytest":
                        continue
                    relative = Path(test_path).relative_to(
                        owner.cwd.relative_to(self.repository_root)
                    ).as_posix()
                    selected = mutable.setdefault(owner, set())
                    if relative in selected:
                        graph_duplicate_tests += 1
                        continue
                    selected.add(relative)
                    graph_added_tests.append(test_path)
                    reasons.append(
                        {
                            "changed_path": None,
                            "test_path": relative,
                            "reason": candidate["selection_reason"],
                            "provenance": candidate["evidence_kind"],
                            "source": "Graphify structural impact",
                            "graph_distance": candidate["graph_distance"],
                            "freshness": graph_status.freshness.value,
                            "confidence": candidate["confidence"],
                            "path": candidate["path"],
                        }
                    )
                selections = {
                    check: tuple(sorted(paths)) for check, paths in mutable.items()
                }
        selection_truncated = False
        used_fallback = False
        if unmapped and test_checks:
            selections = {check: () for check in test_checks}
            used_fallback = True
            available_reason_slots = max(0, MAX_SELECTION_REASONS - len(reasons))
            reasons.extend(
                {
                    "changed_path": path,
                    "test_path": None,
                    "reason": "No direct deterministic mapping found; selected the configured package test suite.",
                    "provenance": EvidenceKind.HEURISTIC.value,
                }
                for path in unmapped[:available_reason_slots]
            )
            selection_truncated = len(unmapped) > available_reason_slots
        elif not selections and test_checks:
            selections = {check: () for check in test_checks}
            used_fallback = True
            reasons = [
                {
                    "changed_path": None,
                    "test_path": None,
                    "reason": "No direct deterministic mapping found; selected the configured package test suite.",
                    "provenance": EvidenceKind.HEURISTIC.value,
                }
            ]
        if not selections:
            evidence = Evidence(
                EvidenceKind.MANUAL_REVIEW_REQUIRED,
                "deterministic test mapping",
                {
                    "changed_paths": [
                        change.path for change in changes[:MAX_SELECTION_REASONS]
                    ],
                    "truncated": len(changes) > MAX_SELECTION_REASONS,
                },
            )
            return CheckResult(
                status=CheckStatus.MANUAL_REVIEW_REQUIRED,
                summary="No direct test mapping or configured fallback suite was found.",
                findings=(
                    Finding(
                        id="AA-TEST-004",
                        category="tests",
                        severity=Severity.MEDIUM,
                        confidence=Confidence.HIGH,
                        message="Relevant tests cannot be selected deterministically.",
                        evidence=(evidence,),
                        suggestion="Select tests manually or register a package test suite.",
                    ),
                ),
                evidence=(evidence,),
                metadata={
                    "dry_run": dry_run,
                    "selection_reason": reasons[:MAX_SELECTION_REASONS],
                    "executions": [],
                    "graph": graph_metadata,
                    "graph_added_tests": sorted(graph_added_tests),
                    "limits": {
                        "max_selection_reasons": MAX_SELECTION_REASONS,
                        "truncated": len(changes) > MAX_SELECTION_REASONS,
                    },
                },
            )

        selected_checks = tuple(
            _check_with_test_paths(check, paths) for check, paths in selections.items()
        )
        selection_evidence = tuple(
            Evidence(
                EvidenceKind(reason["provenance"]),
                reason.get("source", "deterministic test selection"),
                reason,
            )
            for reason in reasons
        )
        fallback_finding: tuple[Finding, ...] = ()
        base_status = CheckStatus.PASS
        if used_fallback:
            base_status = CheckStatus.WARNING
            fallback_finding = (
                Finding(
                    id="AA-TEST-005",
                    category="tests",
                    severity=Severity.INFO,
                    confidence=Confidence.HIGH,
                    message="A configured package suite was selected because no direct mapping was found.",
                    evidence=selection_evidence,
                ),
            )
        graph_finding: tuple[Finding, ...] = ()
        if graph_metadata is not None and graph_non_fresh:
            graph_evidence = Evidence(
                EvidenceKind.MANUAL_REVIEW_REQUIRED,
                "graph provider status",
                graph_metadata,
            )
            graph_finding = (
                Finding(
                    id="AA-TEST-008",
                    category="tests",
                    severity=Severity.INFO,
                    confidence=Confidence.HIGH,
                    message="Graph-aware test additions use non-fresh structural evidence.",
                    evidence=(graph_evidence,),
                    suggestion="Keep deterministic selections and review graph-only candidates before relying on them.",
                ),
            )
            if base_status is CheckStatus.PASS:
                base_status = CheckStatus.WARNING
        if dry_run:
            return CheckResult(
                status=base_status,
                summary=f"Dry run selected {len(selected_checks)} relevant test command(s); nothing executed.",
                findings=fallback_finding + graph_finding,
                evidence=selection_evidence,
                metadata={
                    "dry_run": True,
                    "selection_reason": reasons,
                    "selected_checks": [
                        check.to_dict(self.repository_root) for check in selected_checks
                    ],
                    "executions": [],
                    "graph": graph_metadata,
                    "graph_added_tests": sorted(graph_added_tests),
                    "graph_duplicate_candidates": graph_duplicate_tests,
                    "limits": {
                        "max_selection_reasons": MAX_SELECTION_REASONS,
                        "max_selected_test_paths": MAX_SELECTED_TEST_PATHS,
                        "truncated": selection_truncated,
                    },
                },
            )
        if len(selected_checks) > MAX_EXECUTED_CHECKS:
            evidence = Evidence(
                EvidenceKind.MANUAL_REVIEW_REQUIRED,
                "test execution limit",
                {"selected_checks": len(selected_checks), "maximum": MAX_EXECUTED_CHECKS},
            )
            return CheckResult(
                status=CheckStatus.MANUAL_REVIEW_REQUIRED,
                summary="The relevant-test selection exceeds the bounded execution limit.",
                findings=(
                    Finding(
                        id="AA-TEST-007",
                        category="tests",
                        severity=Severity.MEDIUM,
                        confidence=Confidence.HIGH,
                        message=(
                            f"{len(selected_checks)} test commands were selected; at most "
                            f"{MAX_EXECUTED_CHECKS} run in one call."
                        ),
                        evidence=(evidence,),
                        suggestion="Run package suites in separate bounded calls.",
                    ),
                ),
                evidence=selection_evidence + (evidence,),
                metadata={
                    "dry_run": False,
                    "selection_reason": reasons,
                    "selected_checks": [
                        check.to_dict(self.repository_root) for check in selected_checks[:MAX_CHECKS]
                    ],
                    "executions": [],
                    "graph": graph_metadata,
                    "graph_added_tests": sorted(graph_added_tests),
                    "graph_duplicate_candidates": graph_duplicate_tests,
                    "limits": {
                        "max_selection_reasons": MAX_SELECTION_REASONS,
                        "max_selected_test_paths": MAX_SELECTED_TEST_PATHS,
                        "truncated": selection_truncated,
                    },
                },
            )
        executions = tuple(
            run_command(
                self.repository_root,
                check.command_spec(),
                timeout_seconds=timeout_seconds,
                stdout_limit=MAX_PROCESS_OUTPUT_BYTES,
                stderr_limit=MAX_PROCESS_OUTPUT_BYTES,
            )
            for check in selected_checks
        )
        result = result_from_executions(
            selected_checks,
            executions,
            dry_run=False,
            id_prefix="AA-TEST",
            noun="test",
            repository_root=self.repository_root,
        )
        status = result.status
        if status is CheckStatus.PASS and (used_fallback or graph_non_fresh):
            status = CheckStatus.WARNING
        return CheckResult(
            status=status,
            summary=result.summary,
            findings=fallback_finding + graph_finding + result.findings,
            evidence=selection_evidence + result.evidence,
            metadata={
                **result.metadata,
                "selection_reason": reasons,
                "fallback_suite": used_fallback,
                "graph": graph_metadata,
                "graph_added_tests": sorted(graph_added_tests),
                "graph_duplicate_candidates": graph_duplicate_tests,
                "selection_limits": {
                    "max_selection_reasons": MAX_SELECTION_REASONS,
                    "max_selected_test_paths": MAX_SELECTED_TEST_PATHS,
                    "truncated": selection_truncated,
                },
            },
            errors=result.errors,
        )

    def _select_direct(
        self,
        changes,
        checks: tuple[ProjectCheck, ...],
    ) -> tuple[
        dict[ProjectCheck, tuple[str, ...]],
        list[dict[str, Any]],
        list[str],
    ]:
        selections: dict[ProjectCheck, set[str]] = {}
        reasons: list[dict[str, Any]] = []
        unmapped: list[str] = []
        test_files = self._test_files()
        for change in changes:
            changed_path = normalize_repository_path(change.path)
            owner = _closest_check(changed_path, checks, self.repository_root)
            if owner is None or owner.runner != "pytest":
                unmapped.append(changed_path)
                continue
            relative_to_owner = Path(changed_path).relative_to(owner.cwd.relative_to(self.repository_root)).as_posix()
            if _is_test_path(relative_to_owner):
                selections.setdefault(owner, set()).add(relative_to_owner)
                reasons.append(
                    {
                        "changed_path": changed_path,
                        "test_path": relative_to_owner,
                        "reason": "The changed file is itself a test file.",
                        "provenance": EvidenceKind.FACT.value,
                    }
                )
                continue
            candidates = _python_test_candidates(relative_to_owner, test_files.get(owner.cwd, ()))
            if not candidates:
                unmapped.append(changed_path)
            selected_count = sum(len(paths) for paths in selections.values())
            if selected_count + len(candidates) > MAX_SELECTED_TEST_PATHS:
                unmapped.append(changed_path)
                continue
            for candidate, reason in candidates:
                selections.setdefault(owner, set()).add(candidate)
                reasons.append(
                    {
                        "changed_path": changed_path,
                        "test_path": candidate,
                        "reason": reason,
                        "provenance": EvidenceKind.HEURISTIC.value,
                    }
                )
        return (
            {check: tuple(sorted(paths)) for check, paths in selections.items()},
            reasons,
            unmapped,
        )

    def _test_files(self) -> dict[Path, tuple[str, ...]]:
        result: dict[Path, tuple[str, ...]] = {}
        for check in self.check_service.discover():
            if check.category != "unit-tests" or check.runner != "pytest":
                continue
            paths: list[str] = []
            for current, directories, names in os.walk(check.cwd):
                directories[:] = sorted(name for name in directories if name not in EXCLUDED_DIRECTORIES)
                for name in sorted(names):
                    relative = (Path(current) / name).relative_to(check.cwd).as_posix()
                    if _is_test_path(relative):
                        paths.append(relative)
                        if len(paths) >= MAX_TEST_FILES:
                            break
                if len(paths) >= MAX_TEST_FILES:
                    break
            result[check.cwd] = tuple(paths)
        return result


def _closest_check(path: str, checks: tuple[ProjectCheck, ...], repository_root: Path) -> ProjectCheck | None:
    candidates = []
    absolute = repository_root / Path(path)
    for check in checks:
        try:
            absolute.relative_to(check.cwd)
        except ValueError:
            continue
        candidates.append(check)
    return max(candidates, key=lambda check: len(check.cwd.parts), default=None)


def _is_test_path(path: str) -> bool:
    name = _path_name(path)
    parts = path.lower().split("/")
    return (
        name.startswith("test_")
        or name.endswith("_test.py")
        or "tests" in parts
        or "test" in parts
    )


def _path_name(path: str) -> str:
    return path.rsplit("/", 1)[-1].lower()


def _python_test_candidates(source_path: str, test_files: tuple[str, ...]) -> list[tuple[str, str]]:
    source = source_path
    if source.startswith("src/"):
        source = source[4:]
    source_path_obj = Path(source)
    stem = source_path_obj.stem
    expected_name = f"test_{stem}.py"
    source_parent = source_path_obj.parent.as_posix()
    candidates: list[tuple[str, str]] = []
    for test_path in test_files:
        test_obj = Path(test_path)
        if test_obj.name != expected_name:
            continue
        test_parent = test_obj.parent.as_posix()
        normalized_parent = test_parent[6:] if test_parent.startswith("tests/") else test_parent
        if normalized_parent == source_parent:
            reason = "matching module path"
        elif normalized_parent.endswith(source_parent) or source_parent.endswith(normalized_parent):
            reason = "matching module directory"
        else:
            reason = "matching test module name"
        candidates.append((test_path, reason))
    return candidates


def _check_with_test_paths(check: ProjectCheck, paths: tuple[str, ...]) -> ProjectCheck:
    if not paths:
        return check
    if check.runner != "pytest":
        return check
    return ProjectCheck(
        id=check.id,
        category=check.category,
        command=(*check.command, *paths),
        cwd=check.cwd,
        source=check.source,
        runner=check.runner,
    )
