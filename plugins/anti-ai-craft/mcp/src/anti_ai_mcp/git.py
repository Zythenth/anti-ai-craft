from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

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
from .execution import CommandSpec, run_command
from .paths import PathBoundaryError, normalize_repository_path, resolve_within_repository


DiffMode = Literal["working_tree", "staged", "combined"]
MAX_DIFF_FILES = 500
MAX_GIT_OUTPUT_BYTES = 2 * 1024 * 1024
MAX_UNTRACKED_FILE_BYTES = 1024 * 1024
MAX_ADDED_LINES = 2_000
MAX_REMOVED_LINES = 2_000


@dataclass
class GitFileChange:
    path: str
    status: str
    old_path: str | None = None
    lines_added: int | None = 0
    lines_removed: int | None = 0
    staged: bool = False
    unstaged: bool = False
    untracked: bool = False
    binary: bool = False
    truncated: bool = False

    def endpoints(self) -> tuple[str, ...]:
        return (self.old_path, self.path) if self.old_path else (self.path,)

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "old_path": self.old_path,
            "status": self.status,
            "lines_added": self.lines_added,
            "lines_removed": self.lines_removed,
            "staged": self.staged,
            "unstaged": self.unstaged,
            "untracked": self.untracked,
            "binary": self.binary,
            "truncated": self.truncated,
        }


@dataclass(frozen=True)
class GitDiffSnapshot:
    mode: DiffMode
    files: tuple[GitFileChange, ...] = ()
    branch: str | None = None
    head: str | None = None
    clean: bool = False
    truncated: bool = False


@dataclass(frozen=True)
class GitAddedLine:
    path: str
    line_number: int
    text: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "line_number": self.line_number,
            "text": self.text,
        }


@dataclass(frozen=True)
class GitRemovedLine:
    path: str
    line_number: int
    text: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "line_number": self.line_number,
            "text": self.text,
        }


