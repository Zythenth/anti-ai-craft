from __future__ import annotations

from pathlib import Path

from anti_ai_mcp.anti_ai_audit import AntiAiAuditService
from anti_ai_mcp.architecture import ArchitectureService
from anti_ai_mcp.git import GitInspector
from anti_ai_mcp.graph import GraphFreshness, GraphifyProvider, build_graph_provider
from conftest import edge, git, graph_payload, node, write_graph_fixture


def fresh(*_args):
    return GraphFreshness.AVAILABLE_AND_FRESH, "fixture is current"


def ignore_graph(repository: Path) -> None:
    path = repository / ".gitignore"
    if path.exists():
        return
    path.write_text("graphify-out/\n", encoding="utf-8")
    git(repository, "add", ".gitignore")
    git(repository, "commit", "-q", "-m", "ignore graph cache")


def service(repository: Path, payload: dict | None, *, graph_enabled: bool = True) -> AntiAiAuditService:
    ignore_graph(repository)
    if graph_enabled:
        path = write_graph_fixture(repository, payload or graph_payload([], []))
        provider = GraphifyProvider(repository, path, freshness_probe=fresh)
    else:
        provider = build_graph_provider(repository, enabled=False)
    inspector = GitInspector(repository)
    architecture = ArchitectureService(inspector, provider)
    return AntiAiAuditService(repository, inspector, provider, architecture)


def ids(result: dict) -> set[str]:
    return {finding["id"] for finding in result["findings"]}


def test_new_placeholder_is_reported_but_preexisting_placeholder_is_not(
    clean_repo: Path
) -> None:
    source = clean_repo / "src" / "service.py"
    source.parent.mkdir()
    source.write_text("# TODO: legacy\nVALUE = 1\n", encoding="utf-8")
    git(clean_repo, "add", "src/service.py")
    git(clean_repo, "commit", "-q", "-m", "legacy placeholder")
    source.write_text("# TODO: legacy\nVALUE = 2\n", encoding="utf-8")
    payload = graph_payload([node("service", "src/service.py", 1)], [])

    preexisting = service(clean_repo, payload).audit().to_dict()
    assert "AA-AI-PLACEHOLDER-001" not in ids(preexisting)

    source.write_text("# TODO: legacy\nVALUE = 2\n# FIXME: new gap\n", encoding="utf-8")
    introduced = service(clean_repo, payload).audit().to_dict()
    finding = next(item for item in introduced["findings"] if item["id"] == "AA-AI-PLACEHOLDER-001")
    assert finding["evidence"][0]["kind"] == "HEURISTIC"
    assert finding["location"]["line"] == 3


def test_intentional_not_implemented_signal_remains_ambiguous(clean_repo: Path) -> None:
    source = clean_repo / "src" / "base.py"
    source.parent.mkdir()
    source.write_text(
        "class Base:\n    def run(self):\n        raise NotImplementedError\n",
        encoding="utf-8",
    )
    payload = graph_payload([node("base", "src/base.py", 1)], [])
    result = service(clean_repo, payload).audit().to_dict()
    assert "AA-AI-PLACEHOLDER-001" in ids(result)
    policy = result["metadata"]["rule_policies"]["AA-AI-PLACEHOLDER-001"]
    assert "cannot_prove" in policy
    assert "intentional abstract methods" in policy["known_false_positives"]


def test_test_skip_and_deleted_test_are_current_change_signals(clean_repo: Path) -> None:
    test = clean_repo / "tests" / "test_service.py"
    test.parent.mkdir()
    test.write_text("def test_service():\n    assert True\n", encoding="utf-8")
    git(clean_repo, "add", "tests/test_service.py")
    git(clean_repo, "commit", "-q", "-m", "add test")
    test.write_text("import pytest\n\n@pytest.mark.skip\ndef test_service(): pass\n", encoding="utf-8")
    payload = graph_payload([node("test", "tests/test_service.py", 1)], [])
    skipped = service(clean_repo, payload).audit().to_dict()
    assert "AA-AI-TEST-BYPASS-001" in ids(skipped)

    test.unlink()
    deleted = service(clean_repo, payload).audit().to_dict()
    finding = next(item for item in deleted["findings"] if item["id"] == "AA-AI-TEST-BYPASS-001")
    assert finding["evidence"][0]["kind"] == "FACT"


def test_preexisting_skip_is_not_attributed_to_current_change(clean_repo: Path) -> None:
    test = clean_repo / "tests" / "test_service.py"
    test.parent.mkdir()
    test.write_text(
        "import pytest\n\n@pytest.mark.skip\ndef test_service(): pass\n",
        encoding="utf-8",
    )
    git(clean_repo, "add", "tests/test_service.py")
    git(clean_repo, "commit", "-q", "-m", "preexisting skip")
    (clean_repo / "README.md").write_text("changed\n", encoding="utf-8")
    result = service(clean_repo, graph_payload([node("test", "tests/test_service.py", 1)], [])).audit().to_dict()
    assert "AA-AI-TEST-BYPASS-001" not in ids(result)


