# Anti-AI Craft MCP foundation

This package is the deterministic evidence boundary for Anti-AI Craft. It
keeps the responsibilities deliberately separate:

```text
Codex -> Anti-AI MCP -> GraphProvider -> graphify-out/graph.json
      \-> Graphify MCP (independent structural query surface)
```

Anti-AI rules consume `GraphProvider`; they do not parse Graphify JSON. The
Anti-AI MCP does not call another MCP server.

## Environment

Requirements: Python 3.11+ and `uv`.

```bash
uv sync --project plugins/anti-ai-craft/mcp
```

The lock file pins Graphify `0.9.38`, MCP Python SDK `2.0.0`, and the complete
development environment. Graphify is optional to the Anti-AI MCP runtime: when
its detector is missing, graph freshness becomes `unknown_freshness`; graph
queries can still use a valid local artifact.

## Graph lifecycle

Generate a deterministic code graph:

```bash
uv run --project plugins/anti-ai-craft/mcp graphify extract . --code-only --out .
```

Query and incrementally update it:

```bash
uv run --project plugins/anti-ai-craft/mcp graphify query "GraphProvider"
uv run --project plugins/anti-ai-craft/mcp graphify update .
```

`graphify-out/` is an ignored, regenerable local cache. The versioned inputs are
the package lock/configuration, repository instructions, and Codex MCP config.
No daemon or Git hook is required for correctness; `AGENTS.md` instructs Codex
to run the official incremental update after code changes.

Freshness has four semantic outcomes:

- `available_and_fresh`: Graphify's manifest detector found no relevant change;
- `available_but_stale`: it found changed/new code or deleted manifest entries;
- `unknown_freshness`: the manifest, Graphify package, or detector is unavailable;
- `unavailable`: no valid graph can be loaded.

Availability separately distinguishes `available`, `stale`, `unavailable`,
`invalid`, and `disabled`. A missing or invalid graph does not permanently lock
the process into fallback: `GraphifyProvider` detects a later rebuild.

Graphify `0.9.38` currently retries four JSON configuration files that produce
zero nodes in this repository. The provider therefore reports the real graph as
stale after update instead of claiming freshness without evidence.

## MCP surface

Start over stdio:

```bash
uv run --project plugins/anti-ai-craft/mcp anti-ai-mcp \
  --repository-root . \
  --plugin-root plugins/anti-ai-craft \
  --graphify-freshness-kind ast
```

The MCP surface is:

- `get_anti_ai_status`: integration and Graphify lifecycle status;
- `inspect_repository`: bounded filesystem/manifest/Git inventory;
- `inspect_git_diff`: staged, working-tree, or combined changes;
- `verify_change_scope`: allowed/denied/exception path rules, including both rename endpoints;
- `run_project_validation`: discovered project checks with optional `dry_run`;
- `run_relevant_tests`: deterministic path/name selection with an explicit fallback or manual review;
- resources `anti-ai://project/status`, `anti-ai://project/repository`, and
  `anti-ai://project/checks`.

Every Stage 2 tool returns the same `CheckResult` envelope with status, summary,
findings, evidence, metadata, and errors. Finding IDs are stable (`AA-REPO-*`,
`AA-GIT-*`, `AA-SCOPE-*`, `AA-VAL-*`, and `AA-TEST-*`). Facts, heuristics,
inferences, and manual-review requirements remain distinct.

## Deterministic and Graphify policy

Repository, Git, scope, validation, and relevant-test tools never consult
Graphify. They continue unchanged when the graph is fresh, stale, unavailable,
invalid, disabled, or has unknown freshness. A later graph-aware tool may use a
stale/unknown graph only with an explicit warning when current structure is not
required; it must require manual review when freshness is material. An
unavailable, invalid, or disabled graph cannot provide graph evidence.

## Command and path security

No public tool accepts a command string or Git argv. Validation commands are
generated from recognized manifest keys and fixed runners. Execution uses
`shell=False`, separate argv, a repository-contained cwd, a controlled
environment, timeout/termination, and explicit stdout/stderr byte limits.
Project-owned package scripts are still code: dry-run shows the selected command
before execution, and callers should review untrusted repository changes first.

All paths emitted to clients are repository-relative POSIX paths. Scope patterns
reject absolute paths and traversal, deny rules take precedence, exceptions do
not override denies, and a rename checks both source and destination.

## Validation

```bash
uv run --project plugins/anti-ai-craft/mcp pytest plugins/anti-ai-craft/mcp/tests -q
uv run --project plugins/anti-ai-craft/mcp python plugins/anti-ai-craft/mcp/tests/smoke_stdio.py .
uv run --project plugins/anti-ai-craft/mcp python plugins/anti-ai-craft/mcp/tests/smoke_stdio.py . --disable-graph
uv run --project plugins/anti-ai-craft/mcp python plugins/anti-ai-craft/mcp/tests/smoke_graphify_stdio.py .
uv run --project plugins/anti-ai-craft/mcp python plugins/anti-ai-craft/mcp/tests/smoke_stage2_stdio.py .
uv run --project plugins/anti-ai-craft/mcp python plugins/anti-ai-craft/mcp/tests/smoke_stage2_stdio.py . --execute
```

The tests use isolated repositories for graph lifecycle, Git states, rename/move
scope bypasses, Python/Node/multi-package inspection, validation success/failure,
timeouts, large output, cwd containment, deterministic test mapping/fallback,
and MCP tool/resource behavior with Graphify stale and disabled.

## Current primary references

- [MCP tools specification (2026-07-28)](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [MCP resources specification (2026-07-28)](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
- [Graphify repository](https://github.com/Graphify-Labs/graphify)
- [Graphify MCP](https://graphify.com/mcp)
