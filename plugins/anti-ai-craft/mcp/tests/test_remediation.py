from __future__ import annotations

from pathlib import Path

from anti_ai_mcp.anti_ai_audit import AntiAiAuditService
from anti_ai_mcp.architecture import ArchitectureService
from anti_ai_mcp.baseline import BaselineService
from anti_ai_mcp.git import GitInspector
from anti_ai_mcp.graph import build_graph_provider
from anti_ai_mcp.remediation import RemediationService
from anti_ai_mcp.scope import ScopeVerifier
from anti_ai_mcp.security_audit import SecurityAuditService


def services(repository: Path) -> tuple[AntiAiAuditService, RemediationService]:
    inspector = GitInspector(repository)
    provider = build_graph_provider(repository, enabled=False)
    architecture = ArchitectureService(inspector, provider)
    anti_ai = AntiAiAuditService(repository, inspector, provider, architecture)
    security = SecurityAuditService(repository, inspector)
    remediation = RemediationService(anti_ai, security, ScopeVerifier(inspector))
    return anti_ai, remediation


def previous_finding(result: dict, identifier: str) -> dict:
    return next(item for item in result["findings"] if item["id"] == identifier)


def test_claimed_fixed_does_not_override_current_placeholder_evidence(clean_repo: Path) -> None:
    source = clean_repo / "src" / "service.py"
    source.parent.mkdir()
    source.write_text("# TODO: implement\n", encoding="utf-8")
    anti_ai, remediation = services(clean_repo)
    prior = previous_finding(anti_ai.audit().to_dict(), "AA-AI-PLACEHOLDER-001")
    prior["fixed"] = True

    result = remediation.verify([prior]).to_dict()

    assert result["metadata"]["remediations"][0]["state"] == "UNRESOLVED"


def test_removed_placeholder_is_resolved_by_current_evidence(clean_repo: Path) -> None:
    source = clean_repo / "src" / "service.py"
    source.parent.mkdir()
    source.write_text("# TODO: implement\n", encoding="utf-8")
    anti_ai, remediation = services(clean_repo)
    prior = previous_finding(anti_ai.audit().to_dict(), "AA-AI-PLACEHOLDER-001")
    source.write_text("VALUE = 1\n", encoding="utf-8")

    result = remediation.verify([prior]).to_dict()

    assert result["status"] == "PASS"
    assert result["metadata"]["remediations"][0]["state"] == "RESOLVED"


def test_removed_secret_is_only_partially_resolved_without_rotation(clean_repo: Path) -> None:
    source = clean_repo / "src" / "settings.py"
    source.parent.mkdir()
    source.write_text("ACCESS_KEY = 'AKIA1234567890ABCDEF'\n", encoding="utf-8")
    _, remediation = services(clean_repo)
    prior = previous_finding(
        remediation.security_audit.audit().to_dict(), "AA-SEC-SECRET-001"
    )
    source.write_text("ACCESS_KEY = os.environ['ACCESS_KEY']\n", encoding="utf-8")

    result = remediation.verify([prior]).to_dict()

    item = result["metadata"]["remediations"][0]
    assert item["state"] == "PARTIALLY_RESOLVED"
    assert "rotation" in item["reason"].lower()


def test_new_equivalent_signal_after_original_fix_is_regression(clean_repo: Path) -> None:
    source = clean_repo / "src" / "first.py"
    source.parent.mkdir()
    source.write_text("# TODO: first\n", encoding="utf-8")
    anti_ai, remediation = services(clean_repo)
    prior = previous_finding(anti_ai.audit().to_dict(), "AA-AI-PLACEHOLDER-001")
    source.write_text("VALUE = 1\n", encoding="utf-8")
    (source.parent / "second.py").write_text("# TODO: second\n", encoding="utf-8")

    result = remediation.verify([prior]).to_dict()

    assert result["status"] == "FAIL"
    assert result["metadata"]["remediations"][0]["state"] == "REGRESSION"


def test_judgment_rule_and_unknown_rule_are_not_falsely_proven(clean_repo: Path) -> None:
    _, remediation = services(clean_repo)
    abstraction = {
        "id": "AA-AI-ABSTRACTION-001",
        "category": "anti-ai-abstraction",
        "severity": "LOW",
        "confidence": "LOW",
        "message": "fixture",
        "evidence": [],
        "location": {"path": "src/a.py"},
        "suggestion": None,
    }
    unknown = {**abstraction, "id": "AA-UNKNOWN-001"}

    result = remediation.verify([abstraction, unknown]).to_dict()
    states = [item["state"] for item in result["metadata"]["remediations"]]

    assert states == ["MANUAL_REVIEW_REQUIRED", "NOT_VERIFIABLE"]


def test_baseline_regression_fix_and_remediation_workflow(clean_repo: Path) -> None:
    source = clean_repo / "src" / "service.py"
    source.parent.mkdir()
    source.write_text("# TODO: original\n", encoding="utf-8")
    anti_ai, remediation = services(clean_repo)
    baseline_service = BaselineService(clean_repo)
    initial = anti_ai.audit().to_dict()
    prior = previous_finding(initial, "AA-AI-PLACEHOLDER-001")
    baseline = baseline_service.create_document(
        findings=initial["findings"], tool_version="0.2.0"
    )

    regression = source.parent / "regression.py"
    regression.write_text("# FIXME: regression\n", encoding="utf-8")
    regressed = anti_ai.audit().to_dict()
    comparison = baseline_service.compare_document(baseline, regressed["findings"])
    assert comparison["overall_status"] == "REGRESSION"

    source.write_text("VALUE = 1\n", encoding="utf-8")
    regression.unlink()
    fixed = anti_ai.audit().to_dict()
    comparison = baseline_service.compare_document(baseline, fixed["findings"])
    verification = remediation.verify([prior]).to_dict()
    assert comparison["counts"]["RESOLVED"] == 1
    assert verification["metadata"]["remediations"][0]["state"] == "RESOLVED"
