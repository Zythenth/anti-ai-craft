from __future__ import annotations

import json
from pathlib import Path

import pytest
from mcp import Client

from anti_ai_mcp.server import ServerSettings, create_server
from anti_ai_mcp.server import parse_settings
from anti_ai_mcp.paths import PathBoundaryError


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
        assert tool.structured_content["anti_ai_craft_version"] == "0.5.0"
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
    plugin.mkdir(parents=True)
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
    plugin.mkdir(parents=True)
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


def test_plugin_root_must_remain_inside_repository(clean_repo: Path, tmp_path: Path) -> None:
    with pytest.raises(PathBoundaryError):
        parse_settings(
            [
                "--repository-root",
                str(clean_repo),
                "--plugin-root",
                str(tmp_path.parent),
            ]
        )

    with pytest.raises(PathBoundaryError):
        create_server(
            ServerSettings(
                repository_root=clean_repo,
                plugin_root=tmp_path.parent,
                graph_path="graphify-out/graph.json",
                graph_enabled=False,
            )
        )