class GitInspector:
    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root.resolve(strict=True)

    def inspect(self, mode: DiffMode = "combined") -> CheckResult:
        if mode not in ("working_tree", "staged", "combined"):
            return CheckResult(
                status=CheckStatus.ERROR,
                summary="Git diff mode is invalid.",
                errors=(CheckError("AA-GIT-INPUT", f"unsupported diff mode: {mode}"),),
            )
        try:
            snapshot = self.snapshot(mode)
        except (RuntimeError, PathBoundaryError, ValueError) as exc:
            evidence = Evidence(EvidenceKind.FACT, "git", {"error": str(exc)})
            return CheckResult(
                status=CheckStatus.ERROR,
                summary="Git changes could not be inspected.",
                findings=(
                    Finding(
                        id="AA-GIT-001",
                        category="git",
                        severity=Severity.MEDIUM,
                        confidence=Confidence.HIGH,
                        message=str(exc),
                        evidence=(evidence,),
                        suggestion="Verify that Git is available and the configured root is the repository root.",
                    ),
                ),
                evidence=(evidence,),
                errors=(CheckError("AA-GIT-EXEC", str(exc)),),
            )

        total_added = sum(change.lines_added or 0 for change in snapshot.files)
        total_removed = sum(change.lines_removed or 0 for change in snapshot.files)
        counts: dict[str, int] = {}
        for change in snapshot.files:
            counts[change.status] = counts.get(change.status, 0) + 1
        returned = snapshot.files[:MAX_DIFF_FILES]
        truncated = snapshot.truncated or len(snapshot.files) > MAX_DIFF_FILES
        evidence = Evidence(
            EvidenceKind.FACT,
            "git diff",
            {
                "mode": mode,
                "files_changed": len(snapshot.files),
                "lines_added": total_added,
                "lines_removed": total_removed,
            },
        )
        findings: tuple[Finding, ...] = ()
        status = CheckStatus.PASS
        if truncated:
            status = CheckStatus.WARNING
            findings = (
                Finding(
                    id="AA-GIT-002",
                    category="git",
                    severity=Severity.LOW,
                    confidence=Confidence.HIGH,
                    message="Git diff output was truncated at an explicit limit.",
                    evidence=(evidence,),
                    suggestion="Narrow the requested diff mode or inspect the repository directly.",
                ),
            )
        return CheckResult(
            status=status,
            summary=(
                "Working tree is clean for the requested mode."
                if snapshot.clean
                else f"Git reports {len(snapshot.files)} changed file(s)."
            ),
            findings=findings,
            evidence=(evidence,),
            metadata={
                "mode": mode,
                "branch": snapshot.branch,
                "head": snapshot.head,
                "clean": snapshot.clean,
                "files_changed": len(snapshot.files),
                "lines_added": total_added,
                "lines_removed": total_removed,
                "line_counts_complete": all(
                    change.lines_added is not None and change.lines_removed is not None
                    for change in snapshot.files
                ),
                "status": counts,
                "files": [change.to_dict() for change in returned],
                "diff_summary": {
                    "added": counts.get("added", 0),
                    "modified": counts.get("modified", 0),
                    "deleted": counts.get("deleted", 0),
                    "renamed": counts.get("renamed", 0),
                    "untracked": counts.get("untracked", 0),
                },
                "limits": {
                    "max_files_returned": MAX_DIFF_FILES,
                    "max_git_output_bytes": MAX_GIT_OUTPUT_BYTES,
                    "max_untracked_file_bytes": MAX_UNTRACKED_FILE_BYTES,
                    "truncated": truncated,
                },
            },
        )

    def snapshot(self, mode: DiffMode = "combined") -> GitDiffSnapshot:
        if mode not in ("working_tree", "staged", "combined"):
            raise ValueError(f"unsupported diff mode: {mode}")
        top_level = self._git("rev-parse", "--show-toplevel").strip()
        if not top_level:
            raise RuntimeError("configured root is not a Git repository")
        top_path = Path(top_level).resolve(strict=True)
        if top_path != self.repository_root:
            raise PathBoundaryError("Git top-level is outside the configured repository root")
        branch = self._git("branch", "--show-current").strip() or None
        head_result = self._git_optional("rev-parse", "HEAD")
        head = head_result.strip() or None

        if mode == "staged":
            changes = self._diff_records(cached=True)
            staged_paths = {change.path for change in changes}
            unstaged_paths: set[str] = set()
        elif mode == "working_tree":
            changes = self._diff_records(cached=False)
            staged_paths = set()
            unstaged_paths = {change.path for change in changes}
            changes.extend(self._untracked_records())
        else:
            changes = self._diff_records(head=True) if head else self._diff_records(cached=True)
            staged_paths = {change.path for change in self._diff_records(cached=True)}
            unstaged_paths = {change.path for change in self._diff_records(cached=False)}
            changes.extend(self._untracked_records())

        for change in changes:
            change.staged = change.path in staged_paths
            change.unstaged = change.path in unstaged_paths
        return GitDiffSnapshot(
            mode=mode,
            files=tuple(changes),
            branch=branch,
            head=head,
            clean=not changes,
            truncated=any(change.truncated for change in changes),
        )

    def added_lines(
        self,
        mode: DiffMode = "combined",
        *,
        limit: int = MAX_ADDED_LINES,
    ) -> tuple[tuple[GitAddedLine, ...], bool]:
        if mode not in ("working_tree", "staged", "combined"):
            raise ValueError(f"unsupported diff mode: {mode}")
        if limit < 1 or limit > MAX_ADDED_LINES:
            raise ValueError(f"added-line limit must be between 1 and {MAX_ADDED_LINES}")
        snapshot = self.snapshot(mode)
        result: list[GitAddedLine] = []
        truncated = snapshot.truncated
        for change in snapshot.files:
            if change.status == "deleted":
                continue
            if change.untracked:
                candidate = resolve_within_repository(self.repository_root, change.path)
                if not candidate.is_file() or candidate.stat().st_size > MAX_UNTRACKED_FILE_BYTES:
                    truncated = True
                    continue
                content = candidate.read_bytes()
                if b"\0" in content[:8192]:
                    continue
                text = content.decode("utf-8", errors="replace")
                lines = tuple(
                    GitAddedLine(change.path, number, line)
                    for number, line in enumerate(text.splitlines(), start=1)
                )
            else:
                selector = (
                    ("--cached",)
                    if mode == "staged"
                    else (() if mode == "working_tree" else (("HEAD",) if snapshot.head else ("--cached",)))
                )
                diff = self._git(
                    "diff",
                    *selector,
                    "--unified=0",
                    "--no-color",
                    "--no-ext-diff",
                    "--",
                    change.path,
                )
                lines = _parse_added_lines(change.path, diff)
            available = limit - len(result)
            result.extend(lines[:available])
            if len(lines) > available:
                truncated = True
                break
        return tuple(result), truncated

    def removed_lines(
        self,
        mode: DiffMode = "combined",
        *,
        limit: int = MAX_REMOVED_LINES,
    ) -> tuple[tuple[GitRemovedLine, ...], bool]:
        if mode not in ("working_tree", "staged", "combined"):
            raise ValueError(f"unsupported diff mode: {mode}")
        if limit < 1 or limit > MAX_REMOVED_LINES:
            raise ValueError(f"removed-line limit must be between 1 and {MAX_REMOVED_LINES}")
        snapshot = self.snapshot(mode)
        result: list[GitRemovedLine] = []
        truncated = snapshot.truncated
        for change in snapshot.files:
            if change.untracked:
                continue
            selector = (
                ("--cached",)
                if mode == "staged"
                else (() if mode == "working_tree" else (("HEAD",) if snapshot.head else ("--cached",)))
            )
            diff = self._git(
                "diff",
                *selector,
                "--unified=0",
                "--no-color",
                "--no-ext-diff",
                "--",
                change.path,
            )
            lines = _parse_removed_lines(change.path, diff)
            available = limit - len(result)
            result.extend(lines[:available])
            if len(lines) > available:
                truncated = True
                break
        return tuple(result), truncated

    def _diff_records(self, *, cached: bool = False, head: bool = False) -> list[GitFileChange]:
        selector = ["HEAD"] if head else (["--cached"] if cached else [])
        name_output = self._git("diff", *selector, "--name-status", "-z", "-M", "--no-ext-diff")
        numstat_output = self._git("diff", *selector, "--numstat", "-z", "-M", "--no-ext-diff")
        records = _parse_name_status(name_output)
        line_counts = _parse_numstat(numstat_output)
        for record in records:
            added, removed, binary = line_counts.get(record.path, (0, 0, False))
            record.lines_added = added
            record.lines_removed = removed
            record.binary = binary
        return records

    def _untracked_records(self) -> list[GitFileChange]:
        output = self._git("ls-files", "--others", "--exclude-standard", "-z")
        records: list[GitFileChange] = []
        for raw_path in filter(None, output.split("\0")):
            path = normalize_repository_path(raw_path)
            candidate = resolve_within_repository(self.repository_root, path)
            if not candidate.is_file():
                continue
            size = candidate.stat().st_size
            with candidate.open("rb") as handle:
                content = handle.read(MAX_UNTRACKED_FILE_BYTES + 1)
            truncated = size > MAX_UNTRACKED_FILE_BYTES
            binary = b"\0" in content[:8192]
            lines_added = None if truncated or binary else len(content.splitlines())
            records.append(
                GitFileChange(
                    path=path,
                    status="untracked",
                    lines_added=lines_added,
                    lines_removed=0 if lines_added is not None else None,
                    untracked=True,
                    binary=binary,
                    truncated=truncated,
                )
            )
        return records

    def _git(self, *args: str) -> str:
        execution = run_command(
            self.repository_root,
            CommandSpec(("git", "-C", str(self.repository_root), *args), self.repository_root, "git", "fixed Git argv"),
            timeout_seconds=10,
            stdout_limit=MAX_GIT_OUTPUT_BYTES,
            stderr_limit=64 * 1024,
        )
        if execution.truncated:
            raise RuntimeError("Git output exceeded the configured byte limit")
        if execution.status != "PASS":
            detail = execution.stderr.strip() or execution.error or f"exit code {execution.exit_code}"
            raise RuntimeError(f"Git command failed: {detail}")
        return execution.stdout

    def _git_optional(self, *args: str) -> str:
        try:
            return self._git(*args)
        except RuntimeError:
            return ""


