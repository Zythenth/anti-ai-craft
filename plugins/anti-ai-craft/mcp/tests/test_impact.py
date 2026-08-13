from __future__ import annotations

from pathlib import Path

import pytest

from anti_ai_mcp.git import GitInspector
from anti_ai_mcp.graph import GraphFreshness, GraphifyProvider, build_graph_provider
from anti_ai_mcp.impact import ChangeImpactService, GraphImpactAnalyzer
from conftest import write_graph_fixture


def fresh(*_args):
    return GraphFreshness.AVAILABLE_AND_FRESH, "fixture is current"


def stale(*_args):
    return GraphFreshness.AVAILABLE_BUT_STALE, "fixture is stale"


def unknown(*_args):
    return GraphFreshness.UNKNOWN_FRESHNESS, "fixture freshness is unknown"


def service(repository: Path, payload: dict, probe=fresh) -> ChangeImpactService:
    path = write_graph_fixture(repository, payload)
    provider = GraphifyProvider(repository, path, freshness_probe=probe)
    return ChangeImpactService(GitInspector(repository), provider)


def test_direct_two_hop_and_affected_test_are_bounded(
    clean_repo: Path, linear_graph: dict
) -> None:
    result = service(clean_repo, linear_graph).analyze(
        changed_files=["src/a.py"], max_depth=2
    ).to_dict()

    assert result["status"] == "PASS"
    direct = result["metadata"]["direct_structural_neighbors"]
    indirect = result["metadata"]["indirectly_reachable_nodes"]
    assert [item["node"]["id"] for item in direct] == ["b"]
    assert direct[0]["impact"] == "DIRECT"
    assert direct[0]["evidence_kind"] == "FACT"
    assert direct[0]["relations"][0]["payload"]["direction"] == "OUTGOING"
    assert [item["node"]["id"] for item in indirect] == ["test_b"]
    assert indirect[0]["impact"] == "LIKELY_INDIRECT"
    assert result["metadata"]["candidate_affected_tests"][0]["test_path"] == "tests/test_b.py"
    assert result["metadata"]["graph"]["coverage"]["matched_files"] == 1


def test_distance_limit_stops_two_hop_candidate(clean_repo: Path, linear_graph: dict) -> None:
    result = service(clean_repo, linear_graph).analyze(
        changed_files=["src/a.py"], max_depth=1
    ).to_dict()
    assert result["metadata"]["indirectly_reachable_nodes"] == []
    assert result["metadata"]["candidate_affected_tests"] == []


def test_multiple_changed_nodes_are_seeds(clean_repo: Path, linear_graph: dict) -> None:
    result = service(clean_repo, linear_graph).analyze(
        changed_files=["src/a.py", "src/b.py"], max_depth=1
    ).to_dict()
    assert result["metadata"]["graph"]["coverage"]["matched_files"] == 2
    assert {node["id"] for node in result["metadata"]["changed_nodes"]} == {"a", "b"}
    assert [item["node"]["id"] for item in result["metadata"]["direct_structural_neighbors"]] == ["test_b"]


def test_missing_changed_node_requires_manual_review(clean_repo: Path, linear_graph: dict) -> None:
    result = service(clean_repo, linear_graph).analyze(
        changed_files=["src/missing.py"]
    ).to_dict()
    assert result["status"] == "MANUAL_REVIEW_REQUIRED"
    assert result["findings"][0]["id"] == "AA-IMPACT-002"
    assert result["metadata"]["graph"]["coverage"]["missing_files"] == ["src/missing.py"]


@pytest.mark.parametrize(
    ("probe", "freshness", "direct_confidence"),
    [
        (stale, "available_but_stale", "MEDIUM"),
        (unknown, "unknown_freshness", "MEDIUM"),
    ],
)
def test_non_fresh_graph_warns_and_reduces_confidence(
    clean_repo: Path,
    stale_graph: dict,
    probe,
    freshness: str,
    direct_confidence: str,
) -> None:
    result = service(clean_repo, stale_graph, probe).analyze(
        changed_files=["src/a.py"]
    ).to_dict()
    assert result["status"] == "WARNING"
    assert result["metadata"]["graph"]["freshness"] == freshness
    assert result["metadata"]["direct_structural_neighbors"][0]["confidence"] == direct_confidence
    assert result["metadata"]["warnings"]


def test_graph_off_degrades_without_structural_conclusion(clean_repo: Path) -> None:
    provider = build_graph_provider(clean_repo, enabled=False)
    result = ChangeImpactService(GitInspector(clean_repo), provider).analyze(
        changed_files=["src/a.py"]
    ).to_dict()
    assert result["status"] == "MANUAL_REVIEW_REQUIRED"
    assert result["findings"][0]["id"] == "AA-IMPACT-001"
    assert result["metadata"]["graph"]["availability"] == "disabled"


def test_inferred_edge_remains_inference(
    clean_repo: Path, inferred_edges_graph: dict
) -> None:
    result = service(clean_repo, inferred_edges_graph).analyze(
        changed_files=["src/a.py"]
    ).to_dict()
    candidate = result["metadata"]["direct_structural_neighbors"][0]
    assert candidate["evidence_kind"] == "INFERENCE"
    assert candidate["relations"][0]["payload"]["graph_provenance"] == "INFERRED"


def test_undirected_relation_never_becomes_dependency(
    clean_repo: Path, undirected_graph: dict
) -> None:
    result = service(clean_repo, undirected_graph).analyze(
        changed_files=["src/a.py"], max_depth=1
    ).to_dict()
    relation = result["metadata"]["direct_structural_neighbors"][0]["relations"][0]
    assert relation["payload"]["direction"] == "UNKNOWN"
    assert result["metadata"]["graph"]["directed"] is False
    assert any("direction is unknown" in warning for warning in result["metadata"]["warnings"])


def test_large_fanout_is_explicitly_truncated(
    clean_repo: Path, large_fanout_graph: dict
) -> None:
    result = service(clean_repo, large_fanout_graph).analyze(
        changed_files=["src/root.py"], max_depth=1
    ).to_dict()
    assert result["status"] == "WARNING"
    assert result["metadata"]["limits"]["truncated"] is True
    assert result["findings"][0]["id"] == "AA-IMPACT-004"


def test_invalid_depth_is_rejected(clean_repo: Path, linear_graph: dict) -> None:
    result = service(clean_repo, linear_graph).analyze(
        changed_files=["src/a.py"], max_depth=4
    ).to_dict()
    assert result["status"] == "ERROR"
    assert result["errors"][0]["code"] == "AA-IMPACT-INPUT"


def test_internal_analyzer_caps_changed_files(clean_repo: Path, linear_graph: dict) -> None:
    path = write_graph_fixture(clean_repo, linear_graph)
    provider = GraphifyProvider(clean_repo, path, freshness_probe=fresh)
    files = ["src/a.py", *(f"src/missing_{index}.py" for index in range(100))]

    analysis = GraphImpactAnalyzer(provider).analyze(files, max_depth=1)

    assert analysis.truncated is True
    assert analysis.coverage["changed_files"] == 101
    assert analysis.coverage["analyzed_files"] == 100
    assert any("first 100" in warning for warning in analysis.warnings)
