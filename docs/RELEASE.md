# Anti-AI Craft release and operations guide

This guide is the operational contract for Anti-AI Craft `0.6.x` and its local
MCP `0.2.x`. The plugin skills and the MCP are related but installed separately:
installing the plugin does not silently register a local process or choose a
repository to analyze.

## Clean installation

Requirements are Git, Python 3.11 or newer, `uv`, and a Codex client that supports
project-scoped MCP configuration. From a fresh checkout:

```bash
uv sync --locked --project plugins/anti-ai-craft/mcp
uv lock --check --project plugins/anti-ai-craft/mcp
uv run --project plugins/anti-ai-craft/mcp anti-ai-plugin-validate plugins/anti-ai-craft --marketplace .agents/plugins/marketplace.json
uv run --project plugins/anti-ai-craft/mcp python -m pytest plugins/anti-ai-craft/mcp/tests -q
```

Generate the optional, deterministic code graph and run a status smoke:

```bash
uv run --project plugins/anti-ai-craft/mcp graphify extract . --code-only --out .
uv run --project plugins/anti-ai-craft/mcp python plugins/anti-ai-craft/mcp/tests/smoke_stdio.py .
```

`graphify-out/`, `.venv/`, `.anti-ai/`, Python caches, and temporary logs are
local artifacts. They are ignored and are not release inputs.

## Target repository and plugin root

The MCP refuses to infer either root. Supply both through arguments or the
`ANTI_AI_REPOSITORY_ROOT` and `ANTI_AI_PLUGIN_ROOT` environment variables:

- `repository-root` is the Git repository being analyzed;
- `plugin-root` is the Anti-AI Craft installation containing
  `.codex-plugin/plugin.json` and `skills/`.

The plugin may be installed outside the target. Graph paths, baseline paths,
working directories, Git operations, and emitted file paths remain confined to
the target repository. A missing or invalid plugin marker fails startup instead
of silently analyzing the plugin source as the target.

## Codex configuration

Codex supports project-scoped `.codex/config.toml` for trusted projects. The
repository configuration uses an STDIO server with an explicit target and plugin:

```toml
[mcp_servers.anti-ai-craft]
command = "uv"
args = [
  "run", "--project", "plugins/anti-ai-craft/mcp", "anti-ai-mcp",
  "--repository-root", ".",
  "--plugin-root", "plugins/anti-ai-craft",
  "--graphify-freshness-kind", "ast",
]
cwd = "."
startup_timeout_sec = 30
tool_timeout_sec = 30
enabled = true
required = false
default_tools_approval_mode = "writes"
```

Verify configured servers with `codex mcp list` or `/mcp`. The official Codex
MCP reference is <https://learn.chatgpt.com/docs/extend/mcp?surface=cli>.

Graphify is registered independently. Disable it by setting
`mcp_servers.graphify.enabled = false`; disable graph evidence inside Anti-AI by
adding `--disable-graph` to the Anti-AI server args. Deterministic Git, scope,
validation, security, and test-selection evidence remains available.

## Baselines and regression comparison

Baseline creation is deliberately not an MCP tool. It is an explicit stateful
administrative CLI operation:

```bash
uv run --project plugins/anti-ai-craft/mcp anti-ai-baseline create --repository-root . --output .anti-ai/baseline.json
uv run --project plugins/anti-ai-craft/mcp anti-ai-baseline validate --repository-root . .anti-ai/baseline.json
```

The versioned `1.0` format stores finding fingerprints, compact repository/tool
identity, architecture signature hashes, compact graph status, and selected check
IDs. It stores neither raw graph nodes/edges nor secret values. Line movement and
redacted-value changes do not create a new fingerprint; rule ID, path, category,
and semantic evidence do. `collect_evidence` compares a supplied repository-local
baseline and labels occurrences `PRE_EXISTING`, `NEW`, `CHANGED`, or `RESOLVED`.

Baselines are repository-specific security evidence. Keep them local by default;
if an organization chooses to version one, review its contents and retention
policy first.

## Recovery

- Broken or corrupt graph: move the local `graphify-out/` aside, then run
  `graphify extract . --code-only --out .`. No source file is deleted.
- Stale graph: run `graphify update .`; if the detector still reports known
  zero-node inputs, keep the stale warning rather than forcing freshness.
- Invalid baseline: run `anti-ai-baseline validate`; recreate it explicitly only
  after reviewing why it is invalid. Never overwrite it automatically.
- MCP startup failure: verify both explicit roots, then run `uv sync --locked` and
  start `anti-ai-mcp` directly to see stderr diagnostics.
- Lock mismatch: do not use an unlocked environment for release evidence. Review
  dependency changes, run `uv lock`, commit the intentional lock update, then
  rerun `uv sync --locked`.
- Graphify unavailable: add `--disable-graph` temporarily. Graph-only conclusions
  become manual review; deterministic tools continue.
- Corrupt local environment: remove only the generated MCP `.venv` after resolving
  its exact path, then recreate it with `uv sync --locked`.

## Upgrade, disable, and uninstall

For a released plugin, update the marketplace snapshot, reinstall, and start a
new task:

```bash
codex plugin marketplace upgrade zythenth
codex plugin add anti-ai-craft@zythenth
uv sync --locked --project plugins/anti-ai-craft/mcp
uv run --project plugins/anti-ai-craft/mcp anti-ai-plugin-validate plugins/anti-ai-craft --marketplace .agents/plugins/marketplace.json
uv run --project plugins/anti-ai-craft/mcp graphify update .
```

To disable without deletion, set the relevant MCP `enabled = false`. To uninstall
the skills, run `codex plugin remove anti-ai-craft@zythenth`. Remove the marketplace
only when no other installed plugin needs it. Local `graphify-out/`, `.anti-ai/`,
and the MCP `.venv` may be removed independently; repository source is preserved.
The project installs no daemon and no hidden Git hook.

## Version policy

- Plugin minor versions add or materially extend user-facing skills/evidence
  capabilities; patch versions are compatible corrections.
- MCP minor versions add tools or additive schema fields; patch versions preserve
  the tool surface and schema.
- Persisted baseline and evidence-bundle schemas have their own `schema_version`.

Stage 4 adds three tools, a baseline CLI, normalized envelopes, and release
operations without removing the ten prior tools. Therefore the release versions
are plugin `0.6.0` and MCP `0.2.0`; neither is labeled stable `1.0`.

## Release artifacts

Include source, six skills and references, `.codex-plugin/plugin.json`, marketplace
metadata, MCP source/tests/lockfile, `.codex/config.toml`, CI, README files, threat
model, roadmap, and this guide. Exclude generated graphs, virtual environments,
repository-specific baselines, caches, logs, coverage output, and temporary files.

## Release checklist

- [x] Locked install passes on Python 3.11 and 3.14.
- [x] `uv lock --check`, compile, all tests, and plugin validation pass.
- [ ] CI is green on the release commit.
- [x] MCP Stage 4 smoke passes with Graphify ON and OFF.
- [x] Stale graph behavior remains explicit.
- [x] Security dogfood has no unresolved HIGH or CRITICAL fact.
- [x] Baseline/regression and remediation workflows pass.
- [x] Evidence bundle reports phase timing and safe deduplication.
- [x] Clean install and documented commands are verified.
- [x] No generated artifact or unexpected working-tree file is included.
- [x] The final diff and dependency changes receive manual review.

Local evidence can qualify a commit as a release candidate, but “CI green” requires
the hosted workflow to run on that exact commit. Until then, classify it as beta or
release-candidate pending CI rather than stable.
