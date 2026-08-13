from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters, stdio_client


STAGE_THREE_SCOPE = [
    "README.md",
    "docs/architecture/**",
    "plugins/anti-ai-craft/mcp/**",
]


async def smoke(repository_root: Path, *, disable_graph: bool, execute: bool) -> dict:
    args = [
        "-m",
        "anti_ai_mcp.server",
        "--repository-root",
        str(repository_root),
        "--plugin-root",
        "plugins/anti-ai-craft",
        "--graphify-freshness-kind",
        "ast",
    ]
    if disable_graph:
        args.append("--disable-graph")
    parameters = StdioServerParameters(command=sys.executable, args=args, cwd=repository_root)
    async with Client(stdio_client(parameters)) as client:
        calls = {
            "inspect_repository": await client.call_tool("inspect_repository", {}),
            "inspect_git_diff": await client.call_tool("inspect_git_diff", {"mode": "combined"}),
            "verify_change_scope": await client.call_tool(
                "verify_change_scope",
                {"allowed": STAGE_THREE_SCOPE, "mode": "combined"},
            ),
            "run_project_validation": await client.call_tool(
                "run_project_validation",
                {"dry_run": not execute, "timeout_seconds": 180},
            ),
            "run_relevant_tests": await client.call_tool(
                "run_relevant_tests",
                {"dry_run": not execute, "timeout_seconds": 180},
            ),
            "analyze_change_impact": await client.call_tool(
                "analyze_change_impact",
                {"max_depth": 2, "include_tests": True},
            ),
            "inspect_architecture": await client.call_tool("inspect_architecture", {}),
            "audit_architecture": await client.call_tool(
                "audit_architecture", {"mode": "combined"}
            ),
            "audit_anti_ai": await client.call_tool("audit_anti_ai", {"mode": "combined"}),
        }
    results = {name: result.structured_content for name, result in calls.items()}
    return {
        name: {
            "status": result["status"],
            "summary": result["summary"],
            "findings": [finding["id"] for finding in result["findings"]],
            "graph": result.get("metadata", {}).get("graph"),
            "graph_added_tests": result.get("metadata", {}).get("graph_added_tests"),
            "candidate_tests": len(
                result.get("metadata", {}).get("candidate_affected_tests", [])
            ),
        }
        for name, result in results.items()
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    parser.add_argument("--disable-graph", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    result = asyncio.run(
        smoke(
            args.repository_root.resolve(),
            disable_graph=args.disable_graph,
            execute=args.execute,
        )
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
