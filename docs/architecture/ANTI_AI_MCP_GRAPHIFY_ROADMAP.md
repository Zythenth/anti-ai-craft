# Anti-AI Craft MCP + Graphify roadmap

## Current stage

**Stage 2 of 4 — DETERMINISTIC MCP (complete on 2026-08-13)**

The current objective is a small local MCP vertical slice backed by a stable
`GraphProvider` boundary. Anti-AI rules must not parse Graphify output directly.

## Four-stage roadmap

### STAGE 1 — FOUNDATION + GRAPHIFY

- [x] Assess repository structure, contracts, scripts, configuration, Git state, and existing automation.
- [x] Verify current primary MCP, Codex MCP, MCP Python SDK, and Graphify documentation.
- [x] Create and begin maintaining this roadmap.
- [x] Add reproducible Graphify generation, query, and update commands.
- [x] Decide and implement generated-output commit/ignore/cache policy.
- [x] Add project-scoped Codex integration without overwriting existing instructions or hooks.
- [x] Implement `GraphProvider`, `GraphifyProvider`, and explicit null fallback.
- [x] Preserve structural provenance and distinguish fact, heuristic, inference, and manual review.
- [x] Implement graph availability, validity, capability, and freshness reporting.
- [x] Implement the Anti-AI MCP server foundation.
- [x] Implement the read-only `get_anti_ai_status` tool.
- [x] Implement the compact `anti-ai://project/status` resource.
- [x] Add deterministic path-boundary and provider tests.
- [x] Add MCP tool/resource integration tests.
- [x] Generate and query the Anti-AI Craft graph.
- [x] Pass Graphify ON and Graphify OFF smoke tests.
- [x] Reconcile validation evidence and Stage 1 definition of done.

### STAGE 2 — DETERMINISTIC MCP

- [x] Audit the Stage 1 foundation and record its justified complexity and concrete fixes.
- [x] Formalize graph freshness behavior for deterministic and future graph-aware tools.
- [x] Define the shared `CheckResult`, `Finding`, severity, confidence, and evidence contracts.
- [x] Add stable finding IDs and a minimal `Rule` protocol consumed by scope rules.
- [x] Add deterministic repository, Git diff, and change-scope tools.
- [x] Add bounded validation discovery/execution without arbitrary shell access.
- [x] Add deterministic relevant-test selection, fallback, dry-run, and execution evidence.
- [x] Add compact repository and validation-capability resources without duplicate logic.
- [x] Preserve skills as the judgment layer; keep the MCP evidence-focused.
- [x] Complete final suite/smoke/dogfooding evidence and complexity review.

## Stage 2 implementation log

### Stage 1 foundation review

The pre-change package contained 1,239 lines of Python source and tests excluding
the generated lock file and environment: `graph.py` was 613 lines, `server.py`
111, `status.py` 91, `evidence.py` 27, and the five test/smoke modules 389. The
recorded baseline was 15 passing tests plus Graphify ON/OFF stdio smokes.

The size of `graph.py` was not by itself a defect. Its graph model, provider
contract, bounded Graphify loader, normalization, and traversal operations share
one real boundary and remain cohesive. Splitting graph DTOs or traversal helpers
would add navigation without reducing responsibility. One independent policy was
identified: repository path containment now has multiple non-graph consumers. It
was moved to `paths.py` and remains imported by `graph.py`, preserving the public
symbol used by Stage 1 tests.

Concrete Stage 1 fixes:

- the minimal evidence type was expanded instead of duplicated by every new tool;
- plugin-root parsing is now physically confined to the configured repository;
- an unchanged invalid/oversized graph signature is cached as invalid instead of
  repeatedly parsing up to the 64 MiB input limit;
- manifest/config/untracked-file reads reuse physical path containment and reject
  symlink escape.

`GraphProvider`/`GraphifyProvider` remain justified boundaries: the protocol is
the accepted separation from Graphify JSON, the null provider preserves explicit
disabled/unavailable semantics, and the adapter can recover after a graph rebuild.
`status.py` keeps its small fixed-argv Git identity probe; replacing it with the
larger Stage 2 diff service would increase coupling without changing its contract.

### Implemented deterministic architecture

