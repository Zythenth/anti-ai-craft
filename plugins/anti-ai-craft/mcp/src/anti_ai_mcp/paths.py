from __future__ import annotations

import re
from pathlib import Path, PurePosixPath


MAX_PUBLIC_PATH_TEXT = 4096


class PathBoundaryError(ValueError):
    pass


class PluginRootError(ValueError):
    pass


def resolve_within_repository(repository_root: Path, candidate: str | Path) -> Path:
    root = repository_root.resolve(strict=True)
    requested = Path(candidate)
    combined = requested if requested.is_absolute() else root / requested
    resolved = combined.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise PathBoundaryError(f"path escapes repository root: {candidate}") from exc
    return resolved


def resolve_plugin_root(repository_root: Path, candidate: str | Path) -> Path:
    root = repository_root.resolve(strict=True)
    requested = Path(candidate)
    combined = requested if requested.is_absolute() else root / requested
    try:
        resolved = combined.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise PluginRootError(f"plugin root is unavailable: {candidate}") from exc
    if not resolved.is_dir():
        raise PluginRootError(f"plugin root is not a directory: {candidate}")
    if not (resolved / ".codex-plugin" / "plugin.json").is_file():
        raise PluginRootError(f"plugin manifest is missing below plugin root: {candidate}")
    if not (resolved / "skills").is_dir():
        raise PluginRootError(f"skills directory is missing below plugin root: {candidate}")
    return resolved


def normalize_repository_path(path: str | Path) -> str:
    raw = str(path).replace("\\", "/")
    if len(raw) > MAX_PUBLIC_PATH_TEXT:
        raise PathBoundaryError(f"path exceeds {MAX_PUBLIC_PATH_TEXT} character limit")
    if not raw or "\x00" in raw or raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
        raise PathBoundaryError(f"path is not repository-relative: {path}")
    parts = [part for part in raw.split("/") if part not in ("", ".")]
    if not parts or any(part == ".." for part in parts):
        raise PathBoundaryError(f"path escapes repository root: {path}")
    return PurePosixPath(*parts).as_posix()


def repository_relative_path(repository_root: Path, candidate: str | Path) -> str:
    root = repository_root.resolve(strict=True)
    resolved = resolve_within_repository(root, candidate)
    return resolved.relative_to(root).as_posix()


def normalize_scope_pattern(pattern: str) -> str:
    raw = pattern.strip().replace("\\", "/")
    if len(raw) > MAX_PUBLIC_PATH_TEXT:
        raise PathBoundaryError(f"scope pattern exceeds {MAX_PUBLIC_PATH_TEXT} character limit")
    if not raw or "\x00" in raw or raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
        raise PathBoundaryError(f"scope pattern is not repository-relative: {pattern}")
    parts = [part for part in raw.split("/") if part not in ("", ".")]
    if not parts or any(part == ".." for part in parts):
        raise PathBoundaryError(f"scope pattern escapes repository root: {pattern}")
    return "/".join(parts)
