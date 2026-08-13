from __future__ import annotations

from pathlib import Path

from anti_ai_mcp.git import GitInspector
from anti_ai_mcp.scope import ScopeVerifier


def verify(repository: Path, **kwargs):
    return ScopeVerifier(GitInspector(repository)).verify(**kwargs).to_dict()


def test_allowed_exact_file(modified_repo: Path) -> None:
    result = verify(modified_repo, allowed=["README.md"])
    assert result["status"] == "PASS"
    assert result["metadata"]["authorized"] == ["README.md"]


def test_allowed_directory_and_new_file(clean_repo: Path) -> None:
    path = clean_repo / "src" / "feature.py"
    path.parent.mkdir()
    path.write_text("VALUE = 1\n", encoding="utf-8")
    result = verify(clean_repo, allowed=["src"])
    assert result["status"] == "PASS"


def test_allowed_glob_and_multiple_globs(clean_repo: Path) -> None:
    (clean_repo / "README.md").write_text("changed\n", encoding="utf-8")
    test = clean_repo / "tests" / "test_feature.py"
    test.parent.mkdir()
    test.write_text("def test_feature(): pass\n", encoding="utf-8")
    result = verify(clean_repo, allowed=["*.md", "tests/**"])
    assert result["status"] == "PASS"


def test_exception_removes_path_from_allowed_scope(clean_repo: Path) -> None:
    path = clean_repo / "src" / "generated" / "file.py"
    path.parent.mkdir(parents=True)
    path.write_text("VALUE = 1\n", encoding="utf-8")
    result = verify(clean_repo, allowed=["src/**"], exceptions=["src/generated/**"])
    assert result["status"] == "FAIL"
    assert result["findings"][0]["id"] == "AA-SCOPE-001"


def test_explicit_deny_takes_precedence(modified_repo: Path) -> None:
    result = verify(modified_repo, allowed=["**"], denied=["README.md"])
    assert result["status"] == "FAIL"
    assert result["findings"][0]["id"] == "AA-SCOPE-002"


def test_deleted_file_is_checked(clean_repo: Path) -> None:
    (clean_repo / "README.md").unlink()
    result = verify(clean_repo, allowed=["README.md"])
    assert result["status"] == "PASS"


def test_rename_cannot_escape_through_allowed_destination(renamed_file_repo: Path) -> None:
    result = verify(renamed_file_repo, allowed=["plugins/foo/**"])
    assert result["status"] == "FAIL"
    assert "src/auth.py" in result["metadata"]["violations"]
    assert result["metadata"]["changed"][0]["old_path"] == "src/auth.py"


def test_rename_passes_when_source_and_destination_are_allowed(renamed_file_repo: Path) -> None:
    result = verify(renamed_file_repo, allowed=["src/**", "plugins/foo/**"])
    assert result["status"] == "PASS"


def test_scope_patterns_normalize_windows_separators(clean_repo: Path) -> None:
    path = clean_repo / "src" / "feature.py"
    path.parent.mkdir()
    path.write_text("VALUE = 1\n", encoding="utf-8")
    result = verify(clean_repo, allowed=[r"src\**"])
    assert result["status"] == "PASS"


def test_scope_pattern_traversal_is_rejected(modified_repo: Path) -> None:
    result = verify(modified_repo, allowed=["../outside/**"])
    assert result["status"] == "ERROR"
    assert result["errors"][0]["code"] == "AA-SCOPE-INPUT"


def test_invalid_scope_glob_is_reported_as_input_error(modified_repo: Path) -> None:
    result = verify(modified_repo, allowed=["[z-a]"])
    assert result["status"] == "ERROR"
    assert result["errors"][0]["code"] == "AA-SCOPE-INPUT"