- `evidence.py`: central result/finding/error model and shared enums;
- `paths.py`: canonical repository-relative POSIX paths plus lexical/physical containment;
- `rules.py`: minimal five-field `Rule` protocol, no discovery/plugin framework;
- `repository.py`: bounded factual repository inventory;
- `git.py`: fixed-argv Git inspection for staged, working-tree, and combined modes;
- `scope.py`: allowed/denied/exception rules using Git path endpoints only;
- `execution.py`: shell-free bounded process runner;
- `checks.py`: manifest-derived validation discovery and bounded execution;
- `relevant_tests.py`: deterministic relevant-test mapping, fallback, and execution;
- `server.py`: six tools and three resources, with deterministic services independent
  from the graph provider.

No Stage 3 impact, architecture, graph-aware scope, or graph-aware test selection
was added.

The final complexity pass split `checks.py` after it reached 863 lines and held
two independently testable services. The result is a one-way dependency:
`relevant_tests.py` consumes the check model/discovery/execution result from
`checks.py`; validation does not depend on test selection. Final cohesive module
sizes are 603 lines for the Graphify boundary, 477 for validation, 466
for repository inspection, 416 for relevant tests, 322 for Git, 271 for server
wiring, 265 for scope, and 250 for bounded process execution. No one-line wrapper
layer or generic utility module was introduced.

### Known Stage 2 limitations

- Check discovery currently recognizes Python `pyproject.toml` and Node
  `package.json` conventions; other ecosystems remain factual repository metadata
  but do not produce executable checks yet.
- Python direct test mapping is convention-based and therefore `HEURISTIC`. If any
  changed path lacks a direct mapping, the configured package suite is selected;
  without a suite the result is `MANUAL_REVIEW_REQUIRED`.
- Package scripts are repository-owned code. The MCP allowlists how a script is
  selected and invoked, but cannot make a malicious project script safe; dry-run
  and review remain the trust boundary.
- Process output is capped at 128 KiB per stream, Git parsing at 2 MiB, repository
  inspection at 10,000 files/100 returned entries per section, and scope inputs at
  100 patterns per list. Every truncation is explicit.
- Graphify's four zero-node JSON retries still make the real graph stale; deterministic
  tools intentionally ignore that state.

### CI decision

CI is deferred in Stage 2. The package now has enough tests to justify CI, but the
entire Stage 1/2 package and configuration are still an uncommitted working-tree
addition, and the repository's plugin validator currently lives outside this
package. Adding a third-party action and pretending that external validator is a
stable in-repository command would widen the supply-chain/trust boundary before
the local contracts are accepted. Stage 3 should add one pinned, single-version
workflow after this stage is committed and the plugin-validation command is made
reproducible from the repository.

The external validator was still exercised separately: it failed under the MCP
locked environment because `PyYAML` is not a package dependency, then passed with
the existing system Python 3.14/PyYAML 6.0.3. This confirms the plugin while also
confirming that it must not be advertised as a discovered locked MCP check yet.

### STAGE 3 — GRAPH-AWARE INTELLIGENCE

- [ ] Add graph-backed impact and scope analysis through `GraphProvider` only.
- [ ] Add dependency, dependent, path, and community evidence to selected rules.
- [ ] Calibrate extracted versus inferred Graphify evidence.
- [ ] Add graph-aware validation fixtures and failure-mode tests.
- [ ] Avoid duplicating Graphify MCP tools in the Anti-AI MCP surface.

### STAGE 4 — HARDENING + DOGFOODING

- [ ] Run the Anti-AI MCP against Anti-AI Craft changes by default.
- [ ] Harden time, memory, input-size, path, and concurrency limits.
- [ ] Add compatibility, upgrade, and stale-graph operational tests.
- [ ] Add CI enforcement only after local contracts are stable.
- [ ] Document rollout, failure recovery, and contributor workflows.

## Architecture decisions

### AD-001 — Graphify remains the knowledge-graph owner

**Status:** accepted.

Anti-AI Craft will not build a second graph, copy Graphify internals, or expose
Graphify's full API. The only Graphify-aware implementation is the adapter behind
`GraphProvider`.

### AD-002 — Python + uv for the MCP foundation

