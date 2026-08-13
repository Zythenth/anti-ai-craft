from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

from . import __version__
from .checks import ProjectCheckService
from .git import DiffMode, GitInspector
from .graph import build_graph_provider
from .paths import resolve_within_repository
from .repository import RepositoryInspector
from .relevant_tests import RelevantTestService
from .scope import ScopeVerifier
from .status import AntiAiStatusService, StatusSettings


@dataclass(frozen=True)
class ServerSettings:
    repository_root: Path
    plugin_root: Path
    graph_path: str
    graph_enabled: bool = True
    freshness_kind: Literal["ast", "semantic"] = "semantic"


def create_server(settings: ServerSettings) -> MCPServer:
    repository_root = settings.repository_root.resolve(strict=True)
    plugin_root = resolve_within_repository(repository_root, settings.plugin_root).resolve(strict=True)
    settings = ServerSettings(
        repository_root=repository_root,
        plugin_root=plugin_root,
        graph_path=settings.graph_path,
        graph_enabled=settings.graph_enabled,
        freshness_kind=settings.freshness_kind,
    )
    provider = build_graph_provider(
        settings.repository_root,
        settings.graph_path,
        enabled=settings.graph_enabled,
        freshness_kind=settings.freshness_kind,
    )
    status_service = AntiAiStatusService(
        StatusSettings(settings.repository_root, settings.plugin_root),
        provider,
    )
    git_inspector = GitInspector(settings.repository_root)
    repository_inspector = RepositoryInspector(settings.repository_root, settings.plugin_root)
    check_service = ProjectCheckService(settings.repository_root)
    scope_verifier = ScopeVerifier(git_inspector)
    relevant_test_service = RelevantTestService(
        settings.repository_root,
        git_inspector,
        check_service,
    )
    server = MCPServer(
        "anti-ai-craft",
        version=__version__,
        instructions="Read-only Anti-AI Craft diagnostics and evidence capabilities.",
    )

    @server.tool(
        name="get_anti_ai_status",
        annotations=ToolAnnotations(
            readOnlyHint=True,
            idempotentHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    def get_anti_ai_status() -> dict[str, Any]:
        """Return Anti-AI Craft, repository, Git, skill, and Graphify status."""
        return status_service.get_status()

    @server.tool(
        name="inspect_repository",
        description=(
            "Inspect the configured repository using bounded filesystem, manifest, and fixed Git "
            "observations. Use for a compact factual project inventory; do not use it for architectural "
            "impact or Graphify analysis. No process other than fixed Git identity queries is executed."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True,
            idempotentHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    def inspect_repository() -> dict[str, Any]:
        return repository_inspector.inspect().to_dict()

    @server.tool(
        name="inspect_git_diff",
        description=(
            "Inspect staged, unstaged/untracked, or combined current Git changes with normalized "
            "repository-relative paths and bounded summaries. Use to establish what changed; do not "
            "use it to judge whether a change is acceptable. Accepts only the documented diff mode "
            "and never accepts arbitrary Git arguments."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True,
            idempotentHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    def inspect_git_diff(mode: DiffMode = "combined") -> dict[str, Any]:
        return git_inspector.inspect(mode).to_dict()

    @server.tool(
        name="verify_change_scope",
        description=(
            "Compare current Git path endpoints against allowed, denied, and exception patterns. "
            "Use when a task has an explicit file/directory/glob scope. Deny rules take precedence, "
            "exceptions remove paths from allowed scope, and both rename source and destination are "
            "checked. This deterministic check does not use Graphify."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True,
            idempotentHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    def verify_change_scope(
        allowed: list[str] | None = None,
        denied: list[str] | None = None,
        exceptions: list[str] | None = None,
        mode: DiffMode = "combined",
    ) -> dict[str, Any]:
        return scope_verifier.verify(
            allowed=allowed or (),
            denied=denied or (),
            exceptions=exceptions or (),
            mode=mode,
        ).to_dict()

    @server.tool(
        name="run_project_validation",
        description=(
            "Discover and optionally execute recognized lint, typecheck, format-check, build, test, "
            "or plugin-validation commands from project manifests. Use dry_run to inspect selection. "
            "The tool accepts categories, never a command string; execution uses shell=False, bounded "
            "output, a controlled environment, repository-contained cwd, and a bounded timeout."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=False,
            idempotentHint=False,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    def run_project_validation(
        categories: list[str] | None = None,
        dry_run: bool = False,
        timeout_seconds: float = 120.0,
    ) -> dict[str, Any]:
        return check_service.run(
            categories=categories or (),
            dry_run=dry_run,
            timeout_seconds=timeout_seconds,
        ).to_dict()

    @server.tool(
        name="run_relevant_tests",
        description=(
            "Select and optionally run tests relevant to current Git changes using deterministic "
            "path/name conventions and configured package suites. Use dry_run to inspect each "
            "selection_reason. No Graphify relationships are used; when no direct mapping exists the "
            "tool selects a configured package suite or requires manual review."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=False,
            idempotentHint=False,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    def run_relevant_tests(
        mode: DiffMode = "combined",
        dry_run: bool = False,
        timeout_seconds: float = 120.0,
    ) -> dict[str, Any]:
        return relevant_test_service.run(
            mode=mode,
            dry_run=dry_run,
            timeout_seconds=timeout_seconds,
        ).to_dict()

    @server.resource(
        "anti-ai://project/status",
        name="Anti-AI Craft project status",
        description="Compact read-only status for the current repository integration.",
        mime_type="application/json",
    )
    def project_status() -> str:
        return json.dumps(status_service.get_compact_status(), ensure_ascii=False, separators=(",", ":"))

    @server.resource(
        "anti-ai://project/repository",
        name="Anti-AI Craft repository summary",
        description="Compact deterministic repository inventory shared with inspect_repository.",
        mime_type="application/json",
    )
    def project_repository() -> str:
        return json.dumps(
            repository_inspector.inspect().to_dict(),
            ensure_ascii=False,
            separators=(",", ":"),
        )

    @server.resource(
        "anti-ai://project/checks",
        name="Anti-AI Craft validation capabilities",
        description="Recognized validation categories and fixed argv derived from project manifests.",
        mime_type="application/json",
    )
    def project_checks() -> str:
        return json.dumps(
            check_service.capabilities(),
            ensure_ascii=False,
            separators=(",", ":"),
        )

    return server


def parse_settings(argv: list[str] | None = None) -> ServerSettings:
    parser = argparse.ArgumentParser(description="Serve Anti-AI Craft diagnostics over MCP stdio.")
    parser.add_argument(
        "--repository-root",
        default=os.environ.get("ANTI_AI_REPOSITORY_ROOT", "."),
    )
    parser.add_argument(
        "--plugin-root",
        default=os.environ.get("ANTI_AI_PLUGIN_ROOT", "plugins/anti-ai-craft"),
    )
    parser.add_argument(
        "--graph-path",
        default=os.environ.get("ANTI_AI_GRAPH_PATH", "graphify-out/graph.json"),
    )
    parser.add_argument(
        "--graphify-freshness-kind",
        choices=("ast", "semantic"),
        default=os.environ.get("ANTI_AI_GRAPHIFY_FRESHNESS_KIND", "semantic"),
    )
    parser.add_argument("--disable-graph", action="store_true")
    args = parser.parse_args(argv)
    repository_root = Path(args.repository_root).resolve(strict=True)
    plugin_root = resolve_within_repository(repository_root, args.plugin_root).resolve(strict=True)
    return ServerSettings(
        repository_root=repository_root,
        plugin_root=plugin_root,
        graph_path=args.graph_path,
        graph_enabled=not args.disable_graph,
        freshness_kind=args.graphify_freshness_kind,
    )


def main() -> None:
    create_server(parse_settings()).run(transport="stdio")


if __name__ == "__main__":
    main()
