# Anti-AI Craft project instructions

Keep the responsibilities separate:

- Graphify answers what exists and how repository elements are connected.
- Anti-AI Craft skills decide whether work is acceptable under their contracts.
- The Anti-AI MCP provides read-only status/evidence and depends on `GraphProvider`,
  never directly on Graphify JSON from rules.

Do not add a second knowledge graph, make rules parse `graphify-out/graph.json`,
or add arbitrary shell execution to the Anti-AI MCP. Generated `graphify-out/`
content is a local cache and is not committed.

## Graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `uv run --project plugins/anti-ai-craft/mcp graphify query "<question>"` when `graphify-out/graph.json` exists. Use the same prefix with `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than `GRAPH_REPORT.md` or raw repository scans.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `uv run --project plugins/anti-ai-craft/mcp graphify update .` to keep the code graph current (AST-only, no API cost).
