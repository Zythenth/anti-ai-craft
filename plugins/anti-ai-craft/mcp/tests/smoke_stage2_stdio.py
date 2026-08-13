from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters, stdio_client


STAGE_TWO_SCOPE = [
    ".codex/**",
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "docs/architecture/**",
    "plugins/anti-ai-craft/.codex-plugin/plugin.json",
    "plugins/anti-ai-craft/mcp/**",
]


async def smoke(repository_root: Path, execute: bool) -> dict:
    parameters = StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "anti_ai_mcp.server",
            "--repository-root",
            str(repository_root),
            "--plugin-root",
            "plugins/anti-ai-craft",
            "--graphify-freshness-kind",
            "ast",
        ],
        cwd=repository_root,
    )
    async with Client(stdio_client(parameters)) as client:
        repository = await client.call_tool("inspect_repository", {})
        diff = await client.call_tool("inspect_git_diff", {"mode": "combined"})
        scope = await client.call_tool(
            "verify_change_scope",
            {"allowed": STAGE_TWO_SCOPE, "mode": "combined"},
        )
        validation = await client.call_tool(
            "run_project_validation",
            {"dry_run": not execute, "timeout_seconds": 180},
        )
        tests = await client.call_tool(
            "run_relevant_tests",
            {"dry_run": not execute, "timeout_seconds": 180},
        )
    results = {
        "inspect_repository": repository.structured_content,
        "inspect_git_diff": diff.structured_content,
        "verify_change_scope": scope.structured_content,
        "run_project_validation": validation.structured_content,
        "run_relevant_tests": tests.structured_content,
    }
    return {
        name: {
            "status": result["status"],
            "summary": result["summary"],
            "findings": [finding["id"] for finding in result["findings"]],
        }
        for name, result in results.items()
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    result = asyncio.run(smoke(args.repository_root.resolve(), args.execute))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
