# Anti-AI Craft MCP graph-aware evidence service

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
- `run_relevant_tests`: deterministic path/name selection plus additive bounded Graphify candidates;
- `analyze_change_impact`: changed nodes, bounded direct/indirect reach, structural clusters, paths, and candidate tests;
- `inspect_architecture`: compact communities, representative nodes, hotspots, and cross-community relations;
- `audit_architecture`: conservative current-change structural signals with attributable delta only for new files;
- `audit_anti_ai`: current-diff facts plus the small documented Anti-AI rule set;
- resources `anti-ai://project/status`, `anti-ai://project/repository`, and
  `anti-ai://project/checks`.

Every Stage 2 tool returns the same `CheckResult` envelope with status, summary,
findings, evidence, metadata, and errors. Finding IDs are stable (`AA-REPO-*`,
`AA-GIT-*`, `AA-SCOPE-*`, `AA-VAL-*`, and `AA-TEST-*`). Facts, heuristics,
inferences, and manual-review requirements remain distinct.

## Deterministic and Graphify policy

Repository, Git, scope, and validation tools never consult Graphify. Relevant-test
selection first computes the same deterministic baseline as Stage 2; Graphify may
only add candidates and can never remove or downgrade a direct mapping or fallback
suite. All deterministic behavior continues when the graph is unavailable.

Every graph-aware result includes provider, availability, freshness, node/edge
counts when known, coverage, and explicit truncation. A stale or unknown graph may
support cautious structural observations with a warning and reduced confidence.
An unavailable, invalid, or disabled graph cannot support a structural conclusion;
hybrid tools retain their deterministic evidence instead of crashing.

## Graph-aware evidence

`GraphEvidenceNormalizer` converts `GraphProvider` nodes and relations into the
existing evidence model. It preserves Graphify `EXTRACTED`/`INFERRED` provenance,
freshness, confidence, source location, and direction. It does not create a second
graph. When Graphify's logical graph is undirected, every relation direction is
`UNKNOWN`; the MCP does not call a neighbor a dependency or dependent.

`analyze_change_impact` defaults to Git changes and accepts only three compact
controls: optional `changed_files`, `max_depth` (1–3), and `include_tests`. Traversal
is capped at 100 changed files, 100 nodes per file, 200 total nodes, 400 examined
relations, and 50 cross-community paths. It distinguishes `DIRECT`,
`LIKELY_INDIRECT`, and `POSSIBLE`; indirect propagation is inference even when each
underlying edge is extracted. Ranking reasons are plain-language facts such as
distance, extracted/inferred relations, community crossing, and test paths.
Internal neighbor queries receive the remaining relation budget, so a single dense
node cannot materialize unbounded fan-out before truncation is reported.

`inspect_architecture` treats communities only as graph communities/structural
clusters. It does not infer bounded contexts, layers, services, or entrypoints from
degree. `audit_architecture` can attribute a cross-community relation to the current
change only when it starts at an added/untracked file. For modified files, the
existing-versus-new distinction remains explicitly unavailable until Stage 4 has a
historical graph baseline. Cycles are checked only on a logically directed graph.

## Initial Anti-AI rules and false positives

The first `audit_anti_ai` release intentionally keeps four rules:

- `AA-AI-PLACEHOLDER-001`: new TODO/FIXME or explicit unimplemented-error lines;
- `AA-AI-TEST-BYPASS-001`: deleted test files or newly added skip/xfail markers;
- `AA-AI-FILE-PROLIFERATION-001`: a compound cluster of at least six new production
  source files, predominantly small and structurally isolated;
- `AA-AI-ABSTRACTION-001`: a new abstraction file with graph nodes but no observed
  external relationship.

All four conclusions are heuristics. Added-line inspection distinguishes current
changes from pre-existing markers. File count alone never triggers proliferation.
Tests, fixtures, generated/schema/migration files, likely entrypoints, and likely
required interfaces are excluded from the abstraction/file rules. Dynamic imports,
reflection, registration, generated code, framework scaffolding, deliberate package
boundaries, intentional abstract methods, obsolete tests, and replacement coverage
remain known false positives. The tool returns these limitations and confidence
policy in `metadata.rule_policies`; graph-stale or undirected abstraction evidence is
LOW confidence. No rule infers authorship.

Added-line inspection is capped at 2,000 lines. Anti-AI source inspection reads at
most 100 new source files and 256 KiB per file; reaching either limit is returned as
an explicit warning and `truncated: true` rather than silently producing a complete
claim.

## Command and path security

No public tool accepts a command string or Git argv. Validation commands are
generated from recognized manifest keys and fixed runners. Execution uses
`shell=False`, separate argv, a repository-contained cwd, a controlled
environment, timeout/termination, and explicit stdout/stderr byte limits.
Project-owned package scripts are still code: dry-run shows the selected command
before execution, and callers should review untrusted repository changes first.

Graph input is confined to the repository and capped at 64 MiB. Graph-aware
traversals, overview results, new-source inspection, and evidence lists all have
explicit budgets. These are local availability controls, not proof that generated
graph content is semantically correct.

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
uv run --project plugins/anti-ai-craft/mcp python plugins/anti-ai-craft/mcp/tests/smoke_stage3_stdio.py .
uv run --project plugins/anti-ai-craft/mcp python plugins/anti-ai-craft/mcp/tests/smoke_stage3_stdio.py . --disable-graph
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
