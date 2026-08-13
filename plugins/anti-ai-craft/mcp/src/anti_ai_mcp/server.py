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
from .anti_ai_audit import AntiAiAuditService
from .architecture import ArchitectureService
from .baseline import BaselineService
from .checks import ProjectCheckService
from .evidence_bundle import EvidenceBundleService
from .git import DiffMode, GitInspector
from .graph import build_graph_provider
from .impact import ChangeImpactService
from .observability import observe_tool
from .paths import resolve_plugin_root
from .repository import RepositoryInspector
from .relevant_tests import RelevantTestService
from .remediation import RemediationService
from .scope import ScopeVerifier
from .security_audit import SecurityAuditService
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
    plugin_root = resolve_plugin_root(repository_root, settings.plugin_root)
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
    relevant_test_service = RelevantTestService(
        settings.repository_root,
        git_inspector,
        check_service,
        provider,
    )
    impact_service = ChangeImpactService(git_inspector, provider)
    architecture_service = ArchitectureService(git_inspector, provider)
    anti_ai_audit_service = AntiAiAuditService(
        settings.repository_root,
        git_inspector,
        provider,
        architecture_service,
    )
    security_audit_service = SecurityAuditService(settings.repository_root, git_inspector)
    scope_verifier = ScopeVerifier(git_inspector)
    remediation_service = RemediationService(
        anti_ai_audit_service,
        security_audit_service,
        scope_verifier,
    )
    baseline_service = BaselineService(settings.repository_root)
    evidence_bundle_service = EvidenceBundleService(
        settings.repository_root,
        status_service,
        repository_inspector,
        git_inspector,
        scope_verifier,
        check_service,
        relevant_test_service,
        impact_service,
        architecture_service,
        anti_ai_audit_service,
        security_audit_service,
        remediation_service,
        baseline_service,
    )
    server = MCPServer(
        "anti-ai-craft",
        version=__version__,
        instructions=(
            "Local, bounded Anti-AI Craft evidence for one explicitly configured target repository. "
            "Most tools are read-only. run_project_validation, run_relevant_tests, and "
            "collect_evidence(execute=true) run only recognized project commands without a shell. "
            "No tool uses network access. Graphify is optional evidence; stale/off state never "
            "suppresses deterministic findings. Use focused tools first and collect_evidence for "
            "final review. Baseline creation is an explicit stateful CLI operation, not an MCP tool."
        ),
    )

    @server.tool(
        name="get_anti_ai_status",
        description=(
            "Read integration, target Git, plugin-skill, and Graphify availability/freshness status. "
            "Use for startup diagnostics, not repository analysis. It runs only a fixed Git identity "
            "probe, executes no project command, and reports stale/off Graphify without hiding it."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True,
            idempotentHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    @observe_tool("get_anti_ai_status")
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
    @observe_tool("inspect_repository")
    def inspect_repository() -> dict[str, Any]:
        return repository_inspector.inspect().to_dict()

    @server.tool(
        name="inspect_git_diff",
        description=(
            "Inspect staged, unstaged/untracked, or combined current Git changes with normalized "
            "repository-relative paths and bounded summaries. Use to establish what changed; do not "
            "use it to judge whether a change is acceptable. Accepts only the documented diff mode "
            "and never accepts arbitrary Git arguments. It does not use Graphify or run project code."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True,
            idempotentHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    @observe_tool("inspect_git_diff")
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
    @observe_tool("verify_change_scope")
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
            "output, a controlled environment, repository-contained cwd, and a bounded timeout. It "
            "does not use Graphify or network access, but non-dry-run executes repository-owned code."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=False,
            idempotentHint=False,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    @observe_tool("run_project_validation")
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
            "path/name conventions and configured package suites, then add bounded Graphify candidates "
            "without removing deterministic selections. Use dry_run to inspect each selection_reason. "
            "When no direct deterministic mapping exists, the configured suite remains the fallback. "
            "Stale/off Graphify is explicit; non-dry-run executes recognized repository tests."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=False,
            idempotentHint=False,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    @observe_tool("run_relevant_tests")
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

    @server.tool(
        name="analyze_change_impact",
        description=(
            "Map explicit files or current Git changes to bounded structural neighbors, indirect "
            "candidates, graph communities, cross-community paths, and affected tests. The result "
            "preserves relation provenance, freshness, direction, confidence, coverage, and truncation. "
            "Use for structural review, not proof of runtime impact. It is read-only and degrades to "
            "manual review when Graphify is unavailable."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True,
            idempotentHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    @observe_tool("analyze_change_impact")
    def analyze_change_impact(
        changed_files: list[str] | None = None,
        max_depth: int = 2,
        include_tests: bool = True,
    ) -> dict[str, Any]:
        return impact_service.analyze(
            changed_files=changed_files,
            max_depth=max_depth,
            include_tests=include_tests,
        ).to_dict()

    @server.tool(
        name="inspect_architecture",
        description=(
            "Return a compact graph-derived structural overview: graph communities, representative "
            "nodes, bounded hotspots, and cross-community relations. Communities are structural "
            "clusters, not automatically domains or architecture layers. It is read-only; stale/off "
            "Graphify remains explicit and prevents unsupported conclusions."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True,
            idempotentHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    @observe_tool("inspect_architecture")
    def inspect_architecture() -> dict[str, Any]:
        return architecture_service.inspect().to_dict()

    @server.tool(
        name="audit_architecture",
        description=(
            "Audit current Git changes for conservative structural signals: attributable new "
            "cross-community relations, directed cycles only when direction is reliable, and changed "
            "graph hotspots. It never treats a graph connection alone as an architecture violation, "
            "runs no project command, and requires review when Graphify cannot support the judgment."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True,
            idempotentHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    @observe_tool("audit_architecture")
    def audit_architecture(mode: DiffMode = "combined") -> dict[str, Any]:
        return architecture_service.audit(mode=mode).to_dict()

    @server.tool(
        name="audit_anti_ai",
        description=(
            "Combine current-diff facts, bounded graph evidence, conservative architecture signals, "
            "and a small documented set of Anti-AI heuristics. Findings describe observable code "
            "patterns and uncertainty; they never infer authorship. It is read-only, runs no project "
            "command, and keeps deterministic signals when Graphify is stale/off."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True,
            idempotentHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    @observe_tool("audit_anti_ai")
    def audit_anti_ai(mode: DiffMode = "combined") -> dict[str, Any]:
        return anti_ai_audit_service.audit(mode=mode).to_dict()

    @server.tool(
        name="audit_security",
        description=(
            "Audit only the current Git change and security-sensitive configuration for bounded, "
            "defensive signals such as credential formats (always redacted), explicit shell/dynamic "
            "execution, traversal constants, unsafe temporary files, and control weakening. Use it "
            "before accepting a change; do not use it as a pentest or proof that the repository is "
            "secure. It is read-only, executes no project command or network request, and does not "
            "use Graphify, so stale or disabled graph state does not affect the result."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True,
            idempotentHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    @observe_tool("audit_security")
    def audit_security(mode: DiffMode = "combined") -> dict[str, Any]:
        return security_audit_service.audit(mode=mode).to_dict()

    @server.tool(
        name="verify_remediation",
        description=(
            "Recheck previous finding objects against current Git, Anti-AI, scope, and defensive "
            "security evidence. Use after a proposed fix; claimed fixed/resolved fields are ignored. "
            "It returns resolved, partial, unresolved, regression, not-verifiable, or manual-review "
            "states and never writes files or runs project commands. Graph-backed judgment rules may "
            "remain manual when Graphify is stale, undirected, or unavailable."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True,
            idempotentHint=True,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    @observe_tool("verify_remediation")
    def verify_remediation(
        previous_findings: list[dict[str, Any]],
        mode: DiffMode = "combined",
    ) -> dict[str, Any]:
        return remediation_service.verify(previous_findings, mode=mode).to_dict()

    @server.tool(
        name="collect_evidence",
        description=(
            "Collect one schema-versioned bundle containing repository/Git/scope, validation and "
            "relevant-test selection or execution, Graphify status, impact, architecture, Anti-AI, "
            "security, optional remediation, and optional baseline comparison. Use for final review "
            "or CI evidence; do not use when one focused tool is enough. It has no cross-call cache. "
            "With execute=false it only performs bounded inspections; execute=true runs recognized "
            "project commands and deduplicates only identical command/argv/cwd/state. Stale or disabled "
            "Graphify remains explicit and does not suppress deterministic sections."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=False,
            idempotentHint=False,
            destructiveHint=False,
            openWorldHint=False,
        ),
    )
    @observe_tool("collect_evidence")
    def collect_evidence(
        allowed: list[str] | None = None,
        denied: list[str] | None = None,
        exceptions: list[str] | None = None,
        baseline_path: str | None = None,
        previous_findings: list[dict[str, Any]] | None = None,
        execute: bool = False,
        timeout_seconds: float = 120.0,
    ) -> dict[str, Any]:
        return evidence_bundle_service.collect(
            allowed=allowed,
            denied=denied,
            exceptions=exceptions,
            baseline_path=baseline_path,
            previous_findings=previous_findings,
            execute=execute,
            timeout_seconds=timeout_seconds,
        )

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
    repository_default = os.environ.get("ANTI_AI_REPOSITORY_ROOT")
    parser.add_argument(
        "--repository-root",
        default=repository_default,
        required=repository_default is None,
        help="Explicit target repository to analyze (or ANTI_AI_REPOSITORY_ROOT).",
    )
    plugin_default = os.environ.get("ANTI_AI_PLUGIN_ROOT")
    parser.add_argument(
        "--plugin-root",
        default=plugin_default,
        required=plugin_default is None,
        help="Explicit Anti-AI Craft installation root (or ANTI_AI_PLUGIN_ROOT).",
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
    plugin_root = resolve_plugin_root(repository_root, args.plugin_root)
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
