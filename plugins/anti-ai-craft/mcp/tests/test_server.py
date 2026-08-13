from __future__ import annotations

import json
from pathlib import Path

import pytest
from mcp import Client

from anti_ai_mcp.server import ServerSettings, create_server
from anti_ai_mcp.server import parse_settings
from anti_ai_mcp.paths import PluginRootError


@pytest.mark.anyio
async def test_status_tool_and_resource(
    repository: Path, plugin_root: Path, graph_path: Path
) -> None:
    server = create_server(
        ServerSettings(
            repository_root=repository,
            plugin_root=plugin_root,
            graph_path=str(graph_path),
            freshness_kind="ast",
        )
    )

    async with Client(server) as client:
        tool = await client.call_tool("get_anti_ai_status", {})
        assert tool.is_error is False
        assert tool.structured_content["anti_ai_craft_version"] == "0.6.0"
        assert tool.structured_content["graph"]["provider"] == "graphify"
        assert tool.structured_content["graph"]["node_count"] == 2
        assert tool.structured_content["skills_discovered"] == ["anti-ai-code"]

        resources = await client.list_resources()
        assert [str(resource.uri) for resource in resources.resources] == [
            "anti-ai://project/status",
            "anti-ai://project/repository",
            "anti-ai://project/checks",
        ]
        resource = await client.read_resource("anti-ai://project/status")
        compact = json.loads(resource.contents[0].text)
        assert compact["mcp_status"] == "available"
        assert compact["graph"]["provider"] == "graphify"
        assert compact["skills_count"] == 1
        repository_resource = await client.read_resource("anti-ai://project/repository")
        assert json.loads(repository_resource.contents[0].text)["status"] == "PASS"
        checks_resource = await client.read_resource("anti-ai://project/checks")
        assert json.loads(checks_resource.contents[0].text)["checks"] == []


@pytest.mark.anyio
async def test_status_tool_with_graph_disabled(
    repository: Path, plugin_root: Path
) -> None:
    server = create_server(
        ServerSettings(
            repository_root=repository,
            plugin_root=plugin_root,
            graph_path="graphify-out/graph.json",
            graph_enabled=False,
        )
    )

    async with Client(server) as client:
        tool = await client.call_tool("get_anti_ai_status", {})
        assert tool.structured_content["graph"]["availability"] == "disabled"
        assert not any(tool.structured_content["capabilities"].values())


@pytest.mark.anyio
async def test_stage_two_tools_are_registered_and_deterministic_without_graph(
    clean_repo: Path, tmp_path: Path
) -> None:
    plugin = clean_repo / "plugins" / "anti-ai-craft"
    _write_plugin_markers(plugin)
    (clean_repo / ".git" / "info" / "exclude").write_text(
        "plugins/anti-ai-craft/\n", encoding="utf-8"
    )
    server = create_server(
        ServerSettings(
            repository_root=clean_repo,
            plugin_root=plugin,
            graph_path="graphify-out/graph.json",
            graph_enabled=False,
        )
    )

    async with Client(server) as client:
        tools = await client.list_tools()
        assert [tool.name for tool in tools.tools] == [
            "get_anti_ai_status",
            "inspect_repository",
            "inspect_git_diff",
            "verify_change_scope",
            "run_project_validation",
            "run_relevant_tests",
            "analyze_change_impact",
            "inspect_architecture",
            "audit_architecture",
            "audit_anti_ai",
            "audit_security",
            "verify_remediation",
            "collect_evidence",
        ]
        repository = await client.call_tool("inspect_repository", {})
        assert repository.structured_content["status"] == "PASS"
        diff = await client.call_tool("inspect_git_diff", {"mode": "combined"})
        assert diff.structured_content["metadata"]["clean"] is True

        (clean_repo / "README.md").write_text("changed\n", encoding="utf-8")
        scope = await client.call_tool(
            "verify_change_scope",
            {"allowed": ["README.md"], "mode": "combined"},
        )
        assert scope.structured_content["status"] == "PASS"
        validation = await client.call_tool(
            "run_project_validation",
            {"categories": ["lint"], "dry_run": True},
        )
        assert validation.structured_content["status"] == "NOT_APPLICABLE"
        tests = await client.call_tool("run_relevant_tests", {"dry_run": True})
        assert tests.structured_content["status"] == "MANUAL_REVIEW_REQUIRED"
        impact = await client.call_tool(
            "analyze_change_impact", {"changed_files": ["README.md"]}
        )
        assert impact.structured_content["status"] == "MANUAL_REVIEW_REQUIRED"
        architecture = await client.call_tool("inspect_architecture", {})
        assert architecture.structured_content["status"] == "MANUAL_REVIEW_REQUIRED"
        architecture_audit = await client.call_tool("audit_architecture", {})
        assert architecture_audit.structured_content["status"] == "MANUAL_REVIEW_REQUIRED"
        anti_ai = await client.call_tool("audit_anti_ai", {})
        assert anti_ai.structured_content["status"] == "WARNING"
        assert anti_ai.structured_content["metadata"]["deterministic_evidence_available"] is True
        assert anti_ai.structured_content["metadata"]["graph_evidence_available"] is False
        security = await client.call_tool("audit_security", {})
        assert security.structured_content["status"] == "PASS"
        assert "graph" not in security.structured_content["metadata"]
        remediation = await client.call_tool(
            "verify_remediation",
            {
                "previous_findings": [
                    {
                        "id": "AA-UNKNOWN-001",
                        "category": "fixture",
                        "severity": "LOW",
                        "confidence": "LOW",
                        "message": "fixture",
                        "evidence": [],
                        "location": None,
                        "suggestion": None,
                        "fixed": True,
                    }
                ]
            },
        )
        assert remediation.structured_content["status"] == "WARNING"
        assert remediation.structured_content["metadata"]["remediations"][0]["state"] == "NOT_VERIFIABLE"
        bundle = await client.call_tool("collect_evidence", {"execute": False})
        assert bundle.structured_content["schema_version"] == "1.0"
        assert bundle.structured_content["graph"]["availability"] == "disabled"


