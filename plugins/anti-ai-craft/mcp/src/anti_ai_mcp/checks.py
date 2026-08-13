from __future__ import annotations

import json
import math
import os
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

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
from .execution import CommandExecution, CommandSpec, run_command
from .paths import PathBoundaryError, resolve_within_repository


CHECK_CATEGORIES = (
    "lint",
    "typecheck",
    "format-check",
    "build",
    "unit-tests",
    "integration-tests",
    "plugin-validation",
)
MAX_CHECKS = 100
MAX_EXECUTED_CHECKS = 20
MAX_MANIFEST_BYTES = 1024 * 1024
MAX_PROCESS_OUTPUT_BYTES = 128 * 1024
MAX_TIMEOUT_SECONDS = 600.0
EXCLUDED_DIRECTORIES = {".git", ".venv", "__pycache__", "graphify-out", "node_modules"}


@dataclass(frozen=True)
class ProjectCheck:
    id: str
    category: str
    command: tuple[str, ...]
    cwd: Path
    source: str
    runner: str

    def command_spec(self) -> CommandSpec:
        return CommandSpec(self.command, self.cwd, self.category, self.source)

    def to_dict(self, repository_root: Path) -> dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "command": list(self.command),
            "cwd": self.cwd.relative_to(repository_root).as_posix() or ".",
            "source": self.source,
            "runner": self.runner,
        }