**Status:** accepted for Stage 1.

The repository already contains maintained Python utilities, and the installed
Graphify CLI is a Python package. `uv` is present and is also Graphify's recommended
isolated installer. The official MCP Python SDK v2 supports typed tools, resources,
structured output, stdio, and in-memory client/server tests.

### AD-003 — Local stdio MCP servers

**Status:** accepted for Stage 1.

Both Anti-AI Craft MCP and Graphify MCP will use local stdio processes. No daemon,
HTTP listener, database, or MCP-to-MCP call is required. Codex may connect to both
servers independently.

### AD-004 — Graphify access strategy

**Status:** accepted for Stage 1.

`GraphifyProvider` will read the documented generated `graphify-out/graph.json`
artifact for bounded local traversal and normalization. Freshness will use the
installed Graphify API when available instead of reimplementing Graphify's manifest
algorithm. If that API is unavailable, freshness is explicitly unknown. Anti-AI
rules never receive raw Graphify JSON.

### AD-005 — Repository root is explicit and confined

**Status:** accepted.

The MCP process resolves one repository root at startup from a controlled CLI option
or environment variable, then falls back to its launch directory. Graph paths are
resolved relative to that root and rejected if lexical resolution or symlink
resolution escapes it.

### AD-006 — Generated Graphify output is reproducible cache

**Status:** accepted after measuring the real graph.

The current default is to regenerate and ignore `graphify-out/` rather than version
large or machine-specific outputs. Small source configuration and commands are
versioned. The final code graph contains 1,237 nodes and 1,474 edges and is roughly
1.25 MB; Graphify also generates HTML, reports, query logs, backups, and analysis
sidecars. These remain ignored together as one regenerable cache.

### AD-007 — Evidence provenance survives normalization

**Status:** accepted.

Normalized evidence records distinguish `FACT`, `HEURISTIC`, `INFERENCE`, and
`MANUAL_REVIEW_REQUIRED`. Graphify confidence/provenance metadata is retained when
present; absent metadata is not invented.

### AD-008 — Manual incremental update, no required Git hook

**Status:** accepted for Stage 1.

`graphify codex install` was run and its output inspected. Its generated Codex
PreToolUse command is an intentional no-op in Codex Desktop, so it is retained only
in portable `uv run` form; it is not treated as freshness enforcement. `AGENTS.md`
requires the official `graphify update .` after code changes. No daemon or required
Git hook was added.

### AD-009 — Independent MCP servers

**Status:** accepted.

Project-scoped `.codex/config.toml` configures Anti-AI MCP and Graphify MCP as two
independent stdio servers. Anti-AI MCP does not call Graphify MCP. The adapter reads
the bounded artifact for low-complexity local operations, while Codex may use the
official Graphify MCP tools directly for richer structural questions.

### AD-010 — Graph freshness policy by dependency

**Status:** accepted for Stage 2.

Graph state never globally gates the MCP. Tool behavior is determined by whether
the specific operation needs graph evidence:

| Effective graph state | Deterministic tools | Future graph-aware tools |
| --- | --- | --- |
| `AVAILABLE_AND_FRESH` | run normally without consulting Graphify | may use graph evidence with provenance |
| `AVAILABLE_BUT_STALE` | run normally | may return non-fresh evidence plus warning only when current structure is not required; otherwise `MANUAL_REVIEW_REQUIRED` |
| `UNKNOWN_FRESHNESS` | run normally | same as stale, with the freshness gap stated explicitly |
| `UNAVAILABLE` | run normally | omit optional graph evidence or require manual review when graph evidence is required |
| `INVALID` | run normally | never use the invalid artifact; return error/manual review according to the tool contract |
| `DISABLED` | run normally | treat graph evidence as intentionally unavailable, without trying to bypass configuration |

The first four names are `GraphFreshness` outcomes. `INVALID` and `DISABLED` are
existing `GraphAvailability` outcomes and are not duplicated into a second enum.
Stage 2 tools do not accept a `GraphProvider`, which makes their independence
structural rather than a runtime conditional.

### AD-011 — One evidence/result envelope and stable rule findings

**Status:** accepted for Stage 2.

