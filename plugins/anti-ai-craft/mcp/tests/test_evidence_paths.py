from __future__ import annotations

from pathlib import Path

import pytest

from anti_ai_mcp.evidence import (
    CheckResult,
    CheckStatus,
    Confidence,
    Evidence,
    EvidenceKind,
    Finding,
    Severity,
)
from anti_ai_mcp.paths import PathBoundaryError, normalize_repository_path
from anti_ai_mcp.scope import AllowedScopeRule, ScopeContext


def test_check_result_serializes_shared_enums() -> None:
    evidence = Evidence(EvidenceKind.FACT, "fixture", {"observed": True})
    result = CheckResult(
        CheckStatus.FAIL,
        "fixture",
        findings=(
            Finding(
                "AA-FIXTURE-001",
                "fixture",
                Severity.HIGH,
                Confidence.HIGH,
                "failure",
                (evidence,),
            ),
        ),
        evidence=(evidence,),
    ).to_dict()

    assert result["status"] == "FAIL"
    assert result["findings"][0]["severity"] == "HIGH"
    assert result["findings"][0]["evidence"][0]["kind"] == "FACT"


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("./src/foo.py", "src/foo.py"),
        (r"src\foo\bar.py", "src/foo/bar.py"),
        ("src//foo.py", "src/foo.py"),
    ],
)
def test_repository_paths_are_canonical(raw: str, expected: str) -> None:
    assert normalize_repository_path(raw) == expected


@pytest.mark.parametrize("raw", ["../outside", "/absolute", r"C:\outside", "", "a/../../b"])
def test_repository_path_bypass_is_rejected(raw: str) -> None:
    with pytest.raises(PathBoundaryError):
        normalize_repository_path(raw)


def test_minimal_rule_contract_is_concrete() -> None:
    rule = AllowedScopeRule(("src/**",), ())
    assert rule.id == "AA-SCOPE-001"
    assert rule.category == "scope"
    assert rule.deterministic is True
    assert rule.evaluate(ScopeContext(())) == ()
