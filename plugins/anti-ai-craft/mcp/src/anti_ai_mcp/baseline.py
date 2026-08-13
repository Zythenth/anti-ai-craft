from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .git import GitInspector
from .paths import resolve_within_repository


BASELINE_SCHEMA_VERSION = "1.0"
MAX_BASELINE_BYTES = 1024 * 1024
MAX_BASELINE_FINDINGS = 2_000
SEMANTIC_EVIDENCE_KEYS = {
    "call",
    "change",
    "control_terms",
    "credential_format",
    "direction",
    "graph_item",
    "relation",
    "role",
    "signal",
    "source",
    "source_file",
    "target",
    "test_path",
}


class BaselineError(ValueError):
    pass


class BaselineService:
    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root.resolve(strict=True)
        self.git_inspector = GitInspector(self.repository_root)

    def create_document(
        self,
        *,
        findings: Iterable[dict[str, Any]],
        tool_version: str,
        graph: dict[str, Any] | None = None,
        validation: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        snapshot = self.git_inspector.snapshot("combined")
        occurrences = [
            occurrence
            for finding in findings
            for occurrence in finding_occurrences(finding)
        ]
        if len(occurrences) > MAX_BASELINE_FINDINGS:
            raise BaselineError(
                f"baseline accepts at most {MAX_BASELINE_FINDINGS} finding occurrences"
            )
        occurrences.sort(key=lambda item: (item["id"], item["path"], item["fingerprint"]))
        architecture_signatures = sorted(
            item["fingerprint"]
            for item in occurrences
            if item["id"].startswith("AA-ARCH-")
        )
        document = {
            "schema_version": BASELINE_SCHEMA_VERSION,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "tool_version": str(tool_version),
            "repository": {
                "head": snapshot.head,
                "branch": snapshot.branch,
                "working_tree_clean": snapshot.clean,
            },
            "findings": occurrences,
            "architecture_signatures": architecture_signatures,
            "graph": _compact_graph(graph or {}),
            "validation": _compact_validation(validation or {}),
        }
        _validate_document(document)
        return document

    def write(self, path: str | Path, document: dict[str, Any]) -> Path:
        _validate_document(document)
        target = resolve_within_repository(self.repository_root, path)
        target.parent.mkdir(parents=True, exist_ok=True)
        encoded = json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if len(encoded.encode("utf-8")) > MAX_BASELINE_BYTES:
            raise BaselineError(f"baseline exceeds {MAX_BASELINE_BYTES} byte limit")
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=target.parent,
                prefix=f".{target.name}.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
                temporary = Path(handle.name)
            os.replace(temporary, target)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
        return target

    def load(self, path: str | Path) -> dict[str, Any]:
        target = resolve_within_repository(self.repository_root, path)
        try:
            if target.stat().st_size > MAX_BASELINE_BYTES:
                raise BaselineError(f"baseline exceeds {MAX_BASELINE_BYTES} byte limit")
            document = json.loads(target.read_text(encoding="utf-8"))
        except BaselineError:
            raise
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise BaselineError(f"baseline could not be read: {exc}") from exc
        _validate_document(document)
        return document

    def compare_document(
        self,
        baseline: dict[str, Any],
        current_findings: Iterable[dict[str, Any]],
    ) -> dict[str, Any]:
        _validate_document(baseline)
        current = [
            occurrence
            for finding in current_findings
            for occurrence in finding_occurrences(finding)
        ]
        baseline_items = list(baseline["findings"])
        baseline_by_fingerprint = {item["fingerprint"]: item for item in baseline_items}
        baseline_by_identity = {item["identity"]: item for item in baseline_items}
        current_fingerprints = {item["fingerprint"] for item in current}
        current_identities = {item["identity"] for item in current}
        items: list[dict[str, Any]] = []
        regression_count = 0
        for item in sorted(current, key=lambda value: (value["id"], value["path"], value["fingerprint"])):
            if item["fingerprint"] in baseline_by_fingerprint:
                state = "PRE_EXISTING"
                regression = False
            elif item["identity"] in baseline_by_identity:
                state = "CHANGED"
                previous = baseline_by_identity[item["identity"]]
                regression = _severity_rank(item["severity"]) > _severity_rank(previous["severity"])
            else:
                state = "NEW"
                regression = True
            regression_count += int(regression)
            items.append({**item, "state": state, "regression": regression})
        for item in sorted(baseline_items, key=lambda value: (value["id"], value["path"], value["fingerprint"])):
            if item["fingerprint"] in current_fingerprints or item["identity"] in current_identities:
                continue
            items.append({**item, "state": "RESOLVED", "regression": False})
        counts: dict[str, int] = {}
        for item in items:
            counts[item["state"]] = counts.get(item["state"], 0) + 1
        return {
            "schema_version": BASELINE_SCHEMA_VERSION,
            "baseline_head": baseline["repository"].get("head"),
            "overall_status": "REGRESSION" if regression_count else "PASS",
            "regression_count": regression_count,
            "counts": counts,
            "items": items,
        }


def finding_occurrences(finding: dict[str, Any]) -> list[dict[str, Any]]:
    identifier = str(finding.get("id") or "")
    if not identifier:
        raise BaselineError("finding id is required")
    category = str(finding.get("category") or "unknown")
    severity = str(finding.get("severity") or "INFO")
    evidence = finding.get("evidence")
    evidence_items = evidence if isinstance(evidence, list) and evidence else [{}]
    occurrences = []
    for item in evidence_items:
        payload = item.get("payload", {}) if isinstance(item, dict) else {}
        payload = payload if isinstance(payload, dict) else {}
        path = _finding_path(finding, payload)
        semantic = {
            key: _normalize_semantic(payload[key])
            for key in sorted(SEMANTIC_EVIDENCE_KEYS)
            if key in payload and payload[key] is not None
        }
        identity_payload = {"id": identifier, "path": path}
        fingerprint_payload = {
            "id": identifier,
            "category": category,
            "path": path,
            "semantic": semantic,
        }
        occurrences.append(
            {
                "fingerprint": _digest(fingerprint_payload),
                "identity": _digest(identity_payload),
                "id": identifier,
                "category": category,
                "path": path,
                "severity": severity,
                "evidence_kind": str(item.get("kind") or "MANUAL_REVIEW_REQUIRED")
                if isinstance(item, dict)
                else "MANUAL_REVIEW_REQUIRED",
            }
        )
    unique = {item["fingerprint"]: item for item in occurrences}
    return list(unique.values())


def _finding_path(finding: dict[str, Any], payload: dict[str, Any]) -> str:
    location = finding.get("location")
    location_path = location.get("path") if isinstance(location, dict) else None
    value = payload.get("path") or payload.get("source_file") or location_path or ""
    return str(value).replace("\\", "/")


def _normalize_semantic(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _normalize_semantic(item) for key, item in sorted(value.items())}
    if isinstance(value, (list, tuple, set)):
        return sorted((_normalize_semantic(item) for item in value), key=lambda item: json.dumps(item, sort_keys=True))
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _digest(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _compact_graph(graph: dict[str, Any]) -> dict[str, Any]:
    keys = ("provider", "availability", "freshness", "directed", "node_count", "edge_count")
    return {key: graph[key] for key in keys if key in graph}


def _compact_validation(validation: dict[str, Any]) -> dict[str, Any]:
    checks = validation.get("selected_checks", [])
    identifiers = sorted(
        str(check["id"])
        for check in checks
        if isinstance(check, dict) and check.get("id")
    )
    return {"selected_check_ids": identifiers}


def _validate_document(document: Any) -> None:
    if not isinstance(document, dict):
        raise BaselineError("baseline must be a JSON object")
    if document.get("schema_version") != BASELINE_SCHEMA_VERSION:
        raise BaselineError(
            f"unsupported baseline schema_version: {document.get('schema_version')!r}"
        )
    findings = document.get("findings")
    if not isinstance(findings, list) or len(findings) > MAX_BASELINE_FINDINGS:
        raise BaselineError("baseline findings are missing or exceed the configured limit")
    for item in findings:
        if not isinstance(item, dict):
            raise BaselineError("every baseline finding must be an object")
        if not all(isinstance(item.get(key), str) for key in ("fingerprint", "identity", "id", "path")):
            raise BaselineError("baseline finding is missing stable identity fields")


def _severity_rank(severity: str) -> int:
    return {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}.get(
        severity, 0
    )
