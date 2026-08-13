from __future__ import annotations

import functools
import logging
import os
import time
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar


_PARAMETERS = ParamSpec("_PARAMETERS")
_RESULT = TypeVar("_RESULT")
_LOGGER = logging.getLogger("anti_ai_mcp")
_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def observe_tool(
    name: str,
) -> Callable[[Callable[_PARAMETERS, _RESULT]], Callable[_PARAMETERS, _RESULT]]:
    def decorate(
        operation: Callable[_PARAMETERS, _RESULT],
    ) -> Callable[_PARAMETERS, _RESULT]:
        @functools.wraps(operation)
        def observed(*args: _PARAMETERS.args, **kwargs: _PARAMETERS.kwargs) -> _RESULT:
            started = time.monotonic()
            try:
                result = operation(*args, **kwargs)
            except Exception as exc:
                _log(
                    logging.ERROR,
                    name,
                    time.monotonic() - started,
                    "ERROR",
                    False,
                    0,
                    error_type=type(exc).__name__,
                )
                raise
            status, truncated, findings = _result_metadata(result)
            _log(
                logging.INFO,
                name,
                time.monotonic() - started,
                status,
                truncated,
                findings,
            )
            return result

        return observed

    return decorate


def _result_metadata(result: Any) -> tuple[str, bool, int]:
    if not isinstance(result, dict):
        return "UNKNOWN", False, 0
    status = str(result.get("status") or result.get("overall_status") or "UNKNOWN")
    findings = result.get("findings")
    finding_count = len(findings) if isinstance(findings, list) else 0
    truncated = _contains_truncation(result)
    return status, truncated, finding_count


def _contains_truncation(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    if value.get("truncated") is True:
        return True
    return any(_contains_truncation(item) for item in value.values() if isinstance(item, dict))


def _log(
    event_level: int,
    name: str,
    duration: float,
    status: str,
    truncated: bool,
    findings: int,
    *,
    error_type: str | None = None,
) -> None:
    configured = _LEVELS.get(os.environ.get("ANTI_AI_MCP_LOG_LEVEL", "").upper())
    if configured is None or event_level < configured:
        return
    suffix = f" error_type={error_type}" if error_type else ""
    _LOGGER.log(
        event_level,
        "tool=%s duration_ms=%d status=%s truncated=%s findings=%d%s",
        name,
        round(duration * 1000),
        status,
        str(truncated).lower(),
        findings,
        suffix,
    )
