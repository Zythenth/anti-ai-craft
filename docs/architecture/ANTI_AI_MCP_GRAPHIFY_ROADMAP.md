# Anti-AI Craft MCP + Graphify roadmap

## Current stage

**Stage 4 of 4 — HARDENING, SECURITY, AND REMEDIATION (local release validation complete on 2026-08-13; hosted CI pending)**

The current implementation keeps the stable `GraphProvider` boundary and adds
bounded security auditing, compact regression baselines, remediation verification,
an aggregate evidence bundle, opt-in metadata-only observability, process-tree
termination, plugin validation, and a pinned CI matrix. Anti-AI rules still do not
parse Graphify output directly, and graph evidence never replaces deterministic
selection or validation.

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

- [x] Normalize graph-backed evidence through `GraphProvider` only.
- [x] Add bounded change impact with paths, communities, confidence, coverage, and truncation.
- [x] Add Graphify test candidates without reducing deterministic selections or fallback suites.
- [x] Add compact architecture inspection and conservative current-change auditing.
- [x] Add the first four measurable Anti-AI rules with documented false-positive policies.
- [x] Calibrate extracted versus inferred evidence and never invent graph direction.
- [x] Add controlled directed, undirected, stale, inferred, isolated, and large-fanout fixtures.
- [x] Validate Graphify ON/OFF behavior and dogfood all Stage 3 tools against this repository.
- [x] Avoid duplicating Graphify MCP query/path/node tools in the Anti-AI MCP surface.

## Stage 3 implementation log

### Baseline and real Graphify capabilities

The committed Stage 1+2 baseline was clean at `ee56ead`, with 72/72 tests passing.
The Stage 2 dry-run and executable dogfood both passed before Stage 3 edits. The
reported graph baseline matched exactly: 1,451 nodes, 2,285 edges, and 92
communities. It remained `AVAILABLE_BUT_STALE` because the same four JSON files
produce zero nodes. That state was not suppressed or relabeled as fresh.

The real graph had 2,108 extracted and 177 inferred edges. Nodes did not carry
their own confidence field. Its logical `directed` flag was false, so dependency
and dependent capabilities remained false; paths, neighbors, and communities were
usable only as non-directional structural evidence. Directed behavior is supported
and tested with controlled fixtures, but it is not claimed for this repository.

### Graph evidence and impact architecture

- `graph_evidence.py` centralizes provider/freshness metadata, relation direction,
  Graphify provenance, and confidence reduction using the existing evidence enums.
- `GraphProvider` gained bounded exact-file lookup and structural overview methods;
  rules still never read `graphify-out/graph.json`.
- `impact.py` selects one file node per changed file as the stable seed, then performs
  bounded neighbor traversal. This choice came from dogfooding: seeding every symbol
  consumed all 200 slots before external impact could be visited.
- `ChangeImpactService` exposes only optional changed files, depth 1–3, and whether
  to include tests. Internal limits are 100 changed files, 100 lookup nodes per file,
  200 total impact nodes, 400 examined relations, and 50 cross-community paths.
- Direct extracted adjacency may remain `FACT`; inferred edges remain `INFERENCE`;
  multi-hop impact is an inference even when every traversed relation is extracted.
  Stale/unknown freshness reduces confidence and always emits a warning.

Impact ranking uses explainable categories and reasons, not a numeric pseudo-score:
distance, relation provenance, same/cross community, and test-path status. The
result distinguishes `DIRECT`, `LIKELY_INDIRECT`, and `POSSIBLE`, and reports
`LOW`/`MEDIUM`/`HIGH` structural impact risk without calling impact a defect.

### Graph-aware test selection

`RelevantTestService` still computes the complete deterministic Stage 2 selection
first. Graph impact may add deduplicated pytest paths with distance, path,
provenance, freshness, and confidence. Unmapped deterministic paths still select
the package suite; Graphify cannot replace or narrow that fallback. Graph disabled
preserves the deterministic result and reports the unavailable graph in metadata.

