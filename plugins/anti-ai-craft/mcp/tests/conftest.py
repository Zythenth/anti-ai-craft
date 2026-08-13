from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest


def git(repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    assert result.returncode == 0, result.stderr
    return result


@pytest.fixture
def clean_repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "tests@example.invalid")
    git(tmp_path, "config", "user.name", "Anti-AI Tests")
    (tmp_path / "README.md").write_text("fixture\n", encoding="utf-8")
    git(tmp_path, "add", "README.md")
    git(tmp_path, "commit", "-q", "-m", "fixture")
    return tmp_path


@pytest.fixture
def modified_repo(clean_repo: Path) -> Path:
    (clean_repo / "README.md").write_text("fixture\nmodified\n", encoding="utf-8")
    return clean_repo


@pytest.fixture
def renamed_file_repo(clean_repo: Path) -> Path:
    source = clean_repo / "src" / "auth.py"
    source.parent.mkdir()
    source.write_text("TOKEN = 1\n", encoding="utf-8")
    git(clean_repo, "add", "src/auth.py")
    git(clean_repo, "commit", "-q", "-m", "add source")
    destination = clean_repo / "plugins" / "foo" / "auth.py"
    destination.parent.mkdir(parents=True)
    git(clean_repo, "mv", "src/auth.py", "plugins/foo/auth.py")
    return clean_repo


def make_python_validation_repo(root: Path, test_body: str) -> Path:
    (root / "pyproject.toml").write_text(
        "[project]\nname='fixture'\nversion='0.0.0'\n"
        "[dependency-groups]\ndev=['pytest>=8']\n",
        encoding="utf-8",
    )
    tests = root / "tests"
    tests.mkdir()
    (tests / "test_validation.py").write_text(test_body, encoding="utf-8")
    return root


@pytest.fixture
def validation_pass_repo(clean_repo: Path) -> Path:
    return make_python_validation_repo(clean_repo, "def test_pass():\n    assert True\n")


@pytest.fixture
def validation_fail_repo(clean_repo: Path) -> Path:
    return make_python_validation_repo(clean_repo, "def test_fail():\n    assert False\n")


@pytest.fixture
def validation_timeout_repo(clean_repo: Path) -> Path:
    return make_python_validation_repo(
        clean_repo,
        "import time\n\ndef test_timeout():\n    time.sleep(2)\n",
    )


@pytest.fixture
def large_output_repo(clean_repo: Path) -> Path:
    return make_python_validation_repo(
        clean_repo,
        "import sys\n\ndef test_output():\n"
        "    print('O' * 200000)\n"
        "    sys.stderr.write('E' * 200000)\n"
        "    assert False\n",
    )


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    (tmp_path / ".git").mkdir()
    return tmp_path


@pytest.fixture
def plugin_root(repository: Path) -> Path:
    root = repository / "plugins" / "anti-ai-craft"
    (root / ".codex-plugin").mkdir(parents=True)
    (root / "skills" / "anti-ai-code").mkdir(parents=True)
    (root / ".codex-plugin" / "plugin.json").write_text(
        json.dumps({"version": "0.5.0"}), encoding="utf-8"
    )
    (root / "skills" / "anti-ai-code" / "SKILL.md").write_text(
        "# Test skill\n", encoding="utf-8"
    )
    return root


@pytest.fixture
def graph_path(repository: Path) -> Path:
    path = repository / "graphify-out" / "graph.json"
    path.parent.mkdir()
    payload = {
        "directed": True,
        "multigraph": False,
        "graph": {},
        "nodes": [
            {
                "id": "provider",
                "label": "GraphifyProvider",
                "source_file": "src/graph.py",
                "community": 1,
                "confidence": "EXTRACTED",
            },
            {
                "id": "status",
                "label": "AntiAiStatusService",
                "source_file": "src/status.py",
                "community": 1,
                "confidence": "INFERRED",
            },
        ],
        "links": [
            {
                "source": "status",
                "target": "provider",
                "relation": "USES",
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
            }
        ],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
