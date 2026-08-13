from __future__ import annotations

import json
from pathlib import Path

from anti_ai_mcp.git import GitInspector
from anti_ai_mcp.security_audit import SecurityAuditService
from conftest import git


def audit(repository: Path) -> dict:
    return SecurityAuditService(repository, GitInspector(repository)).audit().to_dict()


def finding_ids(result: dict) -> set[str]:
    return {finding["id"] for finding in result["findings"]}


def test_python_execution_and_tempfile_signals_are_detected(clean_repo: Path) -> None:
    source = clean_repo / "src" / "runner.py"
    source.parent.mkdir()
    source.write_text(
        "import os\nimport subprocess\nimport tempfile\n"
        "subprocess.run(['tool'], shell=True)\n"
        "os.system('tool')\n"
        "eval('1 + 1')\n"
        "exec('VALUE = 1')\n"
        "tempfile.mktemp()\n",
        encoding="utf-8",
    )

    result = audit(clean_repo)

    assert {
        "AA-SEC-SHELL-001",
        "AA-SEC-DYNAMIC-EXEC-001",
        "AA-SEC-TEMP-001",
    } <= finding_ids(result)
    shell = next(item for item in result["findings"] if item["id"] == "AA-SEC-SHELL-001")
    assert all(item["kind"] == "FACT" for item in shell["evidence"])


def test_safe_subprocess_and_environment_secret_are_not_findings(clean_repo: Path) -> None:
    source = clean_repo / "src" / "safe.py"
    source.parent.mkdir()
    source.write_text(
        "import os\nimport subprocess\n"
        "API_KEY = os.environ['API_KEY']\n"
        "PLACEHOLDER = 'your-api-key'\n"
        "subprocess.run(['tool'], shell=False, check=True)\n",
        encoding="utf-8",
    )

    result = audit(clean_repo)

    assert "AA-SEC-SHELL-001" not in finding_ids(result)
    assert "AA-SEC-SECRET-001" not in finding_ids(result)
    assert result["metadata"]["suppressed_secret_candidates"] >= 1


def test_credential_like_value_is_redacted(clean_repo: Path) -> None:
    credential = "AKIA1234567890ABCDEF"
    source = clean_repo / "src" / "settings.py"
    source.parent.mkdir()
    source.write_text(f"ACCESS_KEY = '{credential}'\n", encoding="utf-8")

    result = audit(clean_repo)
    serialized = json.dumps(result)

    finding = next(item for item in result["findings"] if item["id"] == "AA-SEC-SECRET-001")
    payload = finding["evidence"][0]["payload"]
    assert payload["credential_format"] == "aws-access-key-id"
    assert payload["redacted_value"].startswith("AKIA")
    assert payload["redacted_value"].endswith("CDEF")
    assert credential not in serialized


def test_hardcoded_test_credential_requires_manual_review(clean_repo: Path) -> None:
    source = clean_repo / "tests" / "test_auth.py"
    source.parent.mkdir()
    source.write_text("PASSWORD = 'S3cureFixtureValue!'\n", encoding="utf-8")

    result = audit(clean_repo)

    finding = next(item for item in result["findings"] if item["id"] == "AA-SEC-SECRET-001")
    assert finding["severity"] == "LOW"
    assert finding["evidence"][0]["kind"] == "MANUAL_REVIEW_REQUIRED"
    assert finding["evidence"][0]["payload"]["test_fixture"] is True


def test_path_traversal_and_removed_boundary_control_are_reviewed(clean_repo: Path) -> None:
    source = clean_repo / "src" / "reader.py"
    source.parent.mkdir()
    source.write_text(
        "from anti_ai_mcp.paths import resolve_within_repository\n"
        "safe = resolve_within_repository(root, candidate)\n",
        encoding="utf-8",
    )
    git(clean_repo, "add", "src/reader.py")
    git(clean_repo, "commit", "-q", "-m", "add boundary")
    source.write_text("data = open('../outside.txt').read()\n", encoding="utf-8")

    result = audit(clean_repo)

    assert "AA-SEC-PATH-001" in finding_ids(result)
    weakening = next(item for item in result["findings"] if item["id"] == "AA-SEC-WEAKENING-001")
    assert weakening["evidence"][0]["kind"] == "MANUAL_REVIEW_REQUIRED"


def test_sensitive_file_is_reported_but_example_file_is_not(clean_repo: Path) -> None:
    (clean_repo / ".env").write_text("NAME=value\n", encoding="utf-8")
    (clean_repo / ".env.example").write_text("NAME=placeholder\n", encoding="utf-8")

    result = audit(clean_repo)

    finding = next(item for item in result["findings"] if item["id"] == "AA-SEC-SECRET-001")
    paths = {item["payload"]["path"] for item in finding["evidence"]}
    assert ".env" in paths
    assert ".env.example" not in paths
