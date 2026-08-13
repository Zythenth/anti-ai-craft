from __future__ import annotations

from pathlib import Path
import subprocess

from anti_ai_mcp.git import GitInspector
from conftest import git


def test_clean_repository(clean_repo: Path) -> None:
    result = GitInspector(clean_repo).inspect("combined").to_dict()
    assert result["status"] == "PASS"
    assert result["metadata"]["clean"] is True
    assert result["metadata"]["files_changed"] == 0


def test_unstaged_change_is_normalized(modified_repo: Path) -> None:
    result = GitInspector(modified_repo).inspect("working_tree").to_dict()
    assert result["metadata"]["files"][0]["path"] == "README.md"
    assert result["metadata"]["files"][0]["status"] == "modified"
    assert result["metadata"]["lines_added"] == 1


def test_staged_change(clean_repo: Path) -> None:
    (clean_repo / "staged.txt").write_text("one\ntwo\n", encoding="utf-8")
    git(clean_repo, "add", "staged.txt")
    result = GitInspector(clean_repo).inspect("staged").to_dict()
    assert result["metadata"]["files"][0]["status"] == "added"
    assert result["metadata"]["files"][0]["staged"] is True
    assert result["metadata"]["lines_added"] == 2


def test_untracked_change(clean_repo: Path) -> None:
    (clean_repo / "new.txt").write_text("one\ntwo\n", encoding="utf-8")
    result = GitInspector(clean_repo).inspect("working_tree").to_dict()
    file = result["metadata"]["files"][0]
    assert file["status"] == "untracked"
    assert file["untracked"] is True
    assert file["lines_added"] == 2


def test_deleted_change(clean_repo: Path) -> None:
    (clean_repo / "README.md").unlink()
    result = GitInspector(clean_repo).inspect("combined").to_dict()
    assert result["metadata"]["files"][0]["status"] == "deleted"
    assert result["metadata"]["lines_removed"] == 1


def test_rename_preserves_both_paths(renamed_file_repo: Path) -> None:
    result = GitInspector(renamed_file_repo).inspect("combined").to_dict()
    file = result["metadata"]["files"][0]
    assert file["status"] == "renamed"
    assert file["old_path"] == "src/auth.py"
    assert file["path"] == "plugins/foo/auth.py"


def test_mixed_diff_reports_all_states(clean_repo: Path) -> None:
    (clean_repo / "README.md").write_text("staged\n", encoding="utf-8")
    git(clean_repo, "add", "README.md")
    (clean_repo / "README.md").write_text("staged\nunstaged\n", encoding="utf-8")
    (clean_repo / "new.txt").write_text("new\n", encoding="utf-8")
    result = GitInspector(clean_repo).inspect("combined").to_dict()
    readme = next(file for file in result["metadata"]["files"] if file["path"] == "README.md")
    assert readme["staged"] is True
    assert readme["unstaged"] is True
    assert result["metadata"]["diff_summary"]["untracked"] == 1


def test_removed_lines_preserve_original_location(clean_repo: Path) -> None:
    source = clean_repo / "src" / "guard.py"
    source.parent.mkdir()
    source.write_text("authorize(user)\nreturn_resource()\n", encoding="utf-8")
    git(clean_repo, "add", "src/guard.py")
    git(clean_repo, "commit", "-q", "-m", "add guard")
    source.write_text("return_resource()\n", encoding="utf-8")

    lines, truncated = GitInspector(clean_repo).removed_lines()

    assert truncated is False
    assert [(line.path, line.line_number, line.text) for line in lines] == [
        ("src/guard.py", 1, "authorize(user)")
    ]


def test_repository_without_commits_reports_untracked_files(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q")
    (tmp_path / "first.txt").write_text("first\n", encoding="utf-8")

    result = GitInspector(tmp_path).inspect().to_dict()

    assert result["status"] == "PASS"
    assert result["metadata"]["head"] is None
    assert result["metadata"]["files"][0]["status"] == "untracked"


def test_detached_head_is_reported_without_failure(clean_repo: Path) -> None:
    head = git(clean_repo, "rev-parse", "HEAD").stdout.strip()
    detached = subprocess.run(
        ["git", "-C", str(clean_repo), "checkout", "--detach", "-q", head],
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    assert detached.returncode == 0, detached.stderr

    result = GitInspector(clean_repo).inspect().to_dict()

    assert result["status"] == "PASS"
    assert result["metadata"]["branch"] is None
    assert result["metadata"]["head"] == head
