# Anti-AI MCP threat model

## Scope and security objective

This model covers the local Anti-AI MCP process, its read-only evidence tools,
the explicit baseline administration CLI, and the local Graphify adapter. It does
not claim that a target repository or its project scripts are trustworthy. The
security objective is narrower: keep analysis confined to the explicitly selected
repository, avoid leaking repository secrets, bound local resource consumption,
preserve evidence provenance, and make command execution deliberate and observable.

External networks, offensive exploitation, hosted services, and production secret
rotation are out of scope. Graphify semantic backends remain optional and separate;
Anti-AI MCP tools do not make network requests.

## Assets

- target repository content, source code, configuration, and accidentally committed secrets;
- Git metadata and the current staged, unstaged, and untracked change set;
- MCP requests, structured responses, errors, and stderr diagnostics;
- the local `graphify-out/graph.json` artifact and its freshness/provenance metadata;
- compact Anti-AI baseline documents and finding fingerprints;
- validation/test execution results and the developer machine resources used to obtain them;
- Anti-AI Craft plugin metadata and skills, which are distinct from the target repository.

## Actors and assumptions

- The MCP host/operator chooses the target repository and plugin root at process startup.
- A repository author may control files, manifests, filenames, Git diffs, and project scripts.
- An MCP client may submit malformed, oversized, duplicated, or traversal-oriented arguments.
- Graphify output is generated but untrusted input: it can be stale, malformed, very large, or
  semantically wrong.
- The local operating system, Python runtime, Git executable, and locked dependencies are trusted
  to the extent required to run a local development tool; repository-local executable shadowing is
  not trusted.

## Trust boundaries and invariants

| Boundary | Controllable input | Required invariant |
| --- | --- | --- |
| MCP client -> public tool arguments | paths, globs, enums, lists, findings, timeouts | validate type/range/count; reject traversal and unsupported values with a controlled error |
| startup configuration -> target repository | repository root, plugin root, graph path | target repository is explicit; graph/baseline paths stay inside it; plugin metadata is validated separately and is never inferred as the target |
| repository files -> parsers | JSON, TOML, source, encodings, filenames | bounded reads, controlled decoding, schema checks, no unsafe deserialization |
| Git -> `GitInspector` | status, diff, filenames, no-commit/detached states | fixed argv, bounded output, normalized repository-relative endpoints, no client Git argv |
| repository manifests -> validation execution | recognized scripts and runners | fixed runner argv, `shell=False`, contained cwd, controlled environment, explicit dry run, timeout and output bounds |
| MCP process -> subprocess tree | Git, validation, tests | trusted executable resolution, finite timeout, whole-tree termination, no stdin, bounded stdout/stderr |
| Graphify artifact -> `GraphProvider` | graph JSON, nodes, edges, provenance | repository confinement, 64 MiB limit, unique node IDs, valid endpoints, bounded traversal, explicit freshness/direction |
| current evidence -> baseline/remediation | prior findings, fingerprints, structural signatures | schema versioning, compact normalized fields, no blind trust in a claimed `fixed` flag, no silent baseline overwrite |
| tool result -> logs/client | summaries, findings, errors | never log full diffs, file bodies, tokens, or unredacted credential-like values |

## Risk register

Likelihood and impact are contextual (`LOW`, `MEDIUM`, `HIGH`), not probabilities.