def _parse_name_status(output: str) -> list[GitFileChange]:
    tokens = output.split("\0")
    records: list[GitFileChange] = []
    index = 0
    status_names = {"A": "added", "M": "modified", "D": "deleted", "T": "modified"}
    while index < len(tokens) and tokens[index]:
        raw_status = tokens[index]
        index += 1
        code = raw_status[0]
        if code in {"R", "C"}:
            if index + 1 >= len(tokens):
                raise ValueError("incomplete Git rename record")
            old_path = normalize_repository_path(tokens[index])
            path = normalize_repository_path(tokens[index + 1])
            index += 2
            records.append(GitFileChange(path=path, old_path=old_path, status="renamed"))
        else:
            if index >= len(tokens):
                raise ValueError("incomplete Git status record")
            path = normalize_repository_path(tokens[index])
            index += 1
            records.append(GitFileChange(path=path, status=status_names.get(code, "modified")))
    return records


def _parse_numstat(output: str) -> dict[str, tuple[int | None, int | None, bool]]:
    tokens = output.split("\0")
    counts: dict[str, tuple[int | None, int | None, bool]] = {}
    index = 0
    while index < len(tokens) and tokens[index]:
        header = tokens[index]
        index += 1
        parts = header.split("\t", 2)
        if len(parts) != 3:
            raise ValueError("invalid Git numstat record")
        added_raw, removed_raw, path_raw = parts
        binary = added_raw == "-" or removed_raw == "-"
        added = None if binary else int(added_raw)
        removed = None if binary else int(removed_raw)
        if path_raw:
            path = normalize_repository_path(path_raw)
        else:
            if index + 1 >= len(tokens):
                raise ValueError("incomplete Git rename numstat record")
            index += 1  # old path
            path = normalize_repository_path(tokens[index])
            index += 1
        counts[path] = (added, removed, binary)
    return counts