def test_compound_file_proliferation_requires_graph_isolation(clean_repo: Path) -> None:
    nodes = []
    for index in range(6):
        path = f"src/part_{index}.py"
        target = clean_repo / path
        target.parent.mkdir(exist_ok=True)
        target.write_text(f"def part_{index}():\n    return {index}\n", encoding="utf-8")
        nodes.append(node(f"part_{index}", path, 1))
    result = service(clean_repo, graph_payload(nodes, [])).audit().to_dict()
    assert "AA-AI-FILE-PROLIFERATION-001" in ids(result)
    policy = result["metadata"]["rule_policies"]["AA-AI-FILE-PROLIFERATION-001"]
    assert "generated code" in policy["known_false_positives"]


def test_file_count_alone_does_not_trigger_proliferation(clean_repo: Path) -> None:
    nodes = []
    links = []
    for index in range(6):
        path = f"src/part_{index}.py"
        target = clean_repo / path
        target.parent.mkdir(exist_ok=True)
        target.write_text(f"def part_{index}():\n    return {index}\n", encoding="utf-8")
        nodes.append(node(f"part_{index}", path, 1))
        if index:
            links.append(edge("part_0", f"part_{index}"))
    result = service(clean_repo, graph_payload(nodes, links)).audit().to_dict()
    assert "AA-AI-FILE-PROLIFERATION-001" not in ids(result)


def test_generated_files_are_excluded_from_proliferation(clean_repo: Path) -> None:
    nodes = []
    for index in range(6):
        path = f"src/generated_{index}.py"
        target = clean_repo / path
        target.parent.mkdir(exist_ok=True)
        target.write_text(f"def generated_{index}(): pass\n", encoding="utf-8")
        nodes.append(node(f"generated_{index}", path, 1))
    result = service(clean_repo, graph_payload(nodes, [])).audit().to_dict()
    assert "AA-AI-FILE-PROLIFERATION-001" not in ids(result)


def test_isolated_new_abstraction_is_heuristic(
    clean_repo: Path, isolated_new_abstraction: dict
) -> None:
    target = clean_repo / "src" / "isolated.py"
    target.parent.mkdir()
    target.write_text("class Isolated:\n    pass\n", encoding="utf-8")
    result = service(clean_repo, isolated_new_abstraction).audit().to_dict()
    finding = next(item for item in result["findings"] if item["id"] == "AA-AI-ABSTRACTION-001")
    assert finding["confidence"] == "MEDIUM"
    assert finding["evidence"][0]["payload"]["direction"] == "KNOWN"
    assert "runtime use" in result["metadata"]["rule_policies"]["AA-AI-ABSTRACTION-001"]["cannot_prove"]


def test_linked_or_preexisting_abstraction_is_not_reported(clean_repo: Path) -> None:
    target = clean_repo / "src" / "service.py"
    target.parent.mkdir()
    target.write_text("class Service:\n    pass\n", encoding="utf-8")
    git(clean_repo, "add", "src/service.py")
    git(clean_repo, "commit", "-q", "-m", "existing abstraction")
    target.write_text("class Service:\n    VALUE = 1\n", encoding="utf-8")
    payload = graph_payload(
        [node("service", "src/service.py", 1), node("consumer", "src/consumer.py", 1)],
        [edge("consumer", "service")],
    )
    result = service(clean_repo, payload).audit().to_dict()
    assert "AA-AI-ABSTRACTION-001" not in ids(result)


def test_possible_required_protocol_is_ambiguous_and_excluded(clean_repo: Path) -> None:
    target = clean_repo / "src" / "protocol.py"
    target.parent.mkdir()
    target.write_text("class ServiceProtocol:\n    pass\n", encoding="utf-8")
    payload = graph_payload([node("protocol", "src/protocol.py", 1)], [])
    result = service(clean_repo, payload).audit().to_dict()
    assert "AA-AI-ABSTRACTION-001" not in ids(result)


def test_graph_off_keeps_deterministic_placeholder_rule(clean_repo: Path) -> None:
    target = clean_repo / "src" / "service.py"
    target.parent.mkdir()
    target.write_text("# TODO: implement\n", encoding="utf-8")
    result = service(clean_repo, None, graph_enabled=False).audit().to_dict()
    assert result["status"] == "WARNING"
    assert "AA-AI-PLACEHOLDER-001" in ids(result)
    assert result["metadata"]["deterministic_evidence_available"] is True
    assert result["metadata"]["graph_evidence_available"] is False


def test_new_source_file_inspection_has_explicit_limit(clean_repo: Path) -> None:
    source = clean_repo / "src"
    source.mkdir()
    for index in range(101):
        (source / f"part_{index:03}.py").write_text(
            f"VALUE = {index}\n",
            encoding="utf-8",
        )

    result = service(clean_repo, graph_payload([], [])).audit().to_dict()

    assert result["status"] == "WARNING"
    assert result["metadata"]["limits"]["truncated"] is True
    assert result["metadata"]["graph"]["coverage"]["new_source_files"] == 100
    assert any(
        "New-source-file inspection reached" in warning
        for warning in result["metadata"]["warnings"]
    )
