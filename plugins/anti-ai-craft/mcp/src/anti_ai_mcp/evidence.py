from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


CHECK_RESULT_SCHEMA_VERSION = "1.0"


class EvidenceKind(StrEnum):
    FACT = "FACT"
    HEURISTIC = "HEURISTIC"
    INFERENCE = "INFERENCE"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"


class CheckStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    ERROR = "ERROR"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class Severity(StrEnum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Confidence(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class Evidence:
    kind: EvidenceKind
    source: str
    payload: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["kind"] = self.kind.value
        return result


@dataclass(frozen=True)
class Finding:
    id: str
    category: str
    severity: Severity
    confidence: Confidence
    message: str
    evidence: tuple[Evidence, ...] = ()
    location: dict[str, Any] | None = None
    suggestion: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "severity": self.severity.value,
            "confidence": self.confidence.value,
            "message": self.message,
            "evidence": [item.to_dict() for item in self.evidence],
            "location": self.location,
            "suggestion": self.suggestion,
        }


@dataclass(frozen=True)
class CheckError:
    code: str
    message: str
    detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {**asdict(self), "type": _error_type(self.code)}


@dataclass(frozen=True)
class CheckResult:
    status: CheckStatus
    summary: str
    findings: tuple[Finding, ...] = ()
    evidence: tuple[Evidence, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    errors: tuple[CheckError, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": CHECK_RESULT_SCHEMA_VERSION,
            "status": self.status.value,
            "summary": self.summary,
            "findings": [finding.to_dict() for finding in self.findings],
            "evidence": [item.to_dict() for item in self.evidence],
            "metadata": self.metadata,
            "errors": [error.to_dict() for error in self.errors],
        }


def _error_type(code: str) -> str:
    normalized = code.upper()
    if "INPUT" in normalized:
        return "INVALID_INPUT"
    if "GRAPH" in normalized:
        return "GRAPH_INVALID" if "INVALID" in normalized else "GRAPH_UNAVAILABLE"
    if "TIMEOUT" in normalized:
        return "VALIDATION_TIMEOUT"
    if "REPOSITORY" in normalized or normalized.startswith("AA-GIT"):
        return "REPOSITORY_UNAVAILABLE"
    if "SECURITY" in normalized or normalized.startswith("AA-SEC"):
        return "SECURITY_LIMIT"
    if "EXEC" in normalized:
        return "EXECUTION_FAILED"
    if normalized in {
        "INVALID_INPUT",
        "REPOSITORY_UNAVAILABLE",
        "GRAPH_UNAVAILABLE",
        "GRAPH_INVALID",
        "VALIDATION_TIMEOUT",
        "EXECUTION_FAILED",
        "SECURITY_LIMIT",
        "INTERNAL_ERROR",
    }:
        return normalized
    return "INTERNAL_ERROR"
