from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from anti_ai_mcp.evidence import EvidenceKind
from anti_ai_mcp.graph import (
    GraphAvailability,
    GraphFreshness,
    GraphUnavailableError,
    GraphifyProvider,
    NullGraphProvider,
    PathBoundaryError,
    build_graph_provider,
    graphify_freshness_probe,
    resolve_within_repository,
)


def fresh(*_args) -> tuple[GraphFreshness, str]:
    return GraphFreshness.AVAILABLE_AND_FRESH, "fixture is current"


def stale(*_args) -> tuple[GraphFreshness, str]:
    return GraphFreshness.AVAILABLE_BUT_STALE, "fixture changed"


def unknown(*_args) -> tuple[GraphFreshness, str]:
    return GraphFreshness.UNKNOWN_FRESHNESS, "no manifest"


def test_graphify_provider_available_and_structural_operations(
    repository: Path, graph_path: Path
) -> None:
    provider = GraphifyProvider(repository, graph_path, freshness_probe=fresh)

    status = provider.get_status()
    assert status.availability is GraphAvailability.AVAILABLE
    assert status.freshness is GraphFreshness.AVAILABLE_AND_FRESH
    assert status.node_count == 2
    assert status.edge_count == 1
    assert status.capabilities.to_dict() == {
        "query": True,
        "node": True,
        "neighbors": True,
        "dependencies": True,
        "dependents": True,
        "paths": True,
        "communities": True,
    }
    assert provider.query("Graphify provider").nodes[0].id == "provider"
    assert provider.get_node("GraphifyProvider").evidence_kind is EvidenceKind.FACT
    assert {node.id for node in provider.get_dependencies("status").nodes} == {"provider", "status"}
    assert {node.id for node in provider.get_dependents("provider").nodes} == {"provider", "status"}
    assert len(provider.find_path("status", "provider").edges) == 1
    assert len(provider.get_community(1).nodes) == 2


def test_null_provider_is_explicitly_unavailable() -> None:
    provider = NullGraphProvider()
    assert provider.get_status().availability is GraphAvailability.UNAVAILABLE
    assert not any(provider.get_status().capabilities.to_dict().values())
    with pytest.raises(GraphUnavailableError):
        provider.query("anything")


def test_missing_graph_is_unavailable_but_provider_can_recover(repository: Path) -> None:
    provider = build_graph_provider(repository, freshness_probe=fresh)
    assert provider.get_status().availability is GraphAvailability.UNAVAILABLE

    path = repository / "graphify-out" / "graph.json"
    path.parent.mkdir()
    path.write_text(
        json.dumps({"directed": True, "multigraph": False, "graph": {}, "nodes": [], "links": []}),
        encoding="utf-8",
    )
    assert provider.get_status().availability is GraphAvailability.AVAILABLE


def test_invalid_graph_is_reported(repository: Path) -> None:
    path = repository / "graphify-out" / "graph.json"
    path.parent.mkdir()
    path.write_text('{"nodes": [', encoding="utf-8")
    provider = GraphifyProvider(repository, path, freshness_probe=fresh)
    assert provider.get_status().availability is GraphAvailability.INVALID
    with pytest.raises(GraphUnavailableError):
        provider.query("node")


def test_unchanged_invalid_graph_is_not_reparsed(
    repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = repository / "graphify-out" / "graph.json"
    path.parent.mkdir()
    path.write_text('{"nodes": [], "links": []}', encoding="utf-8")
    provider = GraphifyProvider(repository, path, freshness_probe=fresh)
    calls = 0

    def invalid(_payload):
        nonlocal calls
        calls += 1
        raise ValueError("fixture invalid")

    monkeypatch.setattr(provider, "_validate_payload", invalid)
    assert provider.get_status().availability is GraphAvailability.INVALID
    assert provider.get_status().availability is GraphAvailability.INVALID
    assert calls == 1


@pytest.mark.parametrize(
    ("probe", "availability", "freshness"),
    [
        (stale, GraphAvailability.STALE, GraphFreshness.AVAILABLE_BUT_STALE),
        (unknown, GraphAvailability.AVAILABLE, GraphFreshness.UNKNOWN_FRESHNESS),
    ],
)
def test_freshness_states(repository, graph_path, probe, availability, freshness) -> None:
    status = GraphifyProvider(repository, graph_path, freshness_probe=probe).get_status()
    assert status.availability is availability
    assert status.freshness is freshness


def test_ast_freshness_ignores_non_code_files(
    repository: Path, graph_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (graph_path.parent / "manifest.json").write_text("{}", encoding="utf-8")

    def incremental(*_args, **_kwargs):
        return {
            "new_total": 3,
            "new_files": {"code": [], "document": ["a.md", "b.md", "c.md"]},
            "deleted_files": [],
        }

    monkeypatch.setattr("graphify.detect.detect_incremental", incremental)
    freshness, _ = graphify_freshness_probe(repository, graph_path, "ast")
    assert freshness is GraphFreshness.AVAILABLE_AND_FRESH


def test_logically_undirected_graph_does_not_invent_direction(
    repository: Path, graph_path: Path
) -> None:
    payload = json.loads(graph_path.read_text(encoding="utf-8"))
    payload["directed"] = False
    graph_path.write_text(json.dumps(payload), encoding="utf-8")
    provider = GraphifyProvider(repository, graph_path, freshness_probe=fresh)

    assert provider.get_status().capabilities.dependencies is False
    reverse_path = provider.find_path("provider", "status")
    assert len(reverse_path.edges) == 1
    assert reverse_path.edges[0].source == "status"
    assert reverse_path.edges[0].relation == "USES"
    with pytest.raises(GraphUnavailableError):
        provider.get_dependencies("status")
    with pytest.raises(GraphUnavailableError):
        provider.get_neighbors("status", direction="outgoing")


def test_normal_path_is_confined(repository: Path) -> None:
    resolved = resolve_within_repository(repository, "graphify-out/graph.json")
    assert resolved == repository / "graphify-out" / "graph.json"


def test_relative_path_escape_is_rejected(repository: Path) -> None:
    with pytest.raises(PathBoundaryError):
        resolve_within_repository(repository, "../outside.json")


def test_absolute_path_escape_is_rejected(repository: Path, tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.json"
    with pytest.raises(PathBoundaryError):
        resolve_within_repository(repository, outside)


def test_symlink_escape_is_rejected(repository: Path, tmp_path: Path) -> None:
    target = tmp_path.parent / "outside-directory"
    target.mkdir(exist_ok=True)
    link = repository / "graphify-out"
    if os.name == "nt":
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
    else:
        os.symlink(target, link, target_is_directory=True)
    with pytest.raises(PathBoundaryError):
        resolve_within_repository(repository, "graphify-out/graph.json")


def test_disabled_provider_reports_no_capabilities(repository: Path) -> None:
    provider = build_graph_provider(repository, enabled=False)
    assert provider.get_status().availability is GraphAvailability.DISABLED
    assert not any(provider.get_status().capabilities.to_dict().values())
