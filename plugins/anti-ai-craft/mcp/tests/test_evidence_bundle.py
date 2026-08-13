from __future__ import annotations

import json
from pathlib import Path

from anti_ai_mcp.anti_ai_audit import AntiAiAuditService
from anti_ai_mcp.architecture import ArchitectureService
from anti_ai_mcp.baseline import BaselineService
from anti_ai_mcp.checks import ProjectCheckService
from anti_ai_mcp.evidence_bundle import EvidenceBundleService
from anti_ai_mcp.git import GitInspector
from anti_ai_mcp.graph import build_graph_provider
from anti_ai_mcp.impact import ChangeImpactService
from anti_ai_mcp.remediation import RemediationService
from anti_ai_mcp.repository import RepositoryInspector
from anti_ai_mcp.relevant_tests import RelevantTestService
from anti_ai_mcp.scope import ScopeVerifier
from anti_ai_mcp.security_audit import SecurityAuditService
from anti_ai_mcp.status import AntiAiStatusService, StatusSettings


def bundle_service(repository: Path) -> EvidenceBundleService:
    exclude = repository / ".git" / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    exclude.write_text(".pytest_cache/\n__pycache__/\n", encoding="utf-8")
    plugin = repository / "plugins" / "anti-ai-craft"
    (plugin / ".codex-plugin").mkdir(parents=True, exist_ok=True)
    (plugin / ".codex-plugin" / "plugin.json").write_text(
        json.dumps({"version": "0.6.0"}), encoding="utf-8"
    )
    inspector = GitInspector(repository)
    provider = build_graph_provider(repository, enabled=False)
    status = AntiAiStatusService(StatusSettings(repository, plugin), provider)
    checks = ProjectCheckService(repository)
    scope = ScopeVerifier(inspector)
    relevant = RelevantTestService(repository, inspector, checks, provider)
    impact = ChangeImpactService(inspector, provider)
    architecture = ArchitectureService(inspector, provider)
    anti_ai = AntiAiAuditService(repository, inspector, provider, architecture)
    security = SecurityAuditService(repository, inspector)
    remediation = RemediationService(anti_ai, security, scope)
    return EvidenceBundleService(
        repository,
        status,
        RepositoryInspector(repository, plugin),
        inspector,
        scope,
        checks,
        relevant,
        impact,
        architecture,
        anti_ai,
        security,
        remediation,
        BaselineService(repository),
    )


def test_bundle_is_structured_and_dry_run_does_not_execute(clean_repo: Path) -> None:
    result = bundle_service(clean_repo).collect(execute=False)

    assert result["schema_version"] == "1.0"
    assert result["performance"]["total_seconds"] >= 0
    assert "security" in result["performance"]["phase_seconds"]
    assert result["repository"]["status"] == "PASS"
    assert result["git"]["metadata"]["clean"] is False  # plugin fixture is untracked
    assert result["validation"]["metadata"]["executions"] == []
    assert result["tests"]["metadata"]["executions"] == []
    assert result["graph"]["availability"] == "disabled"
    assert result["cache_policy"] == "no_cross_call_cache"
    assert result["state_signature"]


def test_bundle_deduplicates_identical_validation_and_test_execution(
    validation_pass_repo: Path,
) -> None:
    result = bundle_service(validation_pass_repo).collect(
        execute=True, timeout_seconds=60
    )

    assert result["validation"]["metadata"]["executions"][0]["status"] == "PASS"
    assert result["tests"]["metadata"]["execution_reused_from"] == "validation"
    assert result["tests"]["metadata"]["deduplicated_commands"] == 1


def test_bundle_compares_baseline_and_promotes_regression_to_fail(clean_repo: Path) -> None:
    service = bundle_service(clean_repo)
    baseline = service.baseline_service.create_document(findings=[], tool_version="0.2.0")
    service.baseline_service.write(".anti-ai/baseline.json", baseline)
    source = clean_repo / "src" / "runner.py"
    source.parent.mkdir()
    source.write_text("import os\nos.system('tool')\n", encoding="utf-8")

    result = service.collect(baseline_path=".anti-ai/baseline.json")

    assert result["overall_status"] == "FAIL"
    assert result["baseline"]["overall_status"] == "REGRESSION"
    assert result["baseline"]["counts"]["NEW"] >= 1


def test_bundle_reports_invalid_baseline_without_traceback(clean_repo: Path) -> None:
    service = bundle_service(clean_repo)
    (clean_repo / "bad-baseline.json").write_text("{}", encoding="utf-8")

    result = service.collect(baseline_path="bad-baseline.json")

    assert result["overall_status"] == "FAIL"
    assert result["errors"][0]["code"] == "BASELINE_INVALID"