def _parse_added_lines(path: str, diff: str) -> tuple[GitAddedLine, ...]:
    result: list[GitAddedLine] = []
    line_number: int | None = None
    for raw in diff.splitlines():
        if raw.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,\d+)?", raw)
            line_number = int(match.group(1)) if match else None
            continue
        if line_number is None:
            continue
        if raw.startswith("+++"):
            continue
        if raw.startswith("+"):
            result.append(GitAddedLine(path, line_number, raw[1:]))
            line_number += 1
        elif raw.startswith("-") or raw.startswith("\\"):
            continue
        else:
            line_number += 1
    return tuple(result)


def _parse_removed_lines(path: str, diff: str) -> tuple[GitRemovedLine, ...]:
    result: list[GitRemovedLine] = []
    line_number: int | None = None
    for raw in diff.splitlines():
        if raw.startswith("@@"):
            match = re.search(r"-(\d+)(?:,\d+)?", raw)
            line_number = int(match.group(1)) if match else None
            continue
        if line_number is None:
            continue
        if raw.startswith("---"):
            continue
        if raw.startswith("-"):
            result.append(GitRemovedLine(path, line_number, raw[1:]))
            line_number += 1
        elif raw.startswith("+") or raw.startswith("\\"):
            continue
        else:
            line_number += 1
    return tuple(result)