Controlled tests prove direct additions, inferred/stale additions, duplicate
deduplication, unavailable graph behavior, deterministic-only behavior, and fallback
preservation. In real dogfooding the deterministic fallback already selected the
entire suite, so Graphify did not reduce execution. It identified seven structural
test candidates and one explicit graph addition (`test_scope.py`), but the broad
fallback already covered them.

### Architecture inspection and audit

`inspect_architecture` returns bounded communities, representative nodes, hotspots,
cross-community edges, and grouped community relations. It calls them graph
communities/structural clusters, never domains, services, layers, or bounded
contexts. It does not infer entrypoints from an undirected degree ranking.

`audit_architecture` attributes a cross-community relation to the current change
only when its source file is Git added/untracked. A relation from a modified file
is recorded as existing-or-undetermined because no historical graph baseline exists.
Directed cycles are checked only when direction capabilities are true and are
attributable only when a new file participates. Changed graph hotspots are a LOW
heuristic prompting broader review, not a violation.

### Initial Anti-AI rules

`audit_anti_ai` evaluates four rules and includes architecture findings:

- `AA-AI-PLACEHOLDER-001`: new production-source comments with TODO/FIXME or
  explicit Python unimplemented tokens; Python tokenization avoids matching detector
  strings and pre-existing lines are excluded.
- `AA-AI-TEST-BYPASS-001`: deleted test files or newly introduced skip/xfail markers.
- `AA-AI-FILE-PROLIFERATION-001`: a compound signal requiring at least six new
  production source files, at least four small files, and at least half with no
  observed external graph relationship. File count alone cannot trigger it.
- `AA-AI-ABSTRACTION-001`: a new abstraction file with graph nodes but no observed
  external structural relationship; tests, likely entrypoints, generated/schema/
  migration files, and likely required interfaces are excluded.

Every rule is a heuristic and returns what it detects, what it cannot prove, known
false positives, and confidence policy. Positive, negative, ambiguous, pre-existing,
and newly introduced cases are covered. No duplication detector was added because
the repository has no justified clone detector and weak lexical similarity would
not meet the finding-quality bar. No validation-bypass rule beyond observable test
deletion/skip evidence was added because generic ignore-pattern matching was too
weak. No authorship conclusion exists.

### Dogfooding, value, and false-positive control

The graph used by final executable dogfooding contained 1,617 nodes, 3,133 edges,
and 92 communities while correctly remaining stale for the four zero-node JSONs.
The first real impact run exposed the all-symbol seed-budget defect and a
self-referential placeholder false positive; both were fixed and regression-tested.

The final Graphify-ON dry run mapped all 19 changed files to 181 bounded impact
candidates across 11 affected communities, found seven candidate tests, and
truncated explicitly at the 200-node limit. Architecture audit retained two honest
review signals: `AA-ARCH-002` identifies the extracted import from the new
`anti_ai_audit.py` to the existing path-confinement helper across graph communities,
and `AA-ARCH-004` notes changed nodes in the bounded hotspot ranking. The first is
intentional utility reuse, not a claimed violation; the second remains LOW. The
combined Anti-AI audit returned those architecture signals and no code-rule finding.

The executable dogfood ran one discovered validation command and one selected test
command; both passed. With Graphify OFF, deterministic repository/Git/scope/
validation/test behavior remained available, impact and architecture required manual
review, and `audit_anti_ai` completed with zero code-rule findings plus an explicit
graph-unavailable warning. Therefore Graphify adds real structural coverage and
review targets, but did not narrow this repository's already broad deterministic
test fallback. The integration remains justified for impact/architecture evidence,
not as a replacement for deterministic checks.

A final post-review code update rebuilt the cache to 1,634 nodes, 3,162 edges, and
96 communities. The same four zero-node JSON retries remain, so freshness is still
`AVAILABLE_BUT_STALE`; the community-label sidecar still contains 93 saved labels
and is not presented as fresh curated naming.

