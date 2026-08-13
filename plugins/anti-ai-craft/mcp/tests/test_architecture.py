from __future__ import annotations

from pathlib import Path

from anti_ai_mcp.architecture import ArchitectureService
from anti_ai_mcp.git import GitInspector
from anti_ai_mcp.graph import GraphFreshness, GraphifyProvider, build_graph_provider
from conftest import git, write_graph_fixture


def fresh(*_args):
    return GraphFreshness.AVAILABLE_AND_FRESH, "fixture is current"


def stale(*_args):
    return GraphFreshness.AVAILABLE_BUT_STALE, "fixture is stale"


def service(repository: Path, payload: dict, probe=fresh) -> ArchitectureService:
    exclude = repository / ".git" / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    exclude.write_text("graphify-out/\n", encoding="utf-8")
    path = write_graph_fixture(repository, payload)
    provider = GraphifyProvider(repository, path, freshness_probe=probe)
    return ArchitectureService(GitInspector(repository), provider)


def commit_source(repository: Path, path: str) -> Path:
    target = repository / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("VALUE = 1\n", encoding="utf-8")
    git(repository, "add", path)
    git(repository, "commit", "-q", "-m", f"add {path}")
    return target


def test_inspect_architecture_reports_structural_clusters(
    clean_repo: Path, cross_community_change: dict
) -> None:
    result = service(clean_repo, cross_community_change).inspect().to_dict()
    assert result["status"] == "PASS"
    assert {item["id"] for item in result["metadata"]["communities"]} == {1, 2}
    assert result["metadata"]["relations_between_communities"][0]["bounded_edge_count"] == 1
    assert result["metadata"]["possible_entrypoints"] == []


def test_same_community_change_is_not_architecture_drift(
    clean_repo: Path, linear_graph: dict
) -> None:
    target = commit_source(clean_repo, "src/a.py")
    target.write_text("VALUE = 2\n", encoding="utf-8")
    result = service(clean_repo, linear_graph).audit().to_dict()
    ids = {finding["id"] for finding in result["findings"]}
    assert "AA-ARCH-002" not in ids
    assert "AA-ARCH-003" not in ids


def test_new_cross_community_relation_is_attributable(
    clean_repo: Path, cross_community_change: dict
) -> None:
    target = clean_repo / "src" / "new.py"
    target.parent.mkdir()
    target.write_text("VALUE = 1\n", encoding="utf-8")
    result = service(clean_repo, cross_community_change).audit().to_dict()
    finding = next(item for item in result["findings"] if item["id"] == "AA-ARCH-002")
    assert "structural cluster" in finding["message"]
    assert result["metadata"]["observations"]["new_cross_community_relations"] == 1


def test_cross_community_containment_is_not_a_dependency_signal(clean_repo: Path) -> None:
    target = clean_repo / "src" / "new.py"
    target.parent.mkdir()
    target.write_text("class Child: pass\n", encoding="utf-8")
    payload = {
        "directed": True,
        "multigraph": False,
        "graph": {},
        "nodes": [
            {"id": "module", "label": "new.py", "source_file": "src/new.py", "community": 1},
            {"id": "child", "label": "Child", "source_file": "src/new.py", "community": 2},
        ],
        "links": [
            {"source": "module", "target": "child", "relation": "contains", "confidence": "EXTRACTED"}
        ],
    }

    result = service(clean_repo, payload).audit().to_dict()

    assert "AA-ARCH-002" not in {finding["id"] for finding in result["findings"]}
    assert result["metadata"]["observations"]["ignored_containment_relations"] == 1


def test_modified_cross_community_relation_is_not_claimed_as_new(
    clean_repo: Path, cross_community_change: dict
) -> None:
    target = commit_source(clean_repo, "src/new.py")
    target.write_text("VALUE = 2\n", encoding="utf-8")
    result = service(clean_repo, cross_community_change).audit().to_dict()
    ids = {finding["id"] for finding in result["findings"]}
    assert "AA-ARCH-002" not in ids
    assert result["metadata"]["observations"]["existing_or_undetermined_cross_community_relations"] == 1
    assert "cannot be distinguished" in result["metadata"]["structural_delta"]["modified_file_relations"]


def test_directed_cycle_is_reported_only_with_reliable_direction(
    clean_repo: Path, cyclic_graph: dict
) -> None:
    target = clean_repo / "src" / "a.py"
    target.parent.mkdir()
    target.write_text("VALUE = 1\n", encoding="utf-8")
    directed = service(clean_repo, cyclic_graph).audit().to_dict()
    assert "AA-ARCH-003" in {finding["id"] for finding in directed["findings"]}

    cyclic_graph["directed"] = False
    undirected = service(clean_repo, cyclic_graph).audit().to_dict()
    assert "AA-ARCH-003" not in {finding["id"] for finding in undirected["findings"]}
    assert undirected["metadata"]["observations"]["directed_cycles_checked"] is False


def test_stale_architecture_analysis_warns(
    clean_repo: Path, stale_graph: dict
) -> None:
    result = service(clean_repo, stale_graph, stale).inspect().to_dict()
    assert result["status"] == "WARNING"
    assert result["metadata"]["graph"]["freshness"] == "available_but_stale"
    assert result["metadata"]["warnings"]


def test_no_graph_requires_manual_review(clean_repo: Path) -> None:
    provider = build_graph_provider(clean_repo, enabled=False)
    result = ArchitectureService(GitInspector(clean_repo), provider).inspect().to_dict()
    assert result["status"] == "MANUAL_REVIEW_REQUIRED"
    assert result["metadata"]["graph"]["availability"] == "disabled"
