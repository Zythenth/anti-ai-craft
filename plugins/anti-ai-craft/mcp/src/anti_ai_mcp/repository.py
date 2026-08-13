from __future__ import annotations

import json
import os
import re
import tomllib
from collections import Counter
from pathlib import Path
from typing import Any

from .evidence import (
    CheckResult,
    CheckStatus,
    Confidence,
    Evidence,
    EvidenceKind,
    Finding,
    Severity,
)
from .git import GitInspector
from .paths import PathBoundaryError, resolve_within_repository


MAX_SCANNED_FILES = 10_000
MAX_RETURNED_ITEMS = 100
MAX_MANIFEST_BYTES = 1024 * 1024
EXCLUDED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "graphify-out",
    "node_modules",
}

LANGUAGE_EXTENSIONS = {
    ".c": "C",
    ".cc": "C++",
    ".cpp": "C++",
    ".cs": "C#",
    ".css": "CSS",
    ".go": "Go",
    ".html": "HTML",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".kt": "Kotlin",
    ".php": "PHP",
    ".py": "Python",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".sh": "Shell",
    ".swift": "Swift",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".vue": "Vue",
}

MANIFEST_NAMES = {
    "Cargo.toml",
    "Gemfile",
    "go.mod",
    "package.json",
    "pom.xml",
    "pyproject.toml",
    "requirements.txt",
}

CONFIG_NAMES = {
    ".editorconfig",
    ".gitignore",
    ".pre-commit-config.yaml",
    "AGENTS.md",
    "Dockerfile",
    "Makefile",
    "biome.json",
    "eslint.config.js",
    "eslint.config.mjs",
    "mypy.ini",
    "pytest.ini",
    "ruff.toml",
    "tsconfig.json",
    "vite.config.js",
    "vite.config.ts",
}

NODE_FRAMEWORKS = {
    "@angular/core": "Angular",
    "@nestjs/core": "NestJS",
    "@remix-run/react": "Remix",
    "astro": "Astro",
    "express": "Express",
    "next": "Next.js",
    "react": "React",
    "svelte": "Svelte",
    "vue": "Vue",
}

PYTHON_FRAMEWORKS = {
    "django": "Django",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "pytest": "pytest",
}