### Complexity, performance, security, and deferrals

The new cohesive modules are 146 lines (`graph_evidence.py`), 625 (`impact.py`),
431 (`architecture.py`), and 564 (`anti_ai_audit.py`). `graph.py` grew from 603 to
838 lines because bounded overview, exact-file lookup, and adjacency traversal remain
provider operations;
splitting DTO-only modules would add navigation. The normalizer has four consumers,
impact has three, and architecture is reused by the combined audit. No single-use
interface, generic utility module, dynamic rule registry, database, daemon, cache
service, or LLM call was added.

The provider continues to cache parsed graph data by file signature. Services reuse
one observed status inside each analysis path to avoid repeated freshness scans.
Traversal, evidence, Git added-line reads, graph overview, and process output all
have explicit limits. Node expansion uses NetworkX adjacency instead of rescanning
every graph edge. The final Graphify-ON dry dogfood completed in 10.6 seconds; the
executable run completed in 149.7 seconds, dominated by two successful full-suite
executions. No optimization beyond those measured traversal corrections was added.

All tools remain read-only with respect to repository content. Git added-line
inspection uses fixed internal argv and existing bounded execution; clients cannot
submit Git or shell arguments. Graph and path confinement remain unchanged. A final
resource review added internal changed-file, neighbor fan-out, and new-source-file
caps, with regression tests for explicit truncation; no confirmed security defect
remained in the Stage 3 scope. The public `audit_security`, historical baseline/delta
comparison, remediation verification, final CI, installation automation, and release
hardening remain Stage 4 work. The
earlier Stage 2 suggestion to add minimal CI in Stage 3 is superseded by the explicit
Stage 3 scope, which defers final CI and production hardening.

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

### AD-014 — File-node seeds and bounded impact propagation

**Status:** accepted for Stage 3.

Impact analysis uses one Graphify file node per changed file as its initial seed.
Symbols are reached through bounded traversal instead of all becoming seeds. This
preserves the changed-file fact while preventing symbol-heavy files from exhausting
the node budget before external relationships are visited. Multi-hop impact is an
inference even when its component edges are extracted.

### AD-015 — Graph-aware tests are additive only

**Status:** accepted for Stage 3.

Deterministic mapping and fallback selection are computed before graph candidates.
Graphify may add and explain candidates, but cannot satisfy an otherwise unmapped
file, remove a direct mapping, narrow a fallback suite, or downgrade deterministic
evidence. Graph unavailability therefore changes only optional structural evidence.

### AD-016 — Structural delta is attributable only when observable

**Status:** accepted for Stage 3.

A relation from a Git added/untracked file is new with that file. Relations touching
modified files are existing-or-undetermined until Stage 4 provides a historical
graph baseline. Cross-community relations are review signals, not violations, and
communities remain structural clusters rather than asserted domains or layers.

### AD-017 — Small explicit Anti-AI rule set

**Status:** accepted for Stage 3.

Stage 3 automates only placeholder, test-bypass, compound file-proliferation, and
isolated-abstraction signals. Each rule consumes current-delta evidence, states what
it cannot prove, lists false positives, and has negative/ambiguous tests. Duplication,
generic validation-bypass, aesthetic, security, and authorship detectors were not
added because the available evidence did not meet the rule-quality bar.

## Security checkpoint

- **Asset:** repository content and structural conclusions.
- **Actor/input:** MCP client selecting a repository/graph path; local filesystem
  may contain symlinks or malformed graph data.
- **Boundary:** MCP input and generated Graphify artifacts into the local process.
- **Controls required:** one resolved repository root, traversal and absolute-path
  rejection, symlink containment, bounded parsing/output, no arbitrary shell tool,
  explicit unavailable/invalid/stale states.
