from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters, stdio_client


async def smoke(repository_root: Path, disable_graph: bool) -> dict:
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
        tool = await client.call_tool("get_anti_ai_status", {})
        resource = await client.read_resource("anti-ai://project/status")
        return {
            "tool": tool.structured_content,
            "resource": json.loads(resource.contents[0].text),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    parser.add_argument("--disable-graph", action="store_true")
    args = parser.parse_args()
    print(json.dumps(asyncio.run(smoke(args.repository_root.resolve(), args.disable_graph)), indent=2))


if __name__ == "__main__":
    main()
