from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from anti_ai_mcp.architecture import ArchitectureService
from anti_ai_mcp.checks import ProjectCheckService
from anti_ai_mcp.git import GitInspector
from anti_ai_mcp.graph import GraphFreshness, GraphifyProvider
from anti_ai_mcp.impact import ChangeImpactService
from anti_ai_mcp.status import AntiAiStatusService, StatusSettings
from conftest import write_graph_fixture


def fresh(*_args):
    return GraphFreshness.AVAILABLE_AND_FRESH, "fixture is current"


def test_multiple_concurrent_graph_reads_are_consistent(
    clean_repo: Path, linear_graph: dict
) -> None:
    graph_path = write_graph_fixture(clean_repo, linear_graph)
    provider = GraphifyProvider(clean_repo, graph_path, freshness_probe=fresh)

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(lambda _index: provider.query("src", limit=20), range(40)))

    signatures = {
        (tuple(node.id for node in result.nodes), tuple((edge.source, edge.target) for edge in result.edges))
        for result in results
    }
    assert len(signatures) == 1


def test_validation_and_graph_query_can_run_concurrently(
    validation_pass_repo: Path, linear_graph: dict
) -> None:
    graph_path = write_graph_fixture(validation_pass_repo, linear_graph)
    provider = GraphifyProvider(validation_pass_repo, graph_path, freshness_probe=fresh)
    checks = ProjectCheckService(validation_pass_repo)

    with ThreadPoolExecutor(max_workers=2) as executor:
        validation_future = executor.submit(checks.run, categories=["unit-tests"])
        graph_future = executor.submit(provider.query, "src")

    assert validation_future.result().status.value == "PASS"
    assert graph_future.result().nodes


def test_two_impact_analyses_are_independent(clean_repo: Path, linear_graph: dict) -> None:
    graph_path = write_graph_fixture(clean_repo, linear_graph)
    provider = GraphifyProvider(clean_repo, graph_path, freshness_probe=fresh)
    service = ChangeImpactService(GitInspector(clean_repo), provider)

    with ThreadPoolExecutor(max_workers=2) as executor:
        first = executor.submit(service.analyze, changed_files=["src/a.py"])
        second = executor.submit(service.analyze, changed_files=["src/b.py"])

    assert first.result().metadata["graph"]["coverage"]["matched_files"] == 1
    assert second.result().metadata["graph"]["coverage"]["matched_files"] == 1


def test_status_and_architecture_inspection_can_run_concurrently(
    repository: Path, plugin_root: Path, graph_path: Path
) -> None:
    provider = GraphifyProvider(repository, graph_path, freshness_probe=fresh)
    status = AntiAiStatusService(StatusSettings(repository, plugin_root), provider)
    architecture = ArchitectureService(GitInspector(repository), provider)

    with ThreadPoolExecutor(max_workers=2) as executor:
        status_future = executor.submit(status.get_status)
        architecture_future = executor.submit(architecture.inspect)

    assert status_future.result()["graph"]["availability"] == "available"
    assert architecture_future.result().metadata["graph"]["availability"] == "available"