- **Resource controls:** 64 MiB graph input, 100 changed files, 400 traversed
  relations, 2,000 added diff lines, 100 new source files, and 256 KiB per audited
  source file; all truncation remains visible to clients.
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
| 2026-08-13 | Stage 3 committed baseline | `git status --short`; `git rev-parse HEAD`; Stage 2 dry/executable smokes | Clean `main` at `ee56ead`; Stage 1+2 frozen; both Stage 2 dogfood modes passed. |
| 2026-08-13 | Stage 3 baseline suite | `uv run --project plugins/anti-ai-craft/mcp pytest plugins/anti-ai-craft/mcp/tests -q` | 72 passed in 29.39s; 0 failed/skipped. |
| 2026-08-13 | Real relation provenance | bounded `graph.json` metadata inspection | 2,108 extracted and 177 inferred edges; nodes lacked confidence; logical graph remained undirected. |
| 2026-08-13 | Stage 3 focused graph-aware tests | impact/architecture/Anti-AI/relevant-test/server selection | 44 passed initially; focused regression reruns passed after both dogfood corrections. |
| 2026-08-13 | Stage 3 final compile | locked Python `compileall -q` over `src` and `tests` | Exit 0; no syntax/import compilation errors. |
| 2026-08-13 | Stage 3 final graph-consumer regressions | focused graph/impact/architecture/Anti-AI/relevant-test suites | 56 passed in 48.02s; changed-file, neighbor-fanout, new-source truncation, and adjacency traversal are covered. |
| 2026-08-13 | Stage 3 final suite | `uv run --project plugins/anti-ai-craft/mcp pytest plugins/anti-ai-craft/mcp/tests -q` | 108 passed in 71.16s; 0 failed/skipped. |
| 2026-08-13 | Final Stage 3 Graphify update | `uv run --project plugins/anti-ai-craft/mcp graphify update .` | 1,634 nodes, 3,162 edges, 96 communities; four zero-node JSON retries remain and freshness stays stale. |
| 2026-08-13 | Stage 3 Graphify ON dry dogfood | `smoke_stage3_stdio.py .` | All 19 changed files mapped; 181 bounded candidates, 11 communities, 7 tests; explicit truncation; one intentional cross-community import signal and one LOW hotspot finding. |
| 2026-08-13 | Stage 3 executable dogfood | `smoke_stage3_stdio.py . --execute` | Repository/diff/scope/validation passed; one validation and one selected test command passed; graph warnings remained explicit. |
| 2026-08-13 | Stage 3 Graphify OFF dogfood | `smoke_stage3_stdio.py . --disable-graph` | Deterministic tools remained available; graph-only conclusions required manual review; combined Anti-AI audit returned 0 code-rule findings and explicit graph unavailability. |

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

## Stage 3 completion gate

- [x] Stage 1+2 baseline validated at 72 tests and frozen in Git.
- [x] Graph evidence normalization preserves provenance, freshness, confidence, and source.
- [x] Unknown direction is never presented as dependencies or dependents.
- [x] `analyze_change_impact` is bounded, ranked, confidence-aware, and explicit when truncated.
- [x] Graph-aware test candidates only add to the deterministic baseline.
- [x] `inspect_architecture`, `audit_architecture`, and `audit_anti_ai` are exposed.
- [x] Heuristic rules have positive, negative, ambiguous, pre-existing, and new-delta tests.
- [x] Fresh, stale, unknown, unavailable, disabled, directed, undirected, inferred, and fanout behavior is tested.
- [x] Final suite passes at 108 tests; Graphify ON/OFF and executable dogfooding are recorded.
- [x] Real Graphify value and false positives were evaluated without forcing PASS.
- [x] Complexity was reviewed; no Stage 4 security/remediation/baseline/release feature was anticipated.

## Exact prerequisites for Stage 4

1. Freeze or commit the accepted Stage 3 baseline so historical graph comparison
   has an attributable source snapshot.
2. Define a versioned structural-baseline format owned by Anti-AI evidence logic,
   without copying the Graphify graph or making rules parse raw Graphify JSON.
3. Decide which validated findings are eligible for remediation verification and
   preserve approval gates before any write-capable workflow is introduced.
