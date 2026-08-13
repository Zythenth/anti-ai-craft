from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters, stdio_client


async def smoke(repository_root: Path) -> dict:
    graph_path = repository_root / "graphify-out" / "graph.json"
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "graphify.serve", str(graph_path)],
        cwd=repository_root,
    )
    async with Client(stdio_client(parameters)) as client:
        tools = await client.list_tools()
        stats = await client.call_tool("graph_stats", {})
        query = await client.call_tool(
            "query_graph",
            {"question": "GraphifyProvider AntiAiStatusService", "depth": 1, "token_budget": 500},
        )
        return {
            "tools": [tool.name for tool in tools.tools],
            "stats": stats.content[0].text,
            "query": query.content[0].text,
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    args = parser.parse_args()
    print(json.dumps(asyncio.run(smoke(args.repository_root.resolve())), indent=2))


if __name__ == "__main__":
    main()
