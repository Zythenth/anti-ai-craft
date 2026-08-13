from __future__ import annotations

import logging

from anti_ai_mcp.observability import observe_tool


def test_observability_logs_only_bounded_result_metadata(
    caplog, monkeypatch
) -> None:
    monkeypatch.setenv("ANTI_AI_MCP_LOG_LEVEL", "INFO")
    secret = "ghp_abcdefghijklmnopqrstuvwxyz1234567890"

    @observe_tool("fixture")
    def operation() -> dict:
        return {
            "status": "WARNING",
            "findings": [{"id": "AA-FIXTURE"}],
            "metadata": {"limits": {"truncated": True}},
            "secret": secret,
        }

    with caplog.at_level(logging.INFO, logger="anti_ai_mcp"):
        result = operation()

    assert result["secret"] == secret
    assert "tool=fixture" in caplog.text
    assert "status=WARNING" in caplog.text
    assert "findings=1" in caplog.text
    assert "truncated=true" in caplog.text
    assert secret not in caplog.text


def test_observability_rejects_unknown_level_without_logging(
    caplog, monkeypatch
) -> None:
    monkeypatch.setenv("ANTI_AI_MCP_LOG_LEVEL", "NOT-A-LEVEL")

    @observe_tool("fixture")
    def operation() -> dict:
        return {"status": "PASS", "findings": []}

    with caplog.at_level(logging.DEBUG, logger="anti_ai_mcp"):
        operation()

    assert caplog.text == ""
