from __future__ import annotations

from pathlib import Path

from anti_ai_mcp.checks import ProjectCheckService
from anti_ai_mcp.git import GitInspector
from anti_ai_mcp.relevant_tests import RelevantTestService
from conftest import git


def configure_pytest(repository: Path) -> None:
    (repository / "pyproject.toml").write_text(
        "[project]\nname='fixture'\nversion='0.0.0'\n"
        "[dependency-groups]\ndev=['pytest>=8']\n",
        encoding="utf-8",
    )


def service(repository: Path) -> RelevantTestService:
    checks = ProjectCheckService(repository)
    return RelevantTestService(repository, GitInspector(repository), checks)


def commit_fixture(repository: Path) -> None:
    git(repository, "add", ".")
    git(repository, "commit", "-q", "-m", "test mapping fixture")


def test_direct_module_mapping(clean_repo: Path) -> None:
    configure_pytest(clean_repo)
    source = clean_repo / "src" / "orders" / "service.py"
    test = clean_repo / "tests" / "orders" / "test_service.py"
    source.parent.mkdir(parents=True)
    test.parent.mkdir(parents=True)
    source.write_text("VALUE = 1\n", encoding="utf-8")
    test.write_text("def test_service(): pass\n", encoding="utf-8")
    commit_fixture(clean_repo)
    source.write_text("VALUE = 2\n", encoding="utf-8")

    result = service(clean_repo).run(dry_run=True).to_dict()
    assert result["status"] == "PASS"
    assert result["metadata"]["selection_reason"][0]["reason"] == "matching module path"
    assert result["metadata"]["selected_checks"][0]["command"][-1] == "tests/orders/test_service.py"


def test_directory_mapping(clean_repo: Path) -> None:
    configure_pytest(clean_repo)
    source = clean_repo / "packages" / "orders" / "service.py"
    test = clean_repo / "tests" / "orders" / "test_service.py"
    source.parent.mkdir(parents=True)
    test.parent.mkdir(parents=True)
    source.write_text("VALUE = 1\n", encoding="utf-8")
    test.write_text("def test_service(): pass\n", encoding="utf-8")
    commit_fixture(clean_repo)
    source.write_text("VALUE = 2\n", encoding="utf-8")

    result = service(clean_repo).run(dry_run=True).to_dict()
    assert result["metadata"]["selection_reason"][0]["reason"] == "matching module directory"


def test_no_mapping_requires_manual_review(clean_repo: Path) -> None:
    (clean_repo / "README.md").write_text("changed\n", encoding="utf-8")
    result = service(clean_repo).run(dry_run=True).to_dict()
    assert result["status"] == "MANUAL_REVIEW_REQUIRED"
    assert result["findings"][0]["id"] == "AA-TEST-004"


def test_multiple_mappings_are_all_selected(clean_repo: Path) -> None:
    configure_pytest(clean_repo)
    source = clean_repo / "src" / "service.py"
    first = clean_repo / "tests" / "test_service.py"
    second = clean_repo / "package" / "tests" / "test_service.py"
    source.parent.mkdir()
    first.parent.mkdir()
    second.parent.mkdir(parents=True)
    source.write_text("VALUE = 1\n", encoding="utf-8")
    first.write_text("def test_one(): pass\n", encoding="utf-8")
    second.write_text("def test_two(): pass\n", encoding="utf-8")
    commit_fixture(clean_repo)
    source.write_text("VALUE = 2\n", encoding="utf-8")

    result = service(clean_repo).run(dry_run=True).to_dict()
    selected = result["metadata"]["selected_checks"][0]["command"]
    assert "tests/test_service.py" in selected
    assert "package/tests/test_service.py" in selected
    assert len(result["metadata"]["selection_reason"]) == 2


def test_fallback_package_suite_is_explicit(clean_repo: Path) -> None:
    configure_pytest(clean_repo)
    tests = clean_repo / "tests"
    tests.mkdir()
    (tests / "test_unrelated.py").write_text("def test_unrelated(): pass\n", encoding="utf-8")
    commit_fixture(clean_repo)
    (clean_repo / "README.md").write_text("changed\n", encoding="utf-8")

    result = service(clean_repo).run(dry_run=True).to_dict()
    assert result["status"] == "WARNING"
    assert result["findings"][0]["id"] == "AA-TEST-005"
    assert "package test suite" in result["metadata"]["selection_reason"][0]["reason"]


def test_partial_direct_mapping_broadens_to_safe_suite(clean_repo: Path) -> None:
    configure_pytest(clean_repo)
    source = clean_repo / "src" / "service.py"
    mapped = clean_repo / "tests" / "test_service.py"
    unmapped = clean_repo / "src" / "without_coverage.py"
    source.parent.mkdir()
    mapped.parent.mkdir()
    source.write_text("VALUE = 1\n", encoding="utf-8")
    unmapped.write_text("VALUE = 1\n", encoding="utf-8")
    mapped.write_text("def test_service(): pass\n", encoding="utf-8")
    commit_fixture(clean_repo)
    source.write_text("VALUE = 2\n", encoding="utf-8")
    unmapped.write_text("VALUE = 2\n", encoding="utf-8")

    result = service(clean_repo).run(dry_run=True).to_dict()
    assert result["status"] == "WARNING"
    assert result["metadata"]["selected_checks"][0]["command"][-2:] == ["-m", "pytest"]
    assert any(
        reason["changed_path"] == "src/without_coverage.py"
        and "package test suite" in reason["reason"]
        for reason in result["metadata"]["selection_reason"]
    )