Every deterministic tool returns `CheckResult(status, summary, findings,
evidence, metadata, errors)`. Findings carry a stable category ID, severity,
confidence, message, evidence, optional location, and suggestion. The existing
`EvidenceKind` remains the provenance authority; no duplicate fact/heuristic enum
was introduced. Scope uses two concrete rules behind a minimal `Rule` protocol.
There is no dynamic discovery, dependency-injection container, or plugin system.

### AD-012 — Manifest-derived commands, never client-provided shell

**Status:** accepted for Stage 2.

The client selects only documented categories/modes/dry-run/timeout. The service
derives fixed argv from recognized manifest keys and runners. Git argv is wholly
internal. Execution is `shell=False`, bounded by repository cwd, controlled env,
timeout/termination, and per-stream byte limits. A project script is trusted only
as repository-owned executable code, not as sanitized data; dry-run exposes the
selection before execution.

### AD-013 — Validation capability is a resource, not an extra tool

**Status:** accepted for Stage 2.

`anti-ai://project/checks` reuses the same discovery service consumed by execution.
No `discover_project_checks` tool was added because it would duplicate that
resource and enlarge the selection surface without a distinct behavior.

## Security checkpoint

- **Asset:** repository content and structural conclusions.
- **Actor/input:** MCP client selecting a repository/graph path; local filesystem
  may contain symlinks or malformed graph data.
- **Boundary:** MCP input and generated Graphify artifacts into the local process.
- **Controls required:** one resolved repository root, traversal and absolute-path
  rejection, symlink containment, bounded parsing/output, no arbitrary shell tool,
  explicit unavailable/invalid/stale states.
- **Adversarial scenario:** `../../outside-repository`, an absolute outside path, or
  an in-repository symlink targeting an external graph.
- **Legitimate scenario:** the default `graphify-out/graph.json` inside the selected
  repository.
- **Residual risk:** graph content is generated input and may be semantically wrong;
  consumers must preserve provenance and require manual review for unsupported
  conclusions.

## Known limitations

- The repository still has no CI workflow or root application package. Stage 1 adds
  a scoped Python MCP package and test suite under the plugin.
- Graphify `0.9.38` and its MCP extra are pinned in the project `uv.lock`; a global
  Graphify installation is not relied upon.
- The detected corpus contains 217 files and about 891,800 words: 10 code, 96
  documents, 1 PDF, and 110 images. A code-only graph is deterministic and local but
  will not represent most documentation or image semantics.
- MCP roots are deprecated in the 2026-07-28 protocol, so Stage 1 does not depend on
  client-provided roots. Project configuration/explicit startup root is required.
- Freshness cannot be called fresh when Graphify's incremental detector is absent or
  cannot evaluate the repository; that state is reported as unknown.
- Graphify `0.9.38` retries four JSON configuration files (`marketplace.json`,
  `hooks.json`, `plugin.json`, and `progress.json`) because they produce zero nodes.
  Its detector therefore reports the updated real graph as stale with four pending
  code files. Anti-AI Craft preserves that explicit state rather than suppressing it.
- The generated Graphify graph is logically undirected. Direction-dependent
  `dependencies` and `dependents` capabilities are therefore false; path and
  neighbor capabilities remain available without inventing direction.
- The MCP is project-scoped in Stage 1. Packaging it as an automatically started
  marketplace plugin component is deferred until install-root/repository-root
  semantics are designed and tested.

## Open questions

- Can the complete documentation/image corpus be extracted reproducibly in this
  environment without introducing a required external model backend? Stage 1 ships
  the verified code-only graph workflow; semantic coverage remains optional.
- Should a future release bundle Graphify as an Anti-AI plugin dependency, or keep it
  as an independently installed companion? Stage 1 keeps the dependency optional at
  runtime and explicit in the development environment.
- Should a future stage convert the four persistent zero-node Graphify retries into
  `unknown_freshness` rather than `stale`, if Graphify exposes an official empty-file
  manifest state? Stage 1 follows the current detector literally.

## Validation evidence

