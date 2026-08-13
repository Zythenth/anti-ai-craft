from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import __version__ as mcp_version
from .execution import CommandSpec, run_command
from .graph import GraphProvider


MAX_STATUS_MANIFEST_BYTES = 1024 * 1024
MAX_STATUS_SKILLS = 100


@dataclass(frozen=True)
class StatusSettings:
    repository_root: Path
    plugin_root: Path


class AntiAiStatusService:
    def __init__(self, settings: StatusSettings, graph_provider: GraphProvider) -> None:
        self.settings = settings
        self.graph_provider = graph_provider

    def get_status(self) -> dict[str, Any]:
        graph = self.graph_provider.get_status()
        skills, skills_count = self._skills()
        return {
            "anti_ai_craft_version": self._plugin_version(),
            "mcp": {"name": "anti-ai-craft", "version": mcp_version, "status": "available"},
            "repository_root": str(self.settings.repository_root),
            "git": self._git_status(),
            "graph": graph.to_dict(),
            "capabilities": graph.capabilities.to_dict(),
            "skills_discovered": skills,
            "skills_count": skills_count,
            "limits": {
                "max_skills_returned": MAX_STATUS_SKILLS,
                "skills_truncated": skills_count > MAX_STATUS_SKILLS,
            },
        }

    def get_compact_status(self) -> dict[str, Any]:
        status = self.get_status()
        graph = status["graph"]
        return {
            "anti_ai_craft_version": status["anti_ai_craft_version"],
            "mcp_status": status["mcp"]["status"],
            "repository_root": status["repository_root"],
            "graph": {
                "provider": graph["provider"],
                "availability": graph["availability"],
                "freshness": graph["freshness"],
            },
            "capabilities": status["capabilities"],
            "skills_count": status["skills_count"],
        }

    def _plugin_version(self) -> str:
        manifest = self.settings.plugin_root / ".codex-plugin" / "plugin.json"
        try:
            if manifest.stat().st_size > MAX_STATUS_MANIFEST_BYTES:
                return "unknown"
            payload = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return "unknown"
        version = payload.get("version")
        return str(version) if version else "unknown"

    def _skills(self) -> tuple[list[str], int]:
        skills_root = self.settings.plugin_root / "skills"
        if not skills_root.is_dir():
            return [], 0
        skills = sorted(
            path.name
            for path in skills_root.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        )
        return skills[:MAX_STATUS_SKILLS], len(skills)

    def _git_status(self) -> dict[str, Any]:
        result = run_command(
            self.settings.repository_root,
            CommandSpec(
                (
                    "git",
                    "-C",
                    str(self.settings.repository_root),
                    "rev-parse",
                    "--show-toplevel",
                ),
                self.settings.repository_root,
                "git",
                "fixed status probe",
            ),
            timeout_seconds=3,
            stdout_limit=16 * 1024,
            stderr_limit=16 * 1024,
        )
        if result.unavailable:
            return {"available": False, "repository": False}
        if result.status != "PASS":
            return {"available": True, "repository": False}
        return {
            "available": True,
            "repository": True,
            "root": result.stdout.strip(),
        }
