from __future__ import annotations

import sys
import json
import math
import time
from pathlib import Path

import pytest

from anti_ai_mcp.checks import ProjectCheckService
from anti_ai_mcp.execution import CommandSpec, run_command
from anti_ai_mcp.paths import PathBoundaryError


def test_discover_and_dry_run_validation(validation_pass_repo: Path) -> None:
    service = ProjectCheckService(validation_pass_repo)
    capabilities = service.capabilities()
    assert capabilities["checks"][0]["category"] == "unit-tests"
    assert capabilities["checks"][0]["command"][1:3] == ["-m", "pytest"]
    result = service.run(categories=["unit-tests"], dry_run=True).to_dict()
    assert result["status"] == "PASS"
    assert result["metadata"]["executions"] == []


def test_validation_success(validation_pass_repo: Path) -> None:
    result = ProjectCheckService(validation_pass_repo).run(categories=["unit-tests"]).to_dict()
    assert result["status"] == "PASS"
    assert result["metadata"]["executions"][0]["exit_code"] == 0


def test_validation_failure_and_exit_code(validation_fail_repo: Path) -> None:
    result = ProjectCheckService(validation_fail_repo).run(categories=["unit-tests"]).to_dict()
    assert result["status"] == "FAIL"
    assert result["findings"][0]["id"] == "AA-VAL-001"
    assert result["metadata"]["executions"][0]["exit_code"] == 1


def test_validation_timeout_terminates_process(validation_timeout_repo: Path) -> None:
    result = ProjectCheckService(validation_timeout_repo).run(
        categories=["unit-tests"], timeout_seconds=0.1
    ).to_dict()
    assert result["status"] == "FAIL"
    assert result["findings"][0]["id"] == "AA-VAL-003"
    assert result["metadata"]["executions"][0]["timed_out"] is True


def test_validation_huge_output_is_explicitly_truncated(large_output_repo: Path) -> None:
    result = ProjectCheckService(large_output_repo).run(categories=["unit-tests"]).to_dict()
    assert result["status"] == "FAIL"
    assert result["metadata"]["limits"]["truncated"] is True
    assert "AA-VAL-004" in {finding["id"] for finding in result["findings"]}


def test_command_not_available(clean_repo: Path) -> None:
    execution = run_command(
        clean_repo,
        CommandSpec(("anti-ai-command-that-does-not-exist",), clean_repo, "test", "fixture"),
    )
    assert execution.unavailable is True
    assert execution.status == "ERROR"


def test_validation_reports_declared_runner_not_available(
    clean_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (clean_repo / "package.json").write_text(
        json.dumps({"scripts": {"lint": "eslint ."}}), encoding="utf-8"
    )
    monkeypatch.setenv("PATH", str(clean_repo))
    result = ProjectCheckService(clean_repo).run(categories=["lint"]).to_dict()
    assert result["status"] == "ERROR"
    assert result["findings"][0]["id"] == "AA-VAL-002"


def test_huge_stdout_and_stderr_are_bounded(clean_repo: Path) -> None:
    execution = run_command(
        clean_repo,
        CommandSpec(
            (
                sys.executable,
                "-c",
                "import sys; print('O'*5000); sys.stderr.write('E'*5000)",
            ),
            clean_repo,
            "test",
            "fixture",
        ),
        stdout_limit=100,
        stderr_limit=100,
    )
    assert execution.stdout_truncated is True
    assert execution.stderr_truncated is True
    assert len(execution.stdout.encode()) <= 100
    assert len(execution.stderr.encode()) <= 100


def test_cwd_must_remain_inside_repository(clean_repo: Path, tmp_path: Path) -> None:
    with pytest.raises(PathBoundaryError):
        run_command(
            clean_repo,
            CommandSpec((sys.executable, "-c", "pass"), tmp_path.parent, "test", "fixture"),
        )


def test_shell_metacharacters_are_plain_argv(clean_repo: Path) -> None:
    execution = run_command(
        clean_repo,
        CommandSpec(
            (sys.executable, "-c", "import sys; print(sys.argv[1])", "one;echo injected"),
            clean_repo,
            "test",
            "fixture",
        ),
    )
    assert execution.status == "PASS"
    assert execution.stdout.strip() == "one;echo injected"


def test_repository_cannot_shadow_path_executable(
    clean_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    executable = clean_repo / ("shadow-tool.exe" if sys.platform == "win32" else "shadow-tool")
    executable.write_text("not a trusted executable\n", encoding="utf-8")
    executable.chmod(0o755)
    monkeypatch.setenv("PATH", str(clean_repo))
    execution = run_command(
        clean_repo,
        CommandSpec(("shadow-tool",), clean_repo, "test", "fixture"),
    )
    assert execution.unavailable is True


def test_no_matching_validation_is_not_applicable(clean_repo: Path) -> None:
    result = ProjectCheckService(clean_repo).run(categories=["lint"]).to_dict()
    assert result["status"] == "NOT_APPLICABLE"
    assert result["findings"][0]["id"] == "AA-VAL-005"


def test_non_finite_timeout_is_rejected(validation_pass_repo: Path) -> None:
    result = ProjectCheckService(validation_pass_repo).run(timeout_seconds=math.nan).to_dict()
    assert result["schema_version"] == "1.0"
    assert result["status"] == "ERROR"
    assert result["errors"][0]["code"] == "AA-VAL-INPUT"
    assert result["errors"][0]["type"] == "INVALID_INPUT"


def test_timeout_terminates_child_process_tree(clean_repo: Path) -> None:
    marker = clean_repo / "child-survived.txt"
    child_code = (
        "import time; from pathlib import Path; "
        f"time.sleep(0.8); Path({str(marker)!r}).write_text('survived', encoding='utf-8'); "
        "time.sleep(5)"
    )
    parent_code = (
        "import subprocess, sys, time; "
        f"subprocess.Popen([sys.executable, '-c', {child_code!r}]); "
        "time.sleep(10)"
    )

    execution = run_command(
        clean_repo,
        CommandSpec((sys.executable, "-c", parent_code), clean_repo, "test", "fixture"),
        timeout_seconds=0.2,
    )
    time.sleep(1.0)

    assert execution.timed_out is True
    assert marker.exists() is False


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"timeout_seconds": 0}, "timeout_seconds"),
        ({"timeout_seconds": math.inf}, "timeout_seconds"),
        ({"stdout_limit": -1}, "stdout_limit"),
        ({"stderr_limit": -1}, "stderr_limit"),
    ],
)
def test_run_command_rejects_invalid_limits(
    clean_repo: Path, kwargs: dict[str, float | int], message: str
) -> None:
    execution = run_command(
        clean_repo,
        CommandSpec((sys.executable, "-c", "raise SystemExit(99)"), clean_repo, "test", "fixture"),
        **kwargs,
    )

    assert execution.status == "ERROR"
    assert execution.exit_code is None
    assert message in (execution.error or "")


def test_controlled_environment_does_not_forward_unlisted_secret(
    clean_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTI_AI_TEST_SECRET", "must-not-reach-child")
    execution = run_command(
        clean_repo,
        CommandSpec(
            (
                sys.executable,
                "-c",
                "import os; print(os.environ.get('ANTI_AI_TEST_SECRET', 'absent'))",
            ),
            clean_repo,
            "test",
            "fixture",
        ),
    )

    assert execution.status == "PASS"
    assert execution.stdout.strip() == "absent"