@pytest.mark.anyio
async def test_stale_graph_does_not_change_deterministic_tool_results(
    clean_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = clean_repo / "graphify-out" / "graph.json"
    target.parent.mkdir()
    target.write_text(
        json.dumps(
            {
                "directed": False,
                "multigraph": False,
                "graph": {},
                "nodes": [{"id": "fixture", "label": "Fixture"}],
                "links": [],
            }
        ),
        encoding="utf-8",
    )
    (target.parent / "manifest.json").write_text("{}", encoding="utf-8")

    def stale(*_args, **_kwargs):
        return {"new_files": {"code": ["changed.py"]}, "deleted_files": []}

    monkeypatch.setattr("graphify.detect.detect_incremental", stale)
    plugin = clean_repo / "plugins" / "anti-ai-craft"
    _write_plugin_markers(plugin)
    stale_server = create_server(
        ServerSettings(clean_repo, plugin, "graphify-out/graph.json", freshness_kind="ast")
    )
    off_server = create_server(
        ServerSettings(clean_repo, plugin, "graphify-out/graph.json", graph_enabled=False)
    )

    async with Client(stale_server) as client:
        status = await client.call_tool("get_anti_ai_status", {})
        stale_result = await client.call_tool("inspect_git_diff", {"mode": "staged"})
    async with Client(off_server) as client:
        off_result = await client.call_tool("inspect_git_diff", {"mode": "staged"})
    assert status.structured_content["graph"]["freshness"] == "available_but_stale"
    assert stale_result.structured_content == off_result.structured_content


def test_external_installed_plugin_root_is_distinct_from_target_repository(
    clean_repo: Path, tmp_path: Path
) -> None:
    external_plugin = tmp_path.parent / f"installed-plugin-{tmp_path.name}"
    _write_plugin_markers(external_plugin)

    settings = parse_settings(
        [
            "--repository-root",
            str(clean_repo),
            "--plugin-root",
            str(external_plugin),
        ]
    )
    server = create_server(settings)

    assert settings.repository_root == clean_repo.resolve()
    assert settings.plugin_root == external_plugin.resolve()
    assert server is not None


def test_invalid_plugin_root_is_rejected(clean_repo: Path, tmp_path: Path) -> None:
    invalid_plugin = tmp_path / "not-a-plugin"
    invalid_plugin.mkdir()

    with pytest.raises(PluginRootError, match="plugin manifest"):
        create_server(
            ServerSettings(
                repository_root=clean_repo,
                plugin_root=invalid_plugin,
                graph_path="graphify-out/graph.json",
                graph_enabled=False,
            )
        )


def test_repository_root_must_be_explicit(
    clean_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("ANTI_AI_REPOSITORY_ROOT", raising=False)
    monkeypatch.setenv("ANTI_AI_PLUGIN_ROOT", str(clean_repo / "plugin"))

    with pytest.raises(SystemExit):
        parse_settings([])


def _write_plugin_markers(root: Path) -> None:
    (root / ".codex-plugin").mkdir(parents=True)
    (root / "skills").mkdir()
    (root / ".codex-plugin" / "plugin.json").write_text(
        json.dumps({"name": "anti-ai-craft", "version": "0.6.0"}),
        encoding="utf-8",
    )


@pytest.mark.anyio
async def test_public_mcp_inputs_fail_in_controlled_forms(clean_repo: Path) -> None:
    plugin = clean_repo / "plugins" / "anti-ai-craft"
    _write_plugin_markers(plugin)
    server = create_server(
        ServerSettings(clean_repo, plugin, "graphify-out/graph.json", graph_enabled=False)
    )

    async with Client(server) as client:
        invalid_enum = await client.call_tool("inspect_git_diff", {"mode": "sideways"})
        unexpected_type = await client.call_tool("inspect_git_diff", {"mode": 42})
        empty_remediation = await client.call_tool(
            "verify_remediation", {"previous_findings": []}
        )
        huge_scope = await client.call_tool(
            "verify_change_scope", {"allowed": [f"src/{index}" for index in range(101)]}
        )
        huge_impact = await client.call_tool(
            "analyze_change_impact",
            {"changed_files": [f"src/{index}.py" for index in range(101)]},
        )
        long_path = await client.call_tool(
            "analyze_change_impact", {"changed_files": ["x" * 4097]}
        )
        escaped_baseline = await client.call_tool(
            "collect_evidence", {"baseline_path": "../outside.json", "execute": False}
        )

    assert invalid_enum.is_error is True
    assert invalid_enum.structured_content is None
    assert unexpected_type.is_error is True
    assert empty_remediation.structured_content["errors"][0]["type"] == "INVALID_INPUT"
    assert huge_scope.structured_content["status"] == "ERROR"
    assert huge_impact.structured_content["status"] == "ERROR"
    assert long_path.structured_content["status"] == "ERROR"
    assert escaped_baseline.structured_content["overall_status"] == "FAIL"
    assert escaped_baseline.structured_content["errors"][0]["code"] == "BASELINE_INVALID"