4. Threat-model and bound the planned security graph signals before exposing
   `audit_security`; retain the current no-LLM and no-arbitrary-shell boundaries.
5. Resolve Graphify's four zero-node JSON freshness limitation through an official
   Graphify behavior/API or keep the limitation explicit; do not mark it fresh locally.
6. Register plugin validation reproducibly in the locked repository toolchain before
   adding pinned CI; do not rely on the external system-Python validator implicitly.
7. Define final evidence-bundle, regression-comparison, timeout/memory/concurrency,
   installation, recovery, upgrade, and release acceptance criteria before hardening.

## Stage 4 implementation log

All Stage 4 prerequisites were handled without adding a second knowledge graph or
making the Anti-AI rules depend on Graphify's JSON representation:

- `audit_security` reports bounded, redacted, current-change signals with stable IDs;
- `anti-ai-baseline` creates and validates a compact schema-versioned baseline using
  fingerprints and signatures rather than raw graph nodes, edges, diffs, or secrets;
- `verify_remediation` reruns observable checks and does not trust a caller's claimed
  resolution status; secret removal remains partial until external rotation is proven;
- `collect_evidence` composes the existing evidence producers, plans commands by
  default, and deduplicates execution only for an identical command, working directory,
  and Git state;
- all 13 MCP tools expose the shared result/error contract and metadata-only timings;
- spawned validation is fixed-argv, uses `shell=False`, has bounded output and timeout,
  and terminates the child process tree on supported platforms;
- target-repository and plugin roots are explicit and independently contained;
- the repository contains a locked Python 3.11/3.14 CI matrix, in-package plugin
  validator, release/runbook documentation, and Stage 4 stdio/performance probes.

The threat model is maintained in
`docs/architecture/ANTI_AI_MCP_THREAT_MODEL.md`. It treats repository contents,
diffs, graph caches, subprocess output, baseline files, and MCP arguments as untrusted
inputs. Stateful behavior remains limited to the explicit baseline CLI and the MCP
continues to expose no arbitrary command or general file-write primitive.

### Stage 4 measured evidence

- the real graph grew from 1,634 nodes / 3,162 edges / 96 communities to 1,869 nodes /
  3,945 edges / 112 communities during implementation;
- 20 repeated real-graph impact analyses completed in 39.84 seconds with about 4.36 MiB
  peak traced allocation and no accumulating retained-memory pattern;
- a valid graph near the 64 MiB file limit loaded in 0.11 seconds with about 120 MiB
  peak traced allocation, which is bounded but remains an explicit availability risk;
- Stage 4 dogfooding found and removed a test-bypass false positive, calibrated an
  ambiguous removed-boundary security signal to manual review, and stopped treating
  containment-only graph relations as architectural dependency crossings;
- the final suite passed all 160 tests under Python 3.11 and 3.14, and a clean
  source-only installation repeated the 160-test result under Python 3.14;
- Graphify remains useful and optional. Its four zero-node JSON inputs keep the honest
  status at `AVAILABLE_BUT_STALE`; the implementation does not fabricate freshness.

### Stage 4 completion gate

- [x] Threat model, attack surfaces, trust boundaries, and residual risks documented.
- [x] Security audit, compact baseline, remediation verification, and evidence bundle implemented.
- [x] Secrets are redacted and logging is opt-in and argument-free.
- [x] No arbitrary shell execution or general write-capable MCP tool was added.
- [x] Process limits, process-tree cleanup, path separation, and malformed-input behavior tested.
- [x] Positive, negative, ambiguous, adversarial, concurrency, regression, and integration cases added.
- [x] Memory and performance measured against the real graph and a near-limit graph.
- [x] Codex project configuration, plugin metadata, recovery/upgrade guidance, and pinned CI added.
- [x] Graphify ON, stale, disabled, baseline, remediation, and aggregate evidence paths dogfooded.
- [ ] Hosted CI must pass on the exact release commit before promotion beyond beta/release-candidate status.