class RepositoryInspector:
    def __init__(self, repository_root: Path, plugin_root: Path) -> None:
        self.repository_root = repository_root.resolve(strict=True)
        self.plugin_root = plugin_root.resolve(strict=False)

    def inspect(self) -> CheckResult:
        files, scan_truncated = self._files()
        manifests = sorted(path for path in files if path.name in MANIFEST_NAMES)
        invalid_manifests = [
            self._relative(path)
            for path in manifests
            if path.name in {"package.json", "pyproject.toml"} and self._manifest(path) is None
        ]
        languages = self._languages(files)
        package_managers = self._package_managers(files)
        scripts, script_truncated = self._scripts(manifests)
        frameworks, framework_evidence = self._frameworks(manifests)
        tests = self._tests(files)
        ci = self._ci(files)
        documentation = self._documentation(files)
        important_config = sorted(
            path.relative_to(self.repository_root).as_posix()
            for path in files
            if path.name in CONFIG_NAMES or path.name.startswith(".env.example")
        )
        main_directories = sorted(
            path.name
            for path in self.repository_root.iterdir()
            if path.is_dir() and path.name not in EXCLUDED_DIRECTORIES
        )
        git = self._git()
        anti_ai = self._anti_ai(files)

        limits_truncated = scan_truncated or script_truncated or any(
            len(items) > MAX_RETURNED_ITEMS
            for items in (
                manifests,
                important_config,
                main_directories,
                ci,
                documentation,
                package_managers,
                frameworks,
            )
        )
        evidence = [
            Evidence(
                EvidenceKind.FACT,
                "filesystem",
                {"repository_root": self.repository_root.as_posix(), "files_scanned": len(files)},
            ),
            Evidence(
                EvidenceKind.FACT,
                "manifests",
                {"paths": [self._relative(path) for path in manifests[:MAX_RETURNED_ITEMS]]},
            ),
            *framework_evidence,
        ]
        if git.get("repository"):
            evidence.append(Evidence(EvidenceKind.FACT, "git", git))
        findings: list[Finding] = []
        status = CheckStatus.PASS
        if limits_truncated:
            status = CheckStatus.WARNING
            findings.append(
                Finding(
                    id="AA-REPO-001",
                    category="repository",
                    severity=Severity.LOW,
                    confidence=Confidence.HIGH,
                    message="Repository inspection reached one or more explicit output limits.",
                    evidence=(evidence[0],),
                    suggestion="Use direct repository inspection for entries omitted from the compact summary.",
                )
            )
        if invalid_manifests:
            status = CheckStatus.WARNING
            manifest_evidence = Evidence(
                EvidenceKind.FACT,
                "manifest parser",
                {"paths": invalid_manifests[:MAX_RETURNED_ITEMS]},
            )
            evidence.append(manifest_evidence)
            findings.append(
                Finding(
                    id="AA-REPO-002",
                    category="repository",
                    severity=Severity.MEDIUM,
                    confidence=Confidence.HIGH,
                    message=f"{len(invalid_manifests)} recognized manifest(s) could not be parsed within limits.",
                    evidence=(manifest_evidence,),
                    suggestion="Repair the manifest syntax/encoding or reduce it below the byte limit.",
                )
            )

        return CheckResult(
            status=status,
            summary=f"Inspected {len(files)} repository file(s) without using Graphify.",
            findings=tuple(findings),
            evidence=tuple(evidence[:MAX_RETURNED_ITEMS]),
            metadata={
                "repository": {
                    "root": self.repository_root.as_posix(),
                    "git": git,
                },
                "languages": languages,
                "package_managers": package_managers[:MAX_RETURNED_ITEMS],
                "manifests": [self._relative(path) for path in manifests[:MAX_RETURNED_ITEMS]],
                "manifest_errors": invalid_manifests[:MAX_RETURNED_ITEMS],
                "frameworks": frameworks[:MAX_RETURNED_ITEMS],
                "scripts": scripts[:MAX_RETURNED_ITEMS],
                "main_directories": main_directories[:MAX_RETURNED_ITEMS],
                "important_config": important_config[:MAX_RETURNED_ITEMS],
                "tests": tests,
                "ci": {"detected": bool(ci), "files": ci[:MAX_RETURNED_ITEMS]},
                "documentation": documentation[:MAX_RETURNED_ITEMS],
                "anti_ai": anti_ai,
                "limits": {
                    "max_scanned_files": MAX_SCANNED_FILES,
                    "max_returned_items_per_section": MAX_RETURNED_ITEMS,
                    "max_manifest_bytes": MAX_MANIFEST_BYTES,
                    "truncated": limits_truncated,
                },
            },
        )

    def _files(self) -> tuple[list[Path], bool]:
        files: list[Path] = []
        truncated = False
        for current, directories, names in os.walk(self.repository_root):
            directories[:] = sorted(name for name in directories if name not in EXCLUDED_DIRECTORIES)
            for name in sorted(names):
                files.append(Path(current) / name)
                if len(files) >= MAX_SCANNED_FILES:
                    truncated = True
                    return files, truncated
        return files, truncated

    def _languages(self, files: list[Path]) -> list[dict[str, Any]]:
        counts = Counter(
            LANGUAGE_EXTENSIONS[path.suffix.lower()]
            for path in files
            if path.suffix.lower() in LANGUAGE_EXTENSIONS
        )
        return [
            {"name": name, "file_count": count, "evidence": "file extensions"}
            for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        ]

    def _package_managers(self, files: list[Path]) -> list[dict[str, str]]:
        detected: list[dict[str, str]] = []
        mapping = (
            ("uv.lock", "uv"),
            ("pnpm-lock.yaml", "pnpm"),
            ("yarn.lock", "Yarn"),
            ("package-lock.json", "npm"),
            ("bun.lock", "Bun"),
            ("Cargo.lock", "Cargo"),
            ("Gemfile.lock", "Bundler"),
            ("go.mod", "Go modules"),
        )
        for filename, manager in mapping:
            for path in (path for path in files if path.name == filename):
                detected.append(
                    {"name": manager, "evidence": self._relative(path)}
                )
        return sorted(detected, key=lambda item: (item["name"], item["evidence"]))

    def _scripts(self, manifests: list[Path]) -> tuple[list[dict[str, str]], bool]:
        scripts: list[dict[str, str]] = []
        truncated = False
        for manifest in manifests:
            payload = self._manifest(manifest)
            if payload is None:
                continue
            if manifest.name == "package.json":
                values = payload.get("scripts", {})
                if isinstance(values, dict):
                    for name, command in sorted(values.items()):
                        command_text = str(command)
                        if len(command_text) > 500:
                            command_text = command_text[:500]
                            truncated = True
                        scripts.append(
                            {
                                "name": str(name),
                                "command": command_text,
                                "manifest": self._relative(manifest),
                                "ecosystem": "node",
                            }
                        )
            elif manifest.name == "pyproject.toml":
                values = payload.get("project", {}).get("scripts", {})
                if isinstance(values, dict):
                    for name, entrypoint in sorted(values.items()):
                        scripts.append(
                            {
                                "name": str(name),
                                "command": str(entrypoint),
                                "manifest": self._relative(manifest),
                                "ecosystem": "python-entrypoint",
                            }
                        )
        return scripts, truncated

    def _frameworks(self, manifests: list[Path]) -> tuple[list[dict[str, str]], list[Evidence]]:
        detected: dict[tuple[str, str], dict[str, str]] = {}
        evidence: list[Evidence] = []
        for manifest in manifests:
            payload = self._manifest(manifest)
            if payload is None:
                continue
            dependencies: set[str] = set()
            if manifest.name == "package.json":
                for section in ("dependencies", "devDependencies", "peerDependencies"):
                    values = payload.get(section, {})
                    if isinstance(values, dict):
                        dependencies.update(str(name).lower() for name in values)
                mapping = NODE_FRAMEWORKS
            elif manifest.name == "pyproject.toml":
                project_dependencies = payload.get("project", {}).get("dependencies", [])
                groups = payload.get("dependency-groups", {})
                values = list(project_dependencies) if isinstance(project_dependencies, list) else []
                if isinstance(groups, dict):
                    for group in groups.values():
                        if isinstance(group, list):
                            values.extend(group)
                dependencies.update(_python_dependency_name(str(value)) for value in values)
                mapping = PYTHON_FRAMEWORKS
            else:
                continue
            for dependency, framework in mapping.items():
                if dependency in dependencies:
                    item = {
                        "name": framework,
                        "manifest": self._relative(manifest),
                        "dependency": dependency,
                    }
                    detected[(framework, self._relative(manifest))] = item
                    evidence.append(
                        Evidence(
                            EvidenceKind.FACT,
                            "manifest dependency",
                            item,
                        )
                    )
        return sorted(detected.values(), key=lambda item: (item["name"], item["manifest"])), evidence

    def _tests(self, files: list[Path]) -> dict[str, Any]:
        detected = []
        for path in files:
            relative = self._relative(path)
            name = path.name.lower()
            parts = {part.lower() for part in path.parts}
            if (
                name.startswith("test_")
                or name.endswith("_test.py")
                or ".test." in name
                or ".spec." in name
                or "tests" in parts
                or "__tests__" in parts
            ):
                detected.append(relative)
        return {
            "detected": bool(detected),
            "file_count": len(detected),
            "files": sorted(detected)[:MAX_RETURNED_ITEMS],
            "truncated": len(detected) > MAX_RETURNED_ITEMS,
        }

    def _ci(self, files: list[Path]) -> list[str]:
        detected = []
        for path in files:
            relative = self._relative(path)
            if (
                relative.startswith(".github/workflows/")
                or path.name in {".gitlab-ci.yml", "azure-pipelines.yml", "Jenkinsfile"}
            ):
                detected.append(relative)
        return sorted(detected)

    def _documentation(self, files: list[Path]) -> list[str]:
        return sorted(
            self._relative(path)
            for path in files
            if path.name.lower().startswith("readme")
            or self._relative(path).startswith("docs/")
        )

    def _anti_ai(self, files: list[Path]) -> dict[str, Any]:
        skills = sorted({
            path.parent.name
            for path in files
            if path.name == "SKILL.md" and "skills" in path.parts
        })
        config_path = self.repository_root / ".codex" / "config.toml"
        mcp_configured = False
        if config_path.is_file() and config_path.stat().st_size <= MAX_MANIFEST_BYTES:
            try:
                safe_config = resolve_within_repository(self.repository_root, config_path)
                payload = tomllib.loads(safe_config.read_text(encoding="utf-8"))
                mcp_configured = "anti-ai-craft" in payload.get("mcp_servers", {})
            except (OSError, UnicodeError, tomllib.TOMLDecodeError, PathBoundaryError):
                pass
        return {
            "plugin_root": (
                self.plugin_root.relative_to(self.repository_root).as_posix()
                if self.plugin_root.is_relative_to(self.repository_root)
                else None
            ),
            "skills": skills[:MAX_RETURNED_ITEMS],
            "skills_count": len(skills),
            "mcp_configured": mcp_configured,
            "mcp_config": ".codex/config.toml" if config_path.is_file() else None,
        }

    def _git(self) -> dict[str, Any]:
        try:
            snapshot = GitInspector(self.repository_root).snapshot("staged")
        except (RuntimeError, ValueError):
            return {"available": False, "repository": False, "branch": None, "head": None}
        return {
            "available": True,
            "repository": True,
            "branch": snapshot.branch,
            "head": snapshot.head,
        }

    def _manifest(self, path: Path) -> dict[str, Any] | None:
        try:
            safe_path = resolve_within_repository(self.repository_root, path)
            if safe_path.stat().st_size > MAX_MANIFEST_BYTES:
                return None
            if path.name == "package.json":
                payload = json.loads(safe_path.read_text(encoding="utf-8"))
            elif path.name == "pyproject.toml":
                payload = tomllib.loads(safe_path.read_text(encoding="utf-8"))
            else:
                return None
        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            tomllib.TOMLDecodeError,
            PathBoundaryError,
        ):
            return None
        return payload if isinstance(payload, dict) else None

    def _relative(self, path: Path) -> str:
        return path.relative_to(self.repository_root).as_posix()


def _python_dependency_name(requirement: str) -> str:
    match = re.match(r"[A-Za-z0-9_.-]+", requirement.strip())
    return match.group(0).lower().replace("_", "-") if match else ""