class ProjectCheckService:
    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root.resolve(strict=True)

    def discover(self) -> tuple[ProjectCheck, ...]:
        checks: list[ProjectCheck] = []
        for manifest in self._manifests():
            if manifest.name == "package.json":
                checks.extend(self._node_checks(manifest))
            elif manifest.name == "pyproject.toml":
                checks.extend(self._python_checks(manifest))
            if len(checks) >= MAX_CHECKS:
                break
        unique = {check.id: check for check in checks}
        return tuple(sorted(unique.values(), key=lambda check: (check.category, check.id))[:MAX_CHECKS])

    def capabilities(self) -> dict[str, Any]:
        checks = self.discover()
        by_category = {
            category: [
                check.to_dict(self.repository_root)
                for check in checks
                if check.category == category
            ]
            for category in CHECK_CATEGORIES
        }
        return {
            "checks": [check.to_dict(self.repository_root) for check in checks],
            "categories": by_category,
            "trust_boundary": (
                "Commands are generated from recognized manifest keys and fixed runner argv. "
                "The MCP never accepts an arbitrary command. Project-owned scripts may execute "
                "repository code and should be reviewed before use."
            ),
            "limits": {
                "max_checks": MAX_CHECKS,
                "max_checks_per_execution": MAX_EXECUTED_CHECKS,
                "max_timeout_seconds": MAX_TIMEOUT_SECONDS,
                "stdout_bytes": MAX_PROCESS_OUTPUT_BYTES,
                "stderr_bytes": MAX_PROCESS_OUTPUT_BYTES,
                "truncated": len(checks) >= MAX_CHECKS,
            },
        }

    def run(
        self,
        *,
        categories: Iterable[str] = (),
        dry_run: bool = False,
        timeout_seconds: float = 120.0,
    ) -> CheckResult:
        validation_error = self._validate_execution_input(categories, timeout_seconds)
        if validation_error:
            return validation_error
        requested = tuple(dict.fromkeys(str(category) for category in categories))
        checks = tuple(
            check
            for check in self.discover()
            if not requested or check.category in requested
        )
        if not checks:
            evidence = Evidence(
                EvidenceKind.FACT,
                "project manifests",
                {"requested_categories": list(requested), "discovered_checks": 0},
            )
            return CheckResult(
                status=CheckStatus.NOT_APPLICABLE,
                summary="No configured validation check matches the request.",
                findings=(
                    Finding(
                        id="AA-VAL-005",
                        category="validation",
                        severity=Severity.INFO,
                        confidence=Confidence.HIGH,
                        message="No recognized project validation command was discovered.",
                        evidence=(evidence,),
                        suggestion="Register a validation script in a supported project manifest.",
                    ),
                ),
                evidence=(evidence,),
                metadata={"dry_run": dry_run, "selected_checks": [], "executions": []},
            )
        if not dry_run and len(checks) > MAX_EXECUTED_CHECKS:
            evidence = Evidence(
                EvidenceKind.MANUAL_REVIEW_REQUIRED,
                "validation selection limit",
                {"selected_checks": len(checks), "maximum": MAX_EXECUTED_CHECKS},
            )
            return CheckResult(
                status=CheckStatus.MANUAL_REVIEW_REQUIRED,
                summary="The validation selection exceeds the bounded execution limit.",
                findings=(
                    Finding(
                        id="AA-VAL-006",
                        category="validation",
                        severity=Severity.MEDIUM,
                        confidence=Confidence.HIGH,
                        message=f"{len(checks)} checks were selected; at most {MAX_EXECUTED_CHECKS} run in one call.",
                        evidence=(evidence,),
                        suggestion="Narrow the validation categories and run separate bounded calls.",
                    ),
                ),
                evidence=(evidence,),
                metadata={
                    "dry_run": False,
                    "selected_checks": [
                        check.to_dict(self.repository_root) for check in checks[:MAX_CHECKS]
                    ],
                    "executions": [],
                },
            )
        if dry_run:
            return CheckResult(
                status=CheckStatus.PASS,
                summary=f"Dry run selected {len(checks)} validation check(s); nothing executed.",
                evidence=(
                    Evidence(
                        EvidenceKind.FACT,
                        "project manifests",
                        {"selected_check_ids": [check.id for check in checks]},
                    ),
                ),
                metadata={
                    "dry_run": True,
                    "selected_checks": [check.to_dict(self.repository_root) for check in checks],
                    "executions": [],
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
            for check in checks
        )
        return result_from_executions(
            checks,
            executions,
            dry_run=False,
            id_prefix="AA-VAL",
            noun="validation",
            repository_root=self.repository_root,
        )

    def _validate_execution_input(
        self, categories: Iterable[str], timeout_seconds: float
    ) -> CheckResult | None:
        requested = tuple(str(category) for category in categories)
        unknown = sorted(set(requested) - set(CHECK_CATEGORIES))
        if unknown:
            return CheckResult(
                status=CheckStatus.ERROR,
                summary="Validation categories are invalid.",
                errors=(CheckError("AA-VAL-INPUT", f"unsupported categories: {unknown}"),),
            )
        if not math.isfinite(timeout_seconds) or timeout_seconds <= 0 or timeout_seconds > MAX_TIMEOUT_SECONDS:
            return CheckResult(
                status=CheckStatus.ERROR,
                summary="Validation timeout is outside the allowed range.",
                errors=(
                    CheckError(
                        "AA-VAL-INPUT",
                        f"timeout_seconds must be greater than 0 and at most {MAX_TIMEOUT_SECONDS}",
                    ),
                ),
            )
        return None

    def _manifests(self) -> list[Path]:
        manifests: list[Path] = []
        for current, directories, names in os.walk(self.repository_root):
            directories[:] = sorted(name for name in directories if name not in EXCLUDED_DIRECTORIES)
            for name in ("package.json", "pyproject.toml"):
                if name in names:
                    candidate = Path(current) / name
                    try:
                        resolve_within_repository(self.repository_root, candidate)
                    except PathBoundaryError:
                        continue
                    manifests.append(candidate)
        return sorted(manifests)

    def _node_checks(self, manifest: Path) -> list[ProjectCheck]:
        payload = _load_json(manifest)
        if payload is None:
            return []
        scripts = payload.get("scripts", {})
        if not isinstance(scripts, dict):
            return []
        manager = _node_manager(manifest.parent)
        categories = {
            "lint": ("lint",),
            "typecheck": ("typecheck", "type-check", "check-types"),
            "format-check": ("format:check", "format-check", "check-format"),
            "build": ("build",),
            "unit-tests": ("test:unit", "unit", "test"),
            "integration-tests": ("test:integration", "integration"),
            "plugin-validation": ("plugin:validate", "validate:plugin"),
        }
        relative_manifest = manifest.relative_to(self.repository_root).as_posix()
        checks: list[ProjectCheck] = []
        consumed: set[str] = set()
        for category, candidates in categories.items():
            name = next((candidate for candidate in candidates if candidate in scripts and candidate not in consumed), None)
            if name is None:
                continue
            consumed.add(name)
            command = (manager, "run", name)
            checks.append(
                ProjectCheck(
                    id=_check_id(category, relative_manifest, name),
                    category=category,
                    command=command,
                    cwd=manifest.parent,
                    source=f"{relative_manifest} scripts.{name}",
                    runner=manager,
                )
            )
        return checks

    def _python_checks(self, manifest: Path) -> list[ProjectCheck]:
        payload = _load_toml(manifest)
        if payload is None:
            return []
        dependencies = _python_dependencies(payload)
        tools = payload.get("tool", {}) if isinstance(payload.get("tool", {}), dict) else {}
        relative_manifest = manifest.relative_to(self.repository_root).as_posix()
        checks: list[ProjectCheck] = []

        def add(category: str, name: str, argv: tuple[str, ...], runner: str) -> None:
            checks.append(
                ProjectCheck(
                    id=_check_id(category, relative_manifest, name),
                    category=category,
                    command=argv,
                    cwd=manifest.parent,
                    source=f"{relative_manifest} ({name} detected)",
                    runner=runner,
                )
            )

        if "ruff" in dependencies or "ruff" in tools:
            add("lint", "ruff", (sys.executable, "-m", "ruff", "check", "."), "ruff")
            add("format-check", "ruff-format", (sys.executable, "-m", "ruff", "format", "--check", "."), "ruff")
        if "mypy" in dependencies or "mypy" in tools:
            add("typecheck", "mypy", (sys.executable, "-m", "mypy", "."), "mypy")
        elif "pyright" in dependencies or "pyright" in tools:
            add("typecheck", "pyright", (sys.executable, "-m", "pyright"), "pyright")
        if "build" in dependencies:
            add("build", "build", (sys.executable, "-m", "build"), "build")
        if "pytest" in dependencies or "pytest" in tools:
            add("unit-tests", "pytest", (sys.executable, "-m", "pytest"), "pytest")
        return checks


def result_from_executions(
    checks: tuple[ProjectCheck, ...],
    executions: tuple[CommandExecution, ...],
    *,
    dry_run: bool,
    id_prefix: str,
    noun: str,
    repository_root: Path,
) -> CheckResult:
    evidence = tuple(
        Evidence(
            EvidenceKind.FACT,
            "bounded subprocess execution",
            execution.to_dict(),
        )
        for execution in executions
    )
    findings: list[Finding] = []
    errors: list[CheckError] = []
    failed = [item for item in executions if item.exit_code not in (None, 0) and not item.timed_out]
    unavailable = [item for item in executions if item.unavailable or item.error]
    timed_out = [item for item in executions if item.timed_out]
    truncated = [item for item in executions if item.truncated]
    if failed:
        findings.append(
            Finding(
                id=f"{id_prefix}-001",
                category=noun,
                severity=Severity.HIGH,
                confidence=Confidence.HIGH,
                message=f"{len(failed)} {noun} command(s) exited unsuccessfully.",
                evidence=tuple(evidence[index] for index, item in enumerate(executions) if item in failed),
                suggestion="Inspect the bounded stdout/stderr summaries and fix the reported project failure.",
            )
        )
    if unavailable:
        findings.append(
            Finding(
                id=f"{id_prefix}-002",
                category=noun,
                severity=Severity.MEDIUM,
                confidence=Confidence.HIGH,
                message=f"{len(unavailable)} {noun} command(s) could not be started.",
                evidence=tuple(evidence[index] for index, item in enumerate(executions) if item in unavailable),
                suggestion="Install the declared runner or repair the project environment.",
            )
        )
        errors.extend(CheckError(f"{id_prefix}-EXEC", item.error or "command unavailable") for item in unavailable)
    if timed_out:
        findings.append(
            Finding(
                id=f"{id_prefix}-003",
                category=noun,
                severity=Severity.MEDIUM,
                confidence=Confidence.HIGH,
                message=f"{len(timed_out)} {noun} command(s) exceeded the timeout and were terminated.",
                evidence=tuple(evidence[index] for index, item in enumerate(executions) if item in timed_out),
                suggestion="Investigate a slow or stuck check before increasing the bounded timeout.",
            )
        )
    if truncated:
        findings.append(
            Finding(
                id=f"{id_prefix}-004" if id_prefix == "AA-VAL" else "AA-TEST-006",
                category=noun,
                severity=Severity.LOW,
                confidence=Confidence.HIGH,
                message=f"{len(truncated)} {noun} command output(s) reached an explicit byte limit.",
                evidence=tuple(evidence[index] for index, item in enumerate(executions) if item in truncated),
                suggestion="Run the failing check directly when the omitted output is needed.",
            )
        )
    if unavailable:
        status = CheckStatus.ERROR
    elif failed or timed_out:
        status = CheckStatus.FAIL
    elif truncated:
        status = CheckStatus.WARNING
    else:
        status = CheckStatus.PASS
    passed = sum(item.status == "PASS" for item in executions)
    return CheckResult(
        status=status,
        summary=f"Executed {len(executions)} {noun} command(s): {passed} passed.",
        findings=tuple(findings),
        evidence=evidence,
        metadata={
            "dry_run": dry_run,
            "selected_checks": [check.to_dict(repository_root) for check in checks],
            "executions": [execution.to_dict() for execution in executions],
            "limits": {
                "stdout_bytes": MAX_PROCESS_OUTPUT_BYTES,
                "stderr_bytes": MAX_PROCESS_OUTPUT_BYTES,
                "max_timeout_seconds": MAX_TIMEOUT_SECONDS,
                "max_checks_per_execution": MAX_EXECUTED_CHECKS,
                "truncated": bool(truncated),
            },
        },
        errors=tuple(errors),
    )


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        if path.stat().st_size > MAX_MANIFEST_BYTES:
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _load_toml(path: Path) -> dict[str, Any] | None:
    try:
        if path.stat().st_size > MAX_MANIFEST_BYTES:
            return None
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return None


def _python_dependencies(payload: dict[str, Any]) -> set[str]:
    values: list[Any] = []
    project = payload.get("project", {})
    if isinstance(project, dict) and isinstance(project.get("dependencies"), list):
        values.extend(project["dependencies"])
    groups = payload.get("dependency-groups", {})
    if isinstance(groups, dict):
        for group in groups.values():
            if isinstance(group, list):
                values.extend(group)
    result = set()
    for value in values:
        match = re.match(r"[A-Za-z0-9_.-]+", str(value).strip())
        if match:
            result.add(match.group(0).lower().replace("_", "-"))
    return result


def _node_manager(directory: Path) -> str:
    if (directory / "pnpm-lock.yaml").is_file():
        return "pnpm"
    if (directory / "yarn.lock").is_file():
        return "yarn"
    if (directory / "bun.lock").is_file() or (directory / "bun.lockb").is_file():
        return "bun"
    return "npm"


def _check_id(category: str, manifest: str, name: str) -> str:
    raw = f"{category}-{manifest}-{name}".lower()
    return re.sub(r"[^a-z0-9]+", "-", raw).strip("-")
