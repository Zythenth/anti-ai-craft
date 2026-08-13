from __future__ import annotations

import json
from pathlib import Path

import pytest

from anti_ai_mcp.baseline import BaselineError, BaselineService, finding_occurrences
from anti_ai_mcp.paths import PathBoundaryError
from conftest import git


def finding(
    identifier: str,
    path: str,
    *,
    line: int = 1,
    signal: str = "signal-a",
    severity: str = "MEDIUM",
) -> dict:
    return {
        "id": identifier,
        "category": "fixture",
        "severity": severity,
        "confidence": "HIGH",
        "message": "fixture finding",
        "location": {"path": path, "line": line},
        "evidence": [
            {
                "kind": "FACT",
                "source": "fixture",
                "payload": {
                    "path": path,
                    "line": line,
                    "signal": signal,
                    "redacted_value": "abcd********wxyz",
                },
                "provenance": {},
            }
        ],
        "suggestion": None,
    }


def test_fingerprint_ignores_line_and_redacted_value_but_not_semantics() -> None:
    first = finding_occurrences(finding("AA-FIX-001", "src/a.py", line=2))[0]
    moved = finding("AA-FIX-001", "src/a.py", line=200)
    moved["evidence"][0]["payload"]["redacted_value"] = "zzzz****yyyy"
    second = finding_occurrences(moved)[0]
    changed = finding_occurrences(
        finding("AA-FIX-001", "src/a.py", line=200, signal="signal-b")
    )[0]

    assert first["fingerprint"] == second["fingerprint"]
    assert first["fingerprint"] != changed["fingerprint"]


def test_baseline_is_compact_versioned_and_contains_no_raw_evidence(clean_repo: Path) -> None:
    service = BaselineService(clean_repo)
    document = service.create_document(
        findings=[finding("AA-SEC-SECRET-001", "src/settings.py")],
        tool_version="0.2.0",
        graph={"provider": "graphify", "freshness": "available_but_stale", "node_count": 10},
        validation={"selected_checks": [{"id": "unit-tests", "command": ["python", "-m", "pytest"]}]},
    )

    assert document["schema_version"] == "1.0"
    assert document["repository"]["head"]
    assert document["findings"][0]["id"] == "AA-SEC-SECRET-001"
    serialized = json.dumps(document)
    assert "redacted_value" not in serialized
    assert "abcd********wxyz" not in serialized
    assert document["validation"] == {"selected_check_ids": ["unit-tests"]}


def test_compare_distinguishes_new_preexisting_changed_and_resolved(clean_repo: Path) -> None:
    service = BaselineService(clean_repo)
    baseline = service.create_document(
        findings=[
            finding("AA-FIX-001", "src/existing.py"),
            finding("AA-FIX-002", "src/changed.py", signal="before"),
            finding("AA-FIX-003", "src/resolved.py"),
        ],
        tool_version="0.2.0",
    )
    result = service.compare_document(
        baseline,
        [
            finding("AA-FIX-001", "src/existing.py", line=50),
            finding("AA-FIX-002", "src/changed.py", signal="after", severity="HIGH"),
            finding("AA-FIX-004", "src/new.py"),
        ],
    )

    states = {item["id"]: item["state"] for item in result["items"]}
    assert states == {
        "AA-FIX-001": "PRE_EXISTING",
        "AA-FIX-002": "CHANGED",
        "AA-FIX-003": "RESOLVED",
        "AA-FIX-004": "NEW",
    }
    assert result["overall_status"] == "REGRESSION"
    assert result["regression_count"] == 2


def test_baseline_write_is_explicit_atomic_and_repository_confined(clean_repo: Path) -> None:
    service = BaselineService(clean_repo)
    document = service.create_document(findings=[], tool_version="0.2.0")

    path = service.write(".anti-ai/baseline.json", document)

    assert path == clean_repo / ".anti-ai" / "baseline.json"
    assert service.load(".anti-ai/baseline.json") == document
    assert not list(path.parent.glob("*.tmp"))
    with pytest.raises(PathBoundaryError):
        service.write("../baseline.json", document)


def test_invalid_baseline_is_rejected(clean_repo: Path) -> None:
    target = clean_repo / "baseline.json"
    target.write_text('{"schema_version":"99"}', encoding="utf-8")
    with pytest.raises(BaselineError):
        BaselineService(clean_repo).load("baseline.json")


def test_architecture_baseline_stores_only_compact_signatures(clean_repo: Path) -> None:
    service = BaselineService(clean_repo)
    document = service.create_document(
        findings=[finding("AA-ARCH-002", "src/boundary.py")],
        tool_version="0.2.0",
        graph={"provider": "graphify", "freshness": "available_and_fresh", "node_count": 1000, "edge_count": 2000},
    )

    assert document["architecture_signatures"] == [document["findings"][0]["fingerprint"]]
    assert "nodes" not in document["graph"]
    assert "edges" not in document["graph"]
