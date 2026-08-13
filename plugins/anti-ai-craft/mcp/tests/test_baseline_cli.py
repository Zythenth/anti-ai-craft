from __future__ import annotations

import json
from pathlib import Path

from anti_ai_mcp.baseline_cli import main


def test_baseline_cli_create_and_validate_are_explicit(
    clean_repo: Path, capsys
) -> None:
    main(
        [
            "create",
            "--repository-root",
            str(clean_repo),
            "--output",
            ".anti-ai/baseline.json",
            "--disable-graph",
        ]
    )
    created = json.loads(capsys.readouterr().out)
    assert created["status"] == "PASS"
    assert created["path"] == ".anti-ai/baseline.json"

    main(
        [
            "validate",
            "--repository-root",
            str(clean_repo),
            ".anti-ai/baseline.json",
        ]
    )
    validated = json.loads(capsys.readouterr().out)
    assert validated["status"] == "PASS"
    assert validated["schema_version"] == "1.0"
