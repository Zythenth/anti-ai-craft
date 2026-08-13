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
        json.dumps({"version": "0.6.0"}), encoding="utf-8"
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


def write_graph_fixture(root: Path, payload: dict) -> Path:
    path = root / "graphify-out" / "graph.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def graph_payload(nodes: list[dict], links: list[dict], *, directed: bool = True) -> dict:
    return {
        "directed": directed,
        "multigraph": False,
        "graph": {},
        "nodes": nodes,
        "links": links,
    }


def node(identifier: str, path: str, community: int, *, label: str | None = None) -> dict:
    return {
        "id": identifier,
        "label": label or identifier,
        "source_file": path,
        "source_location": "L1",
        "community": community,
        "community_name": f"cluster-{community}",
    }


def edge(source: str, target: str, *, confidence: str = "EXTRACTED") -> dict:
    return {
        "source": source,
        "target": target,
        "relation": "uses",
        "confidence": confidence,
        "confidence_score": 1.0 if confidence == "EXTRACTED" else 0.5,
    }


@pytest.fixture
def linear_graph() -> dict:
    return graph_payload(
        [
            node("a", "src/a.py", 1),
            node("b", "src/b.py", 1),
            node("test_b", "tests/test_b.py", 2),
        ],
        [edge("a", "b"), edge("b", "test_b")],
    )


@pytest.fixture
def branching_graph() -> dict:
    return graph_payload(
        [node("root", "src/root.py", 1), *[node(f"n{i}", f"src/n{i}.py", 1) for i in range(4)]],
        [edge("root", f"n{i}") for i in range(4)],
    )


@pytest.fixture
def cyclic_graph() -> dict:
    return graph_payload(
        [node("a", "src/a.py", 1), node("b", "src/b.py", 2), node("c", "src/c.py", 2)],
        [edge("a", "b"), edge("b", "c"), edge("c", "a")],
    )


@pytest.fixture
def undirected_graph(linear_graph: dict) -> dict:
    return {**linear_graph, "directed": False}


@pytest.fixture
def stale_graph(linear_graph: dict) -> dict:
    return linear_graph


@pytest.fixture
def inferred_edges_graph() -> dict:
    return graph_payload(
        [node("a", "src/a.py", 1), node("b", "src/b.py", 1)],
        [edge("a", "b", confidence="INFERRED")],
    )


@pytest.fixture
def mixed_provenance_graph() -> dict:
    return graph_payload(
        [node("a", "src/a.py", 1), node("b", "src/b.py", 1), node("c", "src/c.py", 2)],
        [edge("a", "b"), edge("b", "c", confidence="INFERRED")],
    )


@pytest.fixture
def cross_community_change() -> dict:
    return graph_payload(
        [node("new", "src/new.py", 1), node("existing", "src/existing.py", 2)],
        [edge("new", "existing")],
    )


@pytest.fixture
def isolated_new_abstraction() -> dict:
    return graph_payload([node("isolated", "src/isolated.py", 1)], [])


@pytest.fixture
def affected_test_graph() -> dict:
    return graph_payload(
        [node("service", "src/orders/service.py", 1), node("test", "tests/integration/test_orders.py", 2)],
        [edge("service", "test")],
    )


@pytest.fixture
def large_fanout_graph() -> dict:
    return graph_payload(
        [node("root", "src/root.py", 1), *[node(f"n{i}", f"src/n{i}.py", i % 3) for i in range(250)]],
        [edge("root", f"n{i}") for i in range(250)],
    )
