from __future__ import annotations

from enum import StrEnum
from typing import Any

from .anti_ai_audit import AntiAiAuditService
from .baseline import BaselineError, finding_occurrences
from .evidence import CheckError, CheckResult, CheckStatus
from .scope import ScopeVerifier
from .security_audit import SecurityAuditService


MAX_REMEDIATION_FINDINGS = 100


class RemediationState(StrEnum):
    RESOLVED = "RESOLVED"
    PARTIALLY_RESOLVED = "PARTIALLY_RESOLVED"
    UNRESOLVED = "UNRESOLVED"
    REGRESSION = "REGRESSION"
    NOT_VERIFIABLE = "NOT_VERIFIABLE"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"


AUTOMATIC_IDS = {
    "AA-AI-PLACEHOLDER-001",
    "AA-AI-TEST-BYPASS-001",
    "AA-SEC-DYNAMIC-EXEC-001",
    "AA-SEC-PATH-001",
    "AA-SEC-SHELL-001",
    "AA-SEC-TEMP-001",
    "AA-SEC-WEAKENING-001",
}
MANUAL_IDS = {
    "AA-AI-ABSTRACTION-001",
    "AA-AI-FILE-PROLIFERATION-001",
    "AA-ARCH-002",
    "AA-ARCH-003",
    "AA-ARCH-004",
}


class RemediationService:
    def __init__(
        self,
        anti_ai_audit: AntiAiAuditService,
        security_audit: SecurityAuditService,
        scope_verifier: ScopeVerifier,
    ) -> None:
        self.anti_ai_audit = anti_ai_audit
        self.security_audit = security_audit
        self.scope_verifier = scope_verifier

    def verify(
        self,
        previous_findings: list[dict[str, Any]],
        *,
        mode: str = "combined",
    ) -> CheckResult:
        if not isinstance(previous_findings, list) or not previous_findings:
            return CheckResult(
                CheckStatus.ERROR,
                "Remediation verification requires at least one previous finding.",
                errors=(CheckError("INVALID_INPUT", "previous_findings must be a non-empty list"),),
            )
        if len(previous_findings) > MAX_REMEDIATION_FINDINGS:
            return CheckResult(
                CheckStatus.ERROR,
                "Remediation verification input exceeds the bounded finding limit.",
                errors=(
                    CheckError(
                        "SECURITY_LIMIT",
                        f"at most {MAX_REMEDIATION_FINDINGS} findings may be verified",
                    ),
                ),
            )
        try:
            anti_ai = self.anti_ai_audit.audit(mode=mode)
            security = self.security_audit.audit(mode=mode)
            current_findings = [
                *(finding.to_dict() for finding in anti_ai.findings),
                *(finding.to_dict() for finding in security.findings),
            ]
            results = [
                self._verify_finding(previous, current_findings, mode=mode)
                for previous in previous_findings
            ]
        except (BaselineError, TypeError, ValueError) as exc:
            return CheckResult(
                CheckStatus.ERROR,
                "Previous findings could not be normalized for remediation verification.",
                errors=(CheckError("INVALID_INPUT", str(exc)),),
            )
        states = {item["state"] for item in results}
        if states & {RemediationState.UNRESOLVED.value, RemediationState.REGRESSION.value}:
            status = CheckStatus.FAIL
        elif states == {RemediationState.RESOLVED.value}:
            status = CheckStatus.PASS
        else:
            status = CheckStatus.WARNING
        return CheckResult(
            status,
            f"Verified {len(results)} previous finding(s) against current repository evidence.",
            metadata={
                "remediations": results,
                "current_audits": {
                    "anti_ai": anti_ai.status.value,
                    "security": security.status.value,
                },
                "ignored_claim_fields": ["fixed", "resolved", "status"],
                "limits": {
                    "max_findings": MAX_REMEDIATION_FINDINGS,
                    "truncated": False,
                },
            },
        )

    def _verify_finding(
        self,
        previous: dict[str, Any],
        current_findings: list[dict[str, Any]],
        *,
        mode: str,
    ) -> dict[str, Any]:
        if not isinstance(previous, dict) or not isinstance(previous.get("id"), str):
            raise ValueError("every previous finding must be an object with a string id")
        identifier = previous["id"]
        if identifier in MANUAL_IDS:
            return _result(
                identifier,
                RemediationState.MANUAL_REVIEW_REQUIRED,
                "The finding depends on architectural or maintainability judgment that current static evidence cannot prove.",
            )
        if identifier.startswith("AA-SCOPE-"):
            return self._verify_scope(previous, mode=mode)
        if identifier != "AA-SEC-SECRET-001" and identifier not in AUTOMATIC_IDS:
            return _result(
                identifier,
                RemediationState.NOT_VERIFIABLE,
                "No deterministic or bounded verifier is registered for this finding ID.",
            )
        previous_occurrences = finding_occurrences(previous)
        current_same_id = [
            occurrence
            for finding in current_findings
            if finding.get("id") == identifier
            for occurrence in finding_occurrences(finding)
        ]
        previous_fingerprints = {item["fingerprint"] for item in previous_occurrences}
        current_fingerprints = {item["fingerprint"] for item in current_same_id}
        remaining = previous_fingerprints & current_fingerprints
        if remaining == previous_fingerprints:
            return _result(
                identifier,
                RemediationState.UNRESOLVED,
                "Equivalent current evidence remains for every previous finding occurrence.",
            )
        if remaining:
            return _result(
                identifier,
                RemediationState.PARTIALLY_RESOLVED,
                "Some previous occurrences disappeared, but equivalent current evidence remains.",
            )
        if current_same_id:
            return _result(
                identifier,
                RemediationState.REGRESSION,
                "The original occurrence is absent, but a new equivalent rule finding exists elsewhere or with changed semantics.",
            )
        if identifier == "AA-SEC-SECRET-001":
            return _result(
                identifier,
                RemediationState.PARTIALLY_RESOLVED,
                "The credential-like value is no longer detected, but removal cannot prove external rotation or revocation.",
            )
        return _result(
            identifier,
            RemediationState.RESOLVED,
            "No equivalent current evidence remains for the supported finding.",
        )

    def _verify_scope(self, previous: dict[str, Any], *, mode: str) -> dict[str, Any]:
        payloads = [
            evidence.get("payload", {})
            for evidence in previous.get("evidence", [])
            if isinstance(evidence, dict) and isinstance(evidence.get("payload"), dict)
        ]
        allowed = next((payload.get("allowed") for payload in payloads if "allowed" in payload), [])
        denied = next((payload.get("denied") for payload in payloads if "denied" in payload), [])
        exceptions = next((payload.get("exceptions") for payload in payloads if "exceptions" in payload), [])
        if not any((allowed, denied, exceptions)):
            return _result(
                previous["id"],
                RemediationState.NOT_VERIFIABLE,
                "The previous scope finding does not contain the declaration needed to rerun verification.",
            )
        current = self.scope_verifier.verify(
            allowed=allowed,
            denied=denied,
            exceptions=exceptions,
            mode=mode,
        )
        current_ids = {finding.id for finding in current.findings}
        state = (
            RemediationState.UNRESOLVED
            if previous["id"] in current_ids
            else RemediationState.RESOLVED
        )
        return _result(
            previous["id"],
            state,
            "Scope verification was rerun from the previous finding declaration.",
        )


def _result(identifier: str, state: RemediationState, reason: str) -> dict[str, str]:
    return {"finding_id": identifier, "state": state.value, "reason": reason}
