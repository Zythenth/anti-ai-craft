from __future__ import annotations

import json
from pathlib import Path

from anti_ai_mcp.repository import RepositoryInspector


def inspect(root: Path):
    return RepositoryInspector(root, root / "plugins" / "anti-ai-craft").inspect().to_dict()


def test_empty_simple_repository_without_git(tmp_path: Path) -> None:
    result = inspect(tmp_path)
    assert result["status"] == "PASS"
    assert result["metadata"]["repository"]["git"]["repository"] is False
    assert result["metadata"]["languages"] == []


def test_python_repository_detects_manifest_framework_and_tests(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname='fixture'\nversion='0.0.0'\n"
        "dependencies=['fastapi>=1']\n[dependency-groups]\ndev=['pytest>=8']\n",
        encoding="utf-8",
    )
    (tmp_path / "uv.lock").write_text("version = 1\n", encoding="utf-8")
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_app.py").write_text("def test_app(): pass\n", encoding="utf-8")
    result = inspect(tmp_path)
    assert result["metadata"]["languages"][0]["name"] == "Python"
    assert {item["name"] for item in result["metadata"]["frameworks"]} == {"FastAPI", "pytest"}
    assert result["metadata"]["tests"]["file_count"] == 1
    assert result["metadata"]["package_managers"] == [{"name": "uv", "evidence": "uv.lock"}]


def test_node_repository_uses_dependencies_not_folder_names(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(
        json.dumps(
            {
                "dependencies": {"react": "1.0.0"},
                "scripts": {"lint": "eslint .", "test": "vitest"},
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "package-lock.json").write_text("{}", encoding="utf-8")
    (tmp_path / "next").mkdir()
    result = inspect(tmp_path)
    assert [item["name"] for item in result["metadata"]["frameworks"]] == ["React"]
    assert {item["name"] for item in result["metadata"]["scripts"]} == {"lint", "test"}
    assert result["metadata"]["package_managers"] == [
        {"name": "npm", "evidence": "package-lock.json"}
    ]


def test_mixed_multi_package_repository_reports_each_manifest(tmp_path: Path) -> None:
    for directory in (tmp_path / "a", tmp_path / "b"):
        directory.mkdir()
        (directory / "pyproject.toml").write_text(
            "[project]\nname='fixture'\nversion='0.0.0'\n", encoding="utf-8"
        )
        (directory / "uv.lock").write_text("version = 1\n", encoding="utf-8")
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    result = inspect(tmp_path)
    assert result["metadata"]["manifests"] == [
        "a/pyproject.toml",
        "b/pyproject.toml",
        "package.json",
    ]
    assert [item["evidence"] for item in result["metadata"]["package_managers"]] == [
        "a/uv.lock",
        "b/uv.lock",
    ]


def test_ci_and_documentation_detection(tmp_path: Path) -> None:
    workflow = tmp_path / ".github" / "workflows" / "test.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("name: test\n", encoding="utf-8")
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "guide.md").write_text("# Guide\n", encoding="utf-8")
    result = inspect(tmp_path)
    assert result["metadata"]["ci"] == {
        "detected": True,
        "files": [".github/workflows/test.yml"],
    }
    assert result["metadata"]["documentation"] == ["docs/guide.md"]


def test_invalid_manifest_is_not_silently_ignored(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text("{", encoding="utf-8")
    result = inspect(tmp_path)
    assert result["status"] == "WARNING"
    assert result["findings"][0]["id"] == "AA-REPO-002"
    assert result["metadata"]["manifest_errors"] == ["package.json"]