| Risk | Likelihood | Impact | Required mitigation/evidence | Residual risk |
| --- | --- | --- | --- | --- |
| Path traversal or symlink/junction escape reads outside the target repository | Medium | High | lexical and physical containment; both rename endpoints checked; adversarial path/symlink tests | TOCTOU remains possible when a local actor can replace paths during a read |
| Installed plugin directory is mistaken for the repository being analyzed | Medium | High | require an explicit target root; validate plugin root independently; document source versus target roots | host configuration can still intentionally select the wrong repository |
| Shell/command injection through MCP arguments or manifests | Medium | High | no arbitrary command tool; fixed/recognized argv; `shell=False`; no repository-local PATH shadowing; dry-run evidence | recognized project scripts are repository-owned code and may themselves be malicious |
| Timed-out process leaves descendants running | Medium | High | new process group/session; terminate the complete process tree; verify with a child-process regression | abrupt termination cannot guarantee application-level cleanup of project scripts |
| Credential-like material is returned or logged in full | Medium | High | scan only current additions, distinguish placeholders/test fixtures, redact every reported value, log counts only | format-based detection cannot prove whether a credential is live and cannot cover every format |
| Malformed or oversized graph/diff/source exhausts memory or CPU | Medium | High | byte/count/depth/fanout limits, temporary-file subprocess capture, explicit truncation, boundary tests | a valid graph near the 64 MiB limit still has non-trivial parse/NetworkX expansion cost |
| Regex or glob input causes pathological runtime | Low | Medium | bound pattern length/count; compile controlled glob grammar; avoid user-supplied regex | platform/path edge cases can still require manual review |
| Stale or undirected graph is presented as current directional fact | Medium | Medium | preserve `AVAILABLE_BUT_STALE`; lower confidence; expose direction as unknown; deterministic tools remain independent | four known zero-node JSON retries keep this repository stale until Graphify models them officially |
| Baseline is silently overwritten or bloated into a second graph | Low | High | MCP stays read-only; creation is an explicit CLI; compact schema/fingerprints/signatures; size limit and atomic replace | a user can intentionally accept a bad baseline; review remains required |
| Remediation trusts an agent assertion rather than current evidence | Medium | High | re-run supported detectors; compare normalized fingerprints; return manual/not-verifiable states for judgment or rotation | removed secrets remain compromised until external revocation/rotation is confirmed |
| Concurrent calls corrupt shared provider/cache state | Low | Medium | concurrent read tests; immutable result objects; add locking only if a race is reproduced | filesystem changes during concurrent calls may yield different honest snapshots |
| Logging or error handling exposes internals/secrets or corrupts stdio | Medium | High | diagnostics on stderr only; configured levels; log tool, duration, status, truncation, counts; controlled error codes | Python/runtime failures outside normalized service boundaries can still surface to the host |
| CI/install pulls mutable or undeclared tooling | Medium | High | locked dependencies, explicit plugin-validation dependency, pinned workflow actions, lock check and clean-install test | external registries and action infrastructure remain supply-chain dependencies |

## Defensive security-audit coverage

`audit_security` should automate only evidence that can be explained and tested with
low false-positive pressure:

1. credential/private-key formats and sensitive files introduced by the current change,
   always redacted and downgraded for explicit test fixtures/placeholders;
2. Python calls that explicitly enable a shell or invoke `os.system`;
3. newly added `eval`/`exec` calls;
4. explicit traversal constants at filesystem sinks and unsafe temporary-file APIs;
5. explicit TLS/security disabling and removal of recognizable authorization,
   validation, or repository-boundary controls.

Authentication-, authorization-, upload-, SSRF-, cookie-, session-, and CORS-sensitive
files may be listed as review surfaces, but filenames or words alone do not prove a
finding. Dynamic behavior, framework registration, external policy, and whether a
credential is live remain manual-review questions.

## Security acceptance tests

- positive, negative, placeholder, and test-fixture credential cases with redaction;
- `shell=True`, `os.system`, `eval`/`exec`, unsafe temporary file, path traversal, and
  security-weakening positive/negative fixtures;
- path, symlink/junction, Unicode, malformed graph, duplicate node, dangling edge,
  graph-size, fanout, and public-input limits;
- timeout with a spawned child, large stdout/stderr, missing executable, and controlled environment;
- concurrent graph reads, validation plus graph query, parallel impact analyses, and status plus architecture;
- logging assertions that credential-like values and file bodies never reach stderr.

Passing these tests demonstrates only the covered controls. It does not establish
that a target repository is secure, that every secret format is detected, or that
all platform-level process cleanup and filesystem races are impossible.
