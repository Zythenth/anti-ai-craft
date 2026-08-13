from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters, stdio_client


STAGE_FOUR_SCOPE = [
    ".codex/config.toml",
    ".github/**",
    ".gitignore",
    "README.md",
    "docs/**",
    "plugins/anti-ai-craft/.codex-plugin/plugin.json",
    "plugins/anti-ai-craft/mcp/**",
]


async def smoke(
    repository_root: Path,
    *,
    baseline_path: str | None,
    previous_findings_path: str | None,
    disable_graph: bool,
    execute: bool,
) -> dict:
    args = [
        "-m",
        "anti_ai_mcp.server",
        "--repository-root",
        str(repository_root),
        "--plugin-root",
        str(repository_root / "plugins" / "anti-ai-craft"),
        "--graphify-freshness-kind",
        "ast",
    ]
    if disable_graph:
        args.append("--disable-graph")
    parameters = StdioServerParameters(command=sys.executable, args=args, cwd=repository_root)
    async with Client(stdio_client(parameters)) as client:
        status = await client.call_tool("get_anti_ai_status", {})
        repository = await client.call_tool("inspect_repository", {})
        git = await client.call_tool("inspect_git_diff", {"mode": "combined"})
        scope = await client.call_tool(
            "verify_change_scope",
            {"allowed": STAGE_FOUR_SCOPE, "mode": "combined"},
        )
        validation = await client.call_tool(
            "run_project_validation",
            {"dry_run": True, "timeout_seconds": 300},
        )
        tests = await client.call_tool(
            "run_relevant_tests",
            {"dry_run": True, "timeout_seconds": 300},
        )
        impact = await client.call_tool(
            "analyze_change_impact", {"max_depth": 2, "include_tests": True}
        )
        architecture = await client.call_tool("inspect_architecture", {})
        architecture_audit = await client.call_tool("audit_architecture", {})
        anti_ai = await client.call_tool("audit_anti_ai", {})
        security = await client.call_tool("audit_security", {})
        previous = (
            _load_previous_findings(repository_root, previous_findings_path)
            if previous_findings_path
            else _previous_findings(
                anti_ai.structured_content["findings"],
                security.structured_content["findings"],
            )
        )
        remediation = await client.call_tool(
            "verify_remediation", {"previous_findings": previous}
        )
        bundle_arguments = {
            "allowed": STAGE_FOUR_SCOPE,
            "previous_findings": previous,
            "execute": execute,
            "timeout_seconds": 300,
        }
        if baseline_path:
            bundle_arguments["baseline_path"] = baseline_path
        bundle = await client.call_tool("collect_evidence", bundle_arguments)

    results = {
        "STATUS": {
            "status": "PASS" if status.structured_content["mcp"]["status"] == "available" else "FAIL",
            "summary": status.structured_content["graph"]["detail"],
        },
        "REPOSITORY": _compact(repository.structured_content),
        "GIT": _compact(git.structured_content),
        "SCOPE": _compact(scope.structured_content),
        "VALIDATION": _compact(validation.structured_content),
        "TESTS": _compact(tests.structured_content),
        "GRAPH": {
            "status": _graph_outcome(status.structured_content["graph"]),
            "summary": status.structured_content["graph"],
        },
        "IMPACT": _compact(impact.structured_content),
        "ARCHITECTURE": {
            "status": architecture_audit.structured_content["status"],
            "summary": {
                "inspection": architecture.structured_content["summary"],
                "audit": architecture_audit.structured_content["summary"],
            },
        },
        "ANTI_AI": _compact(anti_ai.structured_content),
        "SECURITY": _compact(security.structured_content),
        "BASELINE": {
            "status": (
                bundle.structured_content.get("baseline", {}).get("overall_status", "NOT_APPLICABLE")
                if bundle.structured_content.get("baseline")
                else "NOT_APPLICABLE"
            ),
            "summary": bundle.structured_content.get("baseline"),
        },
        "REMEDIATION": _compact(remediation.structured_content),
        "EVIDENCE_BUNDLE": {
            "status": bundle.structured_content["overall_status"],
            "summary": bundle.structured_content["summary"],
            "performance": bundle.structured_content["performance"],
            "truncation": bundle.structured_content["truncation"],
        },
    }
    return results


def _previous_findings(anti_ai: list[dict], security: list[dict]) -> list[dict]:
    candidates = [*security, *anti_ai]
    return candidates[:10] or [
        {
            "id": "AA-UNKNOWN-DOGFOOD",
            "category": "dogfood",
            "severity": "INFO",
            "confidence": "LOW",
            "message": "No current supported finding was available for live recheck.",
            "evidence": [],
            "location": None,
            "suggestion": None,
        }
    ]


def _load_previous_findings(repository_root: Path, relative_path: str) -> list[dict]:
    target = (repository_root / relative_path).resolve(strict=True)
    if not target.is_relative_to(repository_root):
        raise ValueError("previous findings path escapes repository root")
    payload = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise ValueError("previous findings file must contain a non-empty JSON array")
    return payload


def _compact(result: dict) -> dict:
    return {
        "status": result["status"],
        "summary": result["summary"],
        "findings": [item["id"] for item in result.get("findings", [])],
        "errors": result.get("errors", []),
    }


def _graph_outcome(graph: dict) -> str:
    if graph["availability"] in {"unavailable", "invalid"}:
        return "MANUAL_REVIEW_REQUIRED"
    if graph["availability"] in {"stale", "disabled"} or graph["freshness"] != "available_and_fresh":
        return "WARNING"
    return "PASS"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    parser.add_argument("--baseline-path")
    parser.add_argument("--previous-findings")
    parser.add_argument("--disable-graph", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    print(
        json.dumps(
            asyncio.run(
                smoke(
                    args.repository_root.resolve(),
                    baseline_path=args.baseline_path,
                    previous_findings_path=args.previous_findings,
                    disable_graph=args.disable_graph,
                    execute=args.execute,
                )
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