| Date | Claim | Command/source | Result |
| --- | --- | --- | --- |
| 2026-08-13 | Git baseline | `git status --short --branch`; `git rev-parse HEAD` | Clean `main`; HEAD `d3b8d632f68840e6ab13842f28d29c0f9646640d`. |
| 2026-08-13 | Graphify installation | `graphify --version` | `graphify 0.9.38`. |
| 2026-08-13 | Package manager | `uv --version` | `uv 0.11.32`. |
| 2026-08-13 | Existing hook state | `graphify hook status` | post-commit/post-checkout/merge driver not installed. |
| 2026-08-13 | Existing graph | path check | `graphify-out/graph.json` absent before Stage 1 work. |
| 2026-08-13 | Corpus | `graphify.detect.detect(Path('.'))` | 217 files, ~891,800 words, no sensitive skips. |
| 2026-08-13 | MCP protocol | [MCP 2026-07-28 tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), [resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources) | Typed tools/resources and structured content verified against current primary specification. |
| 2026-08-13 | MCP Python SDK | [official Python SDK](https://github.com/modelcontextprotocol/python-sdk) | v2 is the current stable line; Python 3.10+, typed server and in-memory client supported. |
| 2026-08-13 | Codex MCP | [official Codex MCP documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) | stdio and project-scoped `.codex/config.toml` supported. |
| 2026-08-13 | Graphify behavior | [official Graphify repository](https://github.com/Graphify-Labs/graphify), [Graphify MCP](https://graphify.com/mcp) | `graphifyy`, `graphify-out/graph.json`, incremental update, Codex integration, and separate MCP server verified. |
| 2026-08-13 | Reproducible environment | `uv sync --project plugins/anti-ai-craft/mcp --locked` | 68 packages resolved; 66 installed packages checked; lock accepted. |
| 2026-08-13 | Unit/integration tests | `uv run --project plugins/anti-ai-craft/mcp pytest plugins/anti-ai-craft/mcp/tests -q` | 15 passed in 1.32s; 0 failed, 0 skipped. |
| 2026-08-13 | Plugin manifest | `python .../plugin-creator/scripts/validate_plugin.py plugins/anti-ai-craft` | Plugin validation passed. |
| 2026-08-13 | Graph generation | `uv run --project plugins/anti-ai-craft/mcp graphify extract . --code-only --out .` | Generated graph successfully; initial Stage 1 graph had 184 nodes, 406 edges, 15 communities. |
| 2026-08-13 | Incremental graph update | `uv run --project plugins/anti-ai-craft/mcp graphify update .` | Final graph rebuilt: 1,237 nodes, 1,474 edges, 89 communities; four zero-node JSON retries reported. |
| 2026-08-13 | Graph query | `uv run --project plugins/anti-ai-craft/mcp graphify query "GraphProvider create_server" --budget 800` | Found `GraphProvider`, `create_server`, `AntiAiStatusService`, provider operations, and tests. |
| 2026-08-13 | Codex MCP config | `codex mcp list` | Both `anti-ai-craft` and `graphify` project servers listed as enabled. |
| 2026-08-13 | Anti-AI MCP ON smoke | `uv run --project plugins/anti-ai-craft/mcp python plugins/anti-ai-craft/mcp/tests/smoke_stdio.py .` | Tool and resource returned Graphify provider, 1,237 nodes, 1,474 edges, six skills, and explicit stale state. |
| 2026-08-13 | Anti-AI MCP OFF smoke | same command with `--disable-graph` | Tool/resource returned `disabled`; every graph capability false. |
| 2026-08-13 | Graphify MCP smoke | `uv run --project plugins/anti-ai-craft/mcp python plugins/anti-ai-craft/mcp/tests/smoke_graphify_stdio.py .` | 10 tools listed; `graph_stats` and `query_graph` succeeded; 98% extracted and 2% inferred evidence. |
| 2026-08-13 | Stage 2 locked environment | `uv lock --project plugins/anti-ai-craft/mcp --check` | Lock accepted; 68 packages resolved. |
| 2026-08-13 | Stage 2 compile | `python -m compileall -q` over `src` and `tests` in the locked environment | Exit 0; no syntax/import compilation error. |
| 2026-08-13 | Stage 2 unit/integration suite | `uv run --project plugins/anti-ai-craft/mcp pytest plugins/anti-ai-craft/mcp/tests -q` | 72 passed in 29.85s; 0 failed/skipped. |
| 2026-08-13 | Stage 2 security regressions | same suite | Covered path traversal/absolute/symlink boundaries, repository PATH shadowing, shell metacharacters as argv, cwd containment, timeout termination, non-finite timeout, huge stdout/stderr, and invalid manifests/globs. |
| 2026-08-13 | Deterministic tools with stale/off graph | MCP integration tests and Stage 1 ON/OFF smokes | Stale and disabled providers produced identical deterministic Git results; 72-test suite passed. |
| 2026-08-13 | Stage 2 dry-run dogfood | `smoke_stage2_stdio.py .` | Repository/diff/scope/validation `PASS`; relevant tests `WARNING` with stable `AA-TEST-005` fallback; nothing executed. |
| 2026-08-13 | Stage 2 executable dogfood | `smoke_stage2_stdio.py . --execute` | 550 files inspected; 36 changed files; all 36 in declared scope; one validation command passed; one safe fallback test command passed with explicit `AA-TEST-005` warning. |
| 2026-08-13 | Plugin validation | system Python + existing `plugin-creator/scripts/validate_plugin.py plugins/anti-ai-craft` | Passed. Locked MCP Python attempt was recorded as unavailable because `PyYAML` is external to the package. |
| 2026-08-13 | Final Graphify update | `uv run --project plugins/anti-ai-craft/mcp graphify update .` | 1,451 nodes, 2,285 edges, 92 communities; four known zero-node JSON retries remain. |
| 2026-08-13 | Current working-tree evidence | `GitInspector.inspect("combined")` before final roadmap reconciliation | 35 files, 6,755 added/6 removed, no truncation; the final `relevant_tests.py` split increased the subsequent dogfood count to 36 files. Stage 1 was uncommitted, so these are cumulative Stage 1+2 working-tree figures. |

## Stage 1 completion gate

The Stage 1 checklist above is authoritative. An item changes to `[x]` only after
the corresponding command, test, or inspected artifact is recorded in this file.

## Stage 2 completion gate

- [x] Stage 1 foundation and complexity reviewed with concrete, limited fixes.
- [x] Freshness policy formalized without duplicating graph enums.
- [x] Central result/evidence model and stable finding IDs implemented.
- [x] Minimal `Rule` contract consumed by deterministic scope rules.
- [x] `inspect_repository`, `inspect_git_diff`, `verify_change_scope`,
  `run_project_validation`, and deterministic `run_relevant_tests` exposed over MCP.
- [x] Paths normalized repository-relative; lexical, physical, and cwd containment tested.
- [x] Fixed-argv process policy, controlled environment, timeout/termination, PATH
  shadow protection, and explicit output limits tested.
- [x] Facts and heuristics remain distinct; test mappings expose `selection_reason`.
- [x] Critical Git/scope/validation/relevant-test fixtures pass.
- [x] Graphify stale/off integration tests pass without gating deterministic tools.
- [x] Dry-run and executable dogfooding recorded without forcing a pass.
- [x] Complexity reviewed after implementation; independent check/test-selection
  responsibilities split, with no cosmetic Graphify refactor.
- [x] No Stage 3/4 graph-aware audit, impact, remediation, or baseline feature added.

## Exact prerequisites for Stage 3

1. Commit or otherwise freeze the Stage 1+2 baseline so future diffs have an
   attributable comparison point; the current Git worktree is cumulative.
2. Preserve `GraphProvider` as the only graph boundary and implement graph-aware
   evidence as an optional complement to deterministic results, never as a parser
   in rules.
3. Define, per new graph-aware tool, whether stale/unknown data permits a warning
   or requires `MANUAL_REVIEW_REQUIRED`, using AD-010.
4. Add directed and undirected graph fixtures for dependencies, dependents, paths,
   communities, and extracted/inferred provenance before exposing impact analysis.
5. Keep deterministic scope and test selection unchanged as the baseline; add
   graph-aware impact/consumer evidence in separate fields and compare outcomes.
6. Add a pinned minimal CI workflow only after the baseline is committed and a
   plugin validator is registered reproducibly inside the repository/locked toolchain.
