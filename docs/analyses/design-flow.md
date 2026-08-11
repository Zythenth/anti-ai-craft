# Analysis of the `design-flow` unit

## Scope and method

This analysis compares the external design flow with the plugin's five current
public skills. The objective is not to copy its wording, but to identify useful
mechanisms, gaps, and integrations—including whether to add an orchestrator—without
breaking published invocations, paths, or contracts.

The pass considered:

- the complete sequence proposed by the external unit;
- the inputs, outputs, states, gates, transitions, and implicit failures of that flow;
- direct and cross-cutting coverage by the five current skills;
- current authorization, evidence, accessibility, security, audit, and remediation controls;
- compatibility with the public names `$anti-ai-design`, `$anti-ai-code`,
  `$anti-ai-audit`, `$anti-ai-remediate`, and `$anti-ai-security`.

## Complete inventory of what was read

### External unit

- external unit `design-flow/SKILL.md`

### External cross-cutting files

- public documentation for the external unit
- security policy for the external unit
- manifest for the external unit
- marketplace entry for the external unit

### Current public packaging consulted for comparison

- `README.md`
- `plugins/anti-ai-craft/.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`

### `anti-ai-design`

- `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- `plugins/anti-ai-craft/skills/anti-ai-design/agents/openai.yaml`
- `plugins/anti-ai-craft/skills/anti-ai-design/references/accessibility-baseline.md`
- `plugins/anti-ai-craft/skills/anti-ai-design/references/design-antipatterns.md`
- `plugins/anti-ai-craft/skills/anti-ai-design/references/design-principles.md`
- `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- `plugins/anti-ai-craft/skills/anti-ai-design/references/sources.md`

### `anti-ai-code`

- `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md`
- `plugins/anti-ai-craft/skills/anti-ai-code/agents/openai.yaml`
- `plugins/anti-ai-craft/skills/anti-ai-code/references/architecture-antipatterns.md`
- `plugins/anti-ai-craft/skills/anti-ai-code/references/code-antipatterns.md`
- `plugins/anti-ai-craft/skills/anti-ai-code/references/debugging-and-evidence.md`
- `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
- `plugins/anti-ai-craft/skills/anti-ai-code/references/sources.md`
- `plugins/anti-ai-craft/skills/anti-ai-code/references/testing-antipatterns.md`

### `anti-ai-audit`

- `plugins/anti-ai-craft/skills/anti-ai-audit/SKILL.md`
- `plugins/anti-ai-craft/skills/anti-ai-audit/agents/openai.yaml`
- `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md`
- `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
- `plugins/anti-ai-craft/skills/anti-ai-audit/references/severity-model.md`

### `anti-ai-remediate`

- `plugins/anti-ai-craft/skills/anti-ai-remediate/SKILL.md`
- `plugins/anti-ai-craft/skills/anti-ai-remediate/agents/openai.yaml`
- `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md`
- `plugins/anti-ai-craft/skills/anti-ai-remediate/references/remediation-protocol.md`
- `plugins/anti-ai-craft/skills/anti-ai-remediate/references/validation-checklist.md`

### `anti-ai-security`

- `plugins/anti-ai-craft/skills/anti-ai-security/SKILL.md`
- `plugins/anti-ai-craft/skills/anti-ai-security/agents/openai.yaml`
- `plugins/anti-ai-craft/skills/anti-ai-security/references/remediation-workflow.md`
- `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`
- `plugins/anti-ai-craft/skills/anti-ai-security/references/sources.md`
- `plugins/anti-ai-craft/skills/anti-ai-security/references/validation-and-severity.md`

## Relevant cross-cutting implications

### Process

- The external set confirms that orchestration is distinct from the individual
  phases. This favors an explicit entry point for the complete journey rather
  than making every design invocation traverse all stages.
- Persistence by feature resolves collisions and supports resumption, but a fixed
  directory should not override existing project conventions. The real need is a
  stable identifier and artifacts that are not overwritten.
- Detection of the design system, tokens, themes, components, and dependencies
  before creating UI matches the current model and should remain central.
- Fixed-width “mobile first,” a mandatory dark theme, and automatic selection of
  a visual philosophy are prescriptive defaults. The current plugin correctly
  derives breakpoints from content, requires context for themes, and uses a
  dominant direction without a mandatory aesthetic catalog.
- A list of named styles may help exploratory discussion, but should not choose an
  identity for the user or replace product evidence.
- The external flow permits both individual phases and orchestrated use. The same
  separation should remain: an opt-in complete journey and independently usable
  specialized skills.

### Security

- Skills are instruction dependencies executed by local agents. Changes to them
  can expand reading, writing, execution, or external actions even without their
  own binary; diff review and release validation are supply-chain controls.
- Updates should not be trusted merely because they come from the default branch.
  The public package needs a verifiable version, an objective changelog, and
  review before updating a sensitive environment.
- Reports of behavior that could induce exfiltration, consent bypass, destructive
  action, or secret exposure need a private channel. The current repository has
  no `SECURITY.md`; a public issue is not an appropriate channel for an unpatched vulnerability.
- Security reports should request only minimum reproduction and never ask for a
  real secret. Sensitive material should be minimized, redacted, and kept out of
  public artifacts.
- Generic model limitations cannot be fixed by a skill. Project scope should be
  the behavior of instructions, packaging, and integrations it controls.
- Current protection through explicit invocation should remain. A good discovery
  description should not automatically activate a long or write-capable flow.

### Packaging

- The external set lists each unit separately in its manifest. The current package
  points to the skills directory, reducing duplication; if a new skill is created,
  discovery can continue through the directory, but the README, version,
  descriptions, and tests must reflect the sixth unit.
- Duplicated metadata in the manifest and marketplace can diverge. The current
  marketplace retains only discovery and policy while the manifest carries the
  package description; this separation is preferable.
- The current manifest and README say “five skills.” Creating
  `anti-ai-design-flow` would require updating both in the same change and
  validating that the package truly exposes six skills.
- The current repository has no license file. A license should not be copied from
  the external set; publication and reuse require the maintainer's own decision.
- Current updates are manual, which is safer than silently following the latest
  revision. For public releases, a tag or immutable reference improves
  reproducibility, but documentation should not promise pinning without testing
  the actual Codex flow.
- Creating an orchestrator requires no new app, MCP, hook, executable, or service.
  Any such capability would be a separate expansion of risk and scope.

## Model of the external unit

### Intent

The unit coordinates a design journey from initial clarification through
construction. It does not try to solve every discipline internally; it chains
specialized capabilities and uses their artifacts as memory across phases.

### Inputs

Explicit or assumed inputs:

- a request to start a product or feature from scratch;
- intent to traverse the complete process;
- project context;
- a decision about phases that may be skipped;
- the feature in focus;
- artifacts from previous phases, when they exist;
- the project stack, needed to materialize tokens;
- authorization to build;
- an executable application and visual evidence, needed for final review.

Material inputs not formalized:

- definition of done for each phase;
- which source of truth wins in a conflict;
- Git version or state to which each artifact refers;
- security and accessibility criteria before construction;
- policy for stale artifacts;
- behavior when a phase produces questions that invalidate an earlier phase.

### Sequence

The external flow is a linear state machine with controlled detours:

1. clarify decisions;
2. record intent;
3. organize information and navigation;
4. establish a visual language;
5. decompose construction;
6. implement in order;
7. review separately once a built product exists.

Phases 1 through 6 form the primary execution. Review is deliberately separate
and depends on something executable.

### Outputs

Expected outputs:

- shared understanding, without a file in the first phase;
- intent document;
- information-architecture document;
- tokens in the stack's format;
- ordered implementation checklist;
- built components and pages;
- review report;
- screenshots by viewport, theme, page, component, and state.

### Persistent state

State is inferred from the existence of files in a per-feature directory. The
essential elements are:

- short feature identifier;
- completed phases;
- artifacts present;
- open questions;
- next phase;
- marked tasks;
- existence of a reviewable build;
- whether review was requested;
- captured visual evidence.

This model allows a later return, but completion is inferred from file names.
There is no formal metadata distinguishing a file that is started, complete,
blocked, stale, or superseded.

### Gates

Useful gates:

- present the journey before starting;
- allow justified skips;
- state the expected output before each phase;
- complete one phase before the next;
- check whether an output changes the interpretation of the following phase;
- permit pausing and resumption;
- implement tasks in order;
- do not perform final review without something built;
- request feature selection when more than one exists.

Fragile or incomplete gates:

- human confirmation before every phase regardless of risk;
- human confirmation after every task regardless of impact;
- “file exists” as a substitute for a completion criterion;
- no explicit authorization gate before the first edit;
- no security gate before freezing the architecture;
- no freshness check between an artifact and code;
- no technical validation before marking a task complete;
- no handling of contradictions among the brief, architecture, tokens, and tasks.

### Transitions

Each phase should receive validated output from the previous one. Material transitions are:

- understanding → recorded intent;
- intent → structure and navigation;
- structure + identity → tokens;
- intent + structure + tokens → build plan;
- approved plan → implementation;
- verifiable implementation → independent review;
- review with findings → approved remediation.

The external flow mentions the need to observe effects from the previous phase,
but does not define how to invalidate, update, or version dependent outputs.

### Failures and recovery

Handled failures:

- user pauses: summarize the current position and next phase;
- multiple features: ask which one should be resumed;
- review without a build: defer it;
- no browser: use an available alternative or request manual evidence.

Failures not handled adequately:

- nonexistent or unavailable phase skill;
- incomplete or contradictory artifact;
- artifact stale relative to code;
- token incompatible with the stack;
- task marked done without a build, test, or execution;
- implementation diverges from the approved contract;
- architectural change invalidates the threat model;
- partial failure while writing an artifact;
- scope change during the flow;
- conflict with preexisting changes;
- missing real content or data;
- build passes but the real interface does not open;
- screenshot without a reproducible route, state, viewport, or theme.

## Coverage comparison

| Observed capability | State | Where it exists today | Assessment |
|---|---|---|---|
| Read the project before deciding | Already present | The five `SKILL.md` files | Current coverage is stronger because it includes instructions, code, configuration, history, and preexisting state. |
| Clarify material decisions | Already present | `anti-ai-design/SKILL.md`, `anti-ai-code/SKILL.md` | Already distinguishes material questions from low-risk assumptions. |
| Direction contract before code | Already present | `anti-ai-design/references/direction-contract.md` | More rigorous than a generic brief and includes mandate, invariants, media, states, and production. |
| Complete journey visible to the user | Partial | `anti-ai-design/SKILL.md` | There is an internal workflow, but no map of phases, current state, input, output, and definition of done. |
| Choice of phases that may be skipped | Partial | Modes and need-based loading | References are conditional, but there is no explicit gate for skipping a phase when sufficient evidence exists. |
| Persistent record of intent | Partial | Design output contract | Content is required, but path, state, and resumption are undefined. |
| Information architecture as a verifiable deliverable | Partial | Inventory of screens, routes, flows, and structure | Elements exist, but no artifact or minimum section preserves map, inputs, outputs, and navigation. |
| Stack tokens as a phase | Partial | `primitive → semantic → component` chain | The technical rule is strong, but there is no phase output, migration, state, or definition of done. |
| Ordered construction plan | Absent | — | No minimum task contract exists with dependencies, acceptance, and evidence. |
| Construction guided by approved tasks | Partial | Authorized implementation in design and code | Scope and minimum change exist, but there is no traceability from a design task to the diff. |
| Mark a task only after evidence | Partial | `change → evidence` cycle in code and remediation | Evidence exists but is not connected to persistent task state. |
| Pause and resume | Absent | — | No checkpoint records phase, artifacts, questions, blocker, and next input. |
| Multiple independent features | Absent | — | No selection or namespacing policy exists for design artifacts. |
| Review of a built product | Already present | `anti-ai-design/references/review-workflow.md` | Current coverage is more complete: runtime, viewports, states, two passes, and a human gate. |
| Review separate from implementation | Partial | Separate passes and `$anti-ai-audit` | Methodological separation exists, but the post-build handoff is not explicit. |
| Traceable screenshots | Partial | Visual workflow and audit report | Viewport, state, and theme are recorded, but there is no location convention or evidence index. |
| Review only with adequate evidence | Partial | Real capture required | A formal distinction among plan critique, prototype critique, and final runtime validation is still missing. |
| Accessibility in every phase | Already present | Accessibility baseline and workflows | Far more complete than the external unit. |
| Security before and after architectural decisions | Partial | `anti-ai-security/SKILL.md` | The threat model is strong but not connected to design-flow gates. |
| Read-only audit with IDs | Already present | `anti-ai-audit` | More robust than a visual-only review. |
| Remediation only for approved findings | Already present | `anti-ai-remediate` | Safer than fixing items directly from review. |
| Preservation of preexisting work and Git | Already present | Code, audit, and remediation | Missing from the external flow and well covered by the plugin. |
| Falsification and rejection of false positives | Already present | Audit, code, and security | Current coverage is stronger. |
| Artifact freshness relative to code | Absent | — | No skill requires linking a design artifact to the state it describes. |
| Invalidation of dependent outputs | Absent | — | A contract change does not mark architecture, tokens, or tasks as potentially stale. |
| Approval gate at every transition | Do not incorporate | — | Ritual confirmation at every phase or task creates friction and conflicts with risk-proportionate autonomy. |
| Dependency on multiple external skills with fixed names | Do not incorporate | — | Would create broken references and change the public five-skill model. |
| Mandatory fixed structure for all design work | Do not incorporate | — | Small components and local maintenance need no complete documentation directory. |
| Visual review restricted to the final build | Do not incorporate | — | Wireframes and screenshots may also be reviewed if not presented as runtime evidence. |
| Single token format | Do not incorporate | — | Output should follow the existing stack. |
| Specific browser as a requirement | Do not incorporate | — | Validation should use available capabilities and state limitations. |

## Decision: incorporate or create `anti-ai-design-flow`

### Option A — Incorporate everything into `$anti-ai-design`

Advantages:

- no new public name;
- no new skill directory;
- smaller documentation and packaging change;
- suitable if the flow remains limited to interface planning and execution in one task.

Disadvantages:

- mixes local creation/review with long-running orchestration;
- expands a skill that already covers research, planning, review, and implementation;
- makes the trigger ambiguous: “review a screen” and “guide a product from scratch
  through remediation” would share the same contract;
- makes it harder to coordinate security, code, audit, and remediation without
  making `$anti-ai-design` the owner of the other four skills;
- increases the risk of activating unnecessary phases, artifacts, or questions in small tasks.

### Option B — Create `$anti-ai-design-flow`

Advantages:

- makes the complete journey explicitly opt-in;
- preserves the focus and behavior of the five current skills;
- provides a dedicated place for state, transitions, resumption, and handoffs;
- can read and apply current contracts without duplicating their rules;
- allows the flow to evolve without changing routine use of `$anti-ai-design`.

Disadvantages:

- adds a sixth public skill;
- requires updating the README, version, manifest description, and packaging validation;
- may duplicate content if it rewrites the five skills instead of orchestrating them;
- requires clear rules against inheriting authorization, implicitly invoking
  edits, or turning every task into a workflow.

### Recommendation

**Create a new `$anti-ai-design-flow` without renaming or replacing any existing skill.**

The decisive reason is that the complete flow crosses design, security, code,
audit, and remediation, while `$anti-ai-design` should remain appropriate for a
screen, review, or scoped visual implementation. The new skill should contain
only the state machine and transition contracts; specialized rules remain in the
five current skills.

### Triggers for the new skill

Activate only through explicit invocation or an unambiguous request such as:

- guide the complete design flow;
- start a feature from scratch and continue through implementation and review;
- resume a persisted design flow;
- coordinate direction, structure, build, and validation for the same feature.

Do not activate for:

- screenshot review;
- local visual fix;
- creation of an isolated component;
- code review;
- broad audit;
- fixing IDs;
- isolated threat model.

The new skill's `agents/openai.yaml` should retain `allow_implicit_invocation: false`.

### Boundaries of the new skill

- Planning does not authorize editing.
- Authorization does not silently cross phases, skills, or external actions.
- The flow reads each required specialized contract; it does not summarize them into parallel versions.
- Skipping a phase requires an existing, current output, not merely a preference.
- A persistent checkpoint is required only in the complete flow.
- Human confirmation is reserved for material tradeoffs, scope changes, identity,
  navigation, risk, editing, or external action.
- Audit remains read-only.
- Security does not fix without authorization.
- Remediation remains dependent on approved IDs.
- Commits, pushes, deployments, secret rotation, and production changes remain
  outside the flow without specific authorization.
- The `.design/` directory may be a fallback, never an imposition over an existing convention.

### Necessity criterion

Create the new skill when the public product intends to support at least one of these situations:

- resumption in another task or session;
- three or more chained phases;
- coordination of two or more current skills;
- multiple features with separate artifacts;
- formal handoff from implementation to audit and remediation.

If the objective were only to add a short checklist before implementing an
interface in the same task, the new skill would be unnecessary; an internal
section in `$anti-ai-design` would suffice. For the analyzed flow, resumption and
coordination requirements satisfy the creation criterion.

### Planned files, not created in this analysis

- `plugins/anti-ai-craft/skills/anti-ai-design-flow/SKILL.md`
- `plugins/anti-ai-craft/skills/anti-ai-design-flow/agents/openai.yaml`
- a dedicated state/transitions reference only if `SKILL.md` becomes too large;
- updates to `README.md` and `plugins/anti-ai-craft/.codex-plugin/plugin.json`.

## Recommendations

Priorities:

- **P0:** fixes a contract, security, or traceability gap that could produce incorrect work.
- **P1:** improves continuity, verification, or integration without changing the skill's purpose.
- **P2:** improves operational clarity or handoff consistency.

### DF-01 — Route the complete flow to the orchestrator

- **Priority:** P0
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Concrete instruction:** retain current modes and add only one handoff: when a
  request is to guide a complete, resumable journey, direct explicit invocation of
  `$anti-ai-design-flow`; do not run the entire state machine inside `$anti-ai-design`.
- **Reason:** avoids duplicating orchestration and preserves the concise contract of the visual skill.
- **Risk:** creating a dependency on a skill not installed in older versions.
- **Acceptance criterion:** the handoff appears only when the new skill exists in
  the same package; previous installations continue operating with current modes.

### DF-02 — Formalize criteria for skipping phases

- **Priority:** P0
- **Planned file to create:** `plugins/anti-ai-craft/skills/anti-ai-design-flow/SKILL.md`
- **Concrete instruction:** define that a phase may be skipped only when its
  required output already exists, has an identified source of truth, and is
  current for the scope. Require a light read and validation of the existing
  artifact; “we already have tokens” is insufficient when components bypass them.
- **Reason:** avoids repeating work without accepting a nonexistent or decorative foundation as complete.
- **Risk:** the validation pass may become a full audit before any task begins.
- **Acceptance criterion:** the execution record states `execute`, `reuse`,
  `update`, or `not applicable` for each phase and the evidence supporting the decision.

### DF-03 — Create a resumable checkpoint in the direction contract

- **Priority:** P0
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Concrete instruction:** add an optional checkpoint section with feature
  identifier, scope, mandate, current phase, completed phases, artifacts,
  decisions, open questions, blocker, next required input, and the code state used
  as reference. Use explicit states such as `not started`, `in progress`,
  `blocked`, `complete`, and `superseded`.
- **Reason:** file existence proves neither completion nor that it still describes current code.
- **Risk:** generating administrative documentation for a small change.
- **Acceptance criterion:** the checkpoint is required only in complete-flow mode
  or when the user requests resumption; reopening work reveals the next phase without guesswork.

### DF-04 — Define invalidation across phases

- **Priority:** P0
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Concrete instruction:** declare dependencies among contract, structure,
  tokens, plan, and implementation. When an earlier decision changes, mark
  dependent outputs `revalidate` instead of silently updating them or treating them as complete.
- **Reason:** a navigation or identity change may invalidate tasks and tokens even when files remain present.
- **Risk:** a revalidation cascade larger than the real change.
- **Acceptance criterion:** every material change records affected artifacts and
  limits revalidation to real dependencies.

### DF-05 — Make information architecture a minimum output

- **Priority:** P1
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Concrete instruction:** when scope has more than one screen, route, or
  navigable state, add a structural section with entry points, destinations,
  tasks, relationships, navigation, no-access states, and recovery flow. Allow a
  separate file only when volume justifies it.
- **Reason:** the current inventory locates screens and routes but does not
  preserve the logic connecting structure to the task.
- **Risk:** duplicating existing route documentation.
- **Acceptance criterion:** output references the existing source of truth and
  documents only decisions or gaps not represented in code/configuration.

### DF-06 — Specify a definition of done for tokens

- **Priority:** P1
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-principles.md`
- **Concrete instruction:** augment the token section with a completion gate:
  stack-compatible format, defined semantic roles, identified real consumers,
  critical states covered, known loose values, scoped migration, and
  theme/contrast verification. Do not require a new file if the current system is already the source of truth.
- **Reason:** the existing technical chain is sound but does not state when the phase is ready to feed the build plan.
- **Risk:** turning refinement of one component into a complete token migration.
- **Acceptance criterion:** the gate states in-scope coverage and out-of-scope
  debt; it does not require eliminating every legacy value.

### DF-07 — Produce a verifiable build plan

- **Priority:** P0
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Concrete instruction:** when the user requests a build plan or the orchestrator
  routes that phase, require small units with an objective, dependencies, likely
  files or surfaces, preserved behavior, acceptance criterion, expected evidence,
  and risk. Do not begin editing if the plan depends on an open material decision.
- **Reason:** the primary gap between direction and implementation is the absence of traceable decomposition.
- **Risk:** predicting files before understanding the real architecture.
- **Acceptance criterion:** items may point to surfaces instead of files when not
  yet confirmed; no path is invented and every task has independent evidence.

### DF-08 — Consume the design plan in code

- **Priority:** P0
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md`
- **Concrete instruction:** when a change comes from a design flow, locate and read
  the approved contract, structure, tokens, and plan; map each change to the
  corresponding item and criterion. If current code contradicts the artifact,
  stop implementation of that item and record the divergence instead of silently choosing a side.
- **Reason:** closes the transition from visual decision to verifiable implementation.
- **Risk:** trusting a stale document.
- **Acceptance criterion:** the final report lists task → changed files → evidence;
  divergences were resolved or remain blocked.

### DF-09 — Do not complete a task merely because code was written

- **Priority:** P0
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
- **Concrete instruction:** add a flow-task gate: mark complete only after
  proportionate evidence, diff review, and confirmation that applicable design and
  behavioral criteria were exercised. An environment failure results in partial validation, not full completion.
- **Reason:** the external flow tracks tasks but defines no technical completion
  gate; the plugin already has the necessary controls.
- **Risk:** blocking progress because external validations are unavailable.
- **Acceptance criterion:** every task ends as `validated`, `partial validation`,
  `blocked`, `superseded`, or `failed`, with a command/evidence or limitation.

### DF-10 — Add a security gate before freezing structure

- **Priority:** P0
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-security/SKILL.md`
- **Concrete instruction:** add a planning-support mode that, when explicitly
  invoked during the flow, produces a minimum checkpoint for assets, data, actors,
  tenants, boundaries, expensive operations, destructive actions, and abuse stories
  before approving structure and tasks. Reuse the current complete model when risk requires it.
- **Reason:** authorization, isolation, privacy, and cost are architectural decisions, not finishes discovered after the build.
- **Risk:** turning every visual project into a broad security review.
- **Acceptance criterion:** the checkpoint uses only applicable categories and
  separates `resolved`, `pending decision`, `depends on infrastructure`, and `not applicable`.

### DF-11 — Propagate design changes to the threat model

- **Priority:** P0
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`
- **Concrete instruction:** include among threat-model update triggers any
  information-architecture change that creates a new entry point, role, action,
  state, integration, data exposure, or expensive operation. A purely aesthetic
  change should not trigger a broad review.
- **Reason:** the current model already requires updates for architectural changes;
  what is missing is explicit origin in product and flow decisions.
- **Risk:** false triggers for purely visual changes.
- **Acceptance criterion:** the checklist distinguishes cosmetic changes from
  changes to a surface, boundary, actor, asset, or cost.

### DF-12 — Create a final-review readiness gate

- **Priority:** P0
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Concrete instruction:** before presenting a review as final validation, require
  an executable target, known route or entry point, reproducible state/data,
  defined viewport/theme, and available prior criteria. If anything is missing,
  classify the pass as a plan, static, or prototype review and state what it does not prove.
- **Reason:** prevents an isolated screenshot or code inspection from being treated as runtime evidence.
- **Risk:** reducing the usefulness of early feedback.
- **Acceptance criterion:** early feedback remains allowed, but the report clearly
  identifies the evidence level and makes no runtime conclusion without execution.

### DF-13 — Validate the decision chain during review

- **Priority:** P1
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Concrete instruction:** add a consistency pass across the task, contract,
  structure, tokens, plan, and implementation. For each deviation, determine
  whether it is a defect, valid later decision, superseded artifact, or evidence gap.
- **Reason:** comparing only “before and after” does not detect drift among phases.
- **Risk:** reporting stale documentation as a product failure.
- **Acceptance criterion:** every divergence receives a disposition and the current
  source of truth is explicit.

### DF-14 — Make audits recognize flow artifacts

- **Priority:** P0
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-audit/SKILL.md`
- **Concrete instruction:** when design artifacts exist, treat them as candidate
  sources, verify authority and freshness, and build a requirement/decision →
  implementation → evidence matrix. Do not assume an artifact outranks code or
  that a present file is complete.
- **Reason:** audit is the best point for independent review between build and remediation.
- **Risk:** expanding the scope of nonvisual audits.
- **Acceptance criterion:** artifacts are read only when they intersect scope, and
  the report distinguishes implementation divergence, superseded documents, and ambiguity.

### DF-15 — Record flow coverage in the report

- **Priority:** P1
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
- **Concrete instruction:** add an optional section with feature, claimed phase,
  examined artifacts, each artifact's state, connection to code, and unverified flow areas.
- **Reason:** the current report records technical coverage but does not show
  whether the brief, structure, tokens, and tasks were actually compared.
- **Risk:** making the template larger for audits without design.
- **Acceptance criterion:** the section is omitted or marked not applicable when
  no design flow is in scope.

### DF-16 — Preserve review IDs in the remediation handoff

- **Priority:** P0
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-remediate/SKILL.md`
- **Concrete instruction:** accept visual-review findings that use the same ID
  contract as audit and require a connection to phase, artifact, viewport/state,
  and acceptance criterion. Do not update design artifacts automatically; do so
  only when within the approved ID or declared as a necessary consequence.
- **Reason:** connects review to fixes without turning open recommendations into automatic edits.
- **Risk:** duplicate IDs or mixing a visual preference with an approved defect.
- **Acceptance criterion:** each ID preserves classification, evidence, and status;
  preferences remain outside automatic remediation.

### DF-17 — Reconcile state after remediation

- **Priority:** P1
- **Exact current file to change:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/validation-checklist.md`
- **Concrete instruction:** when a design flow exists, verify that code, evidence,
  task status, and affected artifacts do not contradict one another. If updating
  documentation is unauthorized, record the pending work without editing.
- **Reason:** fixing code while leaving a task blocked or a contract incompatible harms resumption.
- **Risk:** expanding a small fix into broad documentation work.
- **Acceptance criterion:** only directly affected artifacts are considered;
  out-of-scope changes become an explicit pending item.

### DF-18 — Standardize pause and resumption handoffs

- **Priority:** P1
- **Planned file to create:** `plugins/anti-ai-craft/skills/anti-ai-design-flow/SKILL.md`
- **Concrete instruction:** when the user stops complete-flow mode, provide a short
  checkpoint with current phase, completed outputs, decisions, open questions,
  blockers, relevant files, and next safe action.
- **Reason:** allows continuation without rereading or reinterpreting the entire conversation history.
- **Risk:** the summary becoming another divergent source of truth.
- **Acceptance criterion:** the checkpoint points to current artifacts and does not
  duplicate their full content.

### DF-19 — Use material gates, not ritual confirmation

- **Priority:** P1
- **Planned file to create:** `plugins/anti-ai-craft/skills/anti-ai-design-flow/SKILL.md`
- **Concrete instruction:** request confirmation only for a material change in
  direction, identity, navigation, scope, edit authorization, or product tradeoff.
  Between phases with no pending decision, advance and report the checkpoint;
  between tasks, run planned evidence without ritual interruption.
- **Reason:** preserves human control where it matters without making a long flow impractical.
- **Risk:** advancing beyond user expectations in open-ended tasks.
- **Acceptance criterion:** every transition capable of external change continues
  to require applicable authorization; read-only or already authorized steps do
  not request repeated consent.

### DF-20 — Make handoffs among the five skills explicit

- **Priority:** P2
- **Planned file to create:** `plugins/anti-ai-craft/skills/anti-ai-design-flow/SKILL.md`
- **Concrete instruction:** at the end of each phase, emit an optional map of next
  modes: scoped implementation in `$anti-ai-code`, independent review in
  `$anti-ai-audit`, abuse assessment in `$anti-ai-security`, and fixes for approved
  IDs in `$anti-ai-remediate`. Do not automatically invoke skills with an
  explicit-activation policy.
- **Reason:** the set already has strong specialization, but the user needs to know which contract starts the next stage.
- **Risk:** implying all five skills are mandatory.
- **Acceptance criterion:** the handoff recommends only the applicable capability,
  states the required input, and respects explicit invocation.

### DF-21 — Publish the new skill without changing the five existing ones

- **Priority:** P0
- **Exact current file to change:** `plugins/anti-ai-craft/.codex-plugin/plugin.json`
- **Concrete instruction:** only in the same commit that creates
  `$anti-ai-design-flow`, increment the version, replace statements of “five” with
  “six,” and include the complete flow in the description and prompt examples.
  Keep `skills` pointing to the directory and validate actual discovery of the new folder.
- **Reason:** the current manifest would become factually incorrect even if directory discovery worked.
- **Risk:** announcing the skill before packaging it or breaking consumers by changing existing identifiers.
- **Acceptance criterion:** the five current invocations remain identical, the
  installed plugin lists the sixth, and the public version matches the content.

### DF-22 — Update public selection documentation

- **Priority:** P0
- **Exact current file to change:** `README.md`
- **Concrete instruction:** add `$anti-ai-design-flow` to offering and selection
  tables, explain that it is opt-in for complete/resumable journeys, and retain
  `$anti-ai-design` for scoped visual work. Update the count, examples, and
  repository structure in the same change.
- **Reason:** prevents users from invoking the orchestrator for small tasks or not knowing it exists.
- **Risk:** documentation promising a flow not yet validated.
- **Acceptance criterion:** each of the six skills has a distinct use boundary and
  examples use identifiers that can actually be installed.

### DF-23 — Define private vulnerability disclosure

- **Priority:** P0
- **Planned file to create:** `SECURITY.md`
- **Concrete instruction:** publish a short policy defining supported versions,
  in-scope instruction and packaging behavior, a private channel, minimum
  reproduction information, and a prohibition on sending real secrets. Do not
  copy the external set's license, identity, or contacts.
- **Reason:** the current public repository invites contributions but does not
  separate an unpatched vulnerability from an ordinary issue.
- **Risk:** offering an unmonitored channel or promising an unrealistic response time.
- **Acceptance criterion:** an operational private channel exists, the text does
  not request sensitive data, and no unsupported promise is made.

### DF-24 — Add a release gate for skills

- **Priority:** P1
- **Exact current file to change:** `README.md`
- **Concrete instruction:** in the contribution or maintenance section, require
  validation of skills and the manifest, diff review for new capabilities,
  confirmation that no invocation policy changed silently, and installation/listing
  tests before publishing a version.
- **Reason:** a skill is an instruction dependency; a textual diff can change
  permissions and behavior with impact similar to code.
- **Risk:** documenting commands that do not exist or were not tested.
- **Acceptance criterion:** documentation records only executable commands in the
  current environment and separates required validation from optional steps.

### DF-25 — Do not follow a mutable update without transparency

- **Priority:** P1
- **Exact current file to change:** `README.md`
- **Concrete instruction:** explain that a marketplace update loads a new plugin
  revision and recommend reviewing notes/diffs in sensitive environments. If
  immutable references are documented, test installation by tag first; do not
  claim reproducibility merely from using the default branch.
- **Reason:** the current public flow teaches updating but does not explain the
  trust change between versions.
- **Risk:** complicating common installation or promising tag support without evidence.
- **Acceptance criterion:** the simple path remains available, and the
  higher-assurance path appears only if validated.

## Recommended integration among the five skills

### Primary flow

1. **`$anti-ai-design`** organizes discovery, contract, structure, visual system,
   and plan. It may implement only when authorized, but should produce criteria
   consumable by code and review.
2. **`$anti-ai-security`** enters as an explicit gate when structure or a task
   affects data, identity, tenants, destructive operations, integrations, cost, or
   a public surface. Its output is a risk checkpoint or findings with IDs, not a parallel aesthetic.
3. **`$anti-ai-code`** implements scoped items, reads current decisions, preserves
   architecture, and completes a task only after appropriate evidence.
4. **`$anti-ai-audit`** reviews independently and read-only. Within scope it
   compares the contract, structure, tokens, plan, code, and runtime, closes false
   positives, and issues supported IDs.
5. **`$anti-ai-remediate`** receives only approved IDs, revalidates current state,
   fixes one cause at a time, and keeps evidence and status consistent.

### Handoff contracts

| Origin | Destination | Minimum destination input | Expected output |
|---|---|---|---|
| Design | Security | assets, actors, data, boundaries, actions, and proposed architecture | risk decisions, gaps, or confirmed IDs |
| Design | Code | current contract, structure, applicable tokens, tasks, and criteria | scoped diff and evidence per task |
| Code | Design | executable implementation, states, routes, and limitations | visual/technical review with evidence |
| Design/Code/Security | Audit | scope, sources of truth, and comparable state | findings with IDs, dispositions, and coverage |
| Audit/Security | Remediation | approved IDs, evidence, scope, and acceptance | status and evidence per ID |
| Remediation | Audit or Design | diff, commands, screenshots, and residual risk | independent recheck when requested |

### Integration rules

- One skill must not claim another was executed without invocation and evidence.
- Artifacts are verifiable inputs, not automatic authority.
- The feature name should be stable within the flow, but storage need not follow a
  mandatory directory when the project already has its own convention.
- A contract change may require revalidation; it does not authorize rewriting every phase.
- Approval to plan is not approval to edit.
- Approval to implement is not approval to commit, push, deploy, or change production.
- Design review may produce a recommendation; only a supported, approved finding enters remediation.
- A security finding must not be reduced to a visual adjustment.
- A visual task that changes behavior must meet both design and code criteria.

## Pitfalls

### Turning sequence into bureaucracy

A long journey can produce worthless files, repeated questions, and checkpoints
that age quickly. The complete flow should be opt-in and proportional to scope.

### Confusing files with progress

A present file may be empty, partially complete, blocked, or superseded. State and
completion criteria need to be explicit.

### Treating linearity as truth

Real design is iterative. A content, security, or implementation discovery may
require revisiting an earlier decision. The return should invalidate only affected dependencies.

### Hiding authorization inside the flow

“Continuing” a planning phase grants no permission to edit, install, create a
dependency, take external action, commit, or push.

### Making documentation compete with the repository

Routes, tokens, and components that already have a source of truth should not be
duplicated in full. An artifact should record the decision, gap, and connection.

### Planning invented files

The build plan should not assert paths, APIs, or components before reading the
architecture. When still uncertain, it should identify the surface and decision to locate.

### Using review as automatic approval

A visual pass proves neither runtime, accessibility, security, performance, nor
integration. Evidence levels should remain separate.

### Fixing during audit

The flow cannot weaken the read-only contract of `$anti-ai-audit`. Review produces
IDs; remediation applies only approved ones.

### Turning preference into a defect

Direction, composition, and aesthetics remain product-dependent. The existence of
a review stage does not change the current taxonomy.

### Treating tokens as complete without consumers

A table of variables without connected real components, states, and themes does
not constitute a complete visual system.

### Deferring security until the end

Authorization, isolation, cost, and privacy may change information architecture
and tasks. Discovering them only after the build makes fixes more expensive and fragile.

### Updating everything after any change

Traceability does not mean rewriting the entire set. Only artifacts dependent on
the changed decision should be revalidated.

## Rules that should be rejected

- Do not rename the new skill to generic `design-flow` or make it replace
  `$anti-ai-design`; the recommended name is `$anti-ai-design-flow`.
- Do not create the sixth skill if the product abandons resumption, multiple
  phases, or coordination among skills; in that case, keep only a short checklist
  in `$anti-ai-design`.
- Do not rename any of the five existing skills.
- Do not change public triggers or permit implicit invocation as a side effect.
- Do not require a fixed document collection for a component, localized fix, or small review.
- Do not require human confirmation before every phase or after every task.
- Do not use the number of phases as a measure of quality.
- Do not consider a phase complete merely because a file was created.
- Do not mark a task complete merely because an edit occurred.
- Do not depend on names of external skills that do not exist in the plugin.
- Do not require a specific browser tool.
- Do not limit review to screenshots or code; declare the evidence type.
- Do not present static review as runtime validation.
- Do not create parallel tokens when the project already has a source of truth.
- Do not impose CSS, Tailwind, a theme, or any universal format.
- Do not create a design directory when the project convention defines another location.
- Do not overwrite another feature's artifact by reusing a generic name.
- Do not automatically update a superseded artifact without confirming the source of truth.
- Do not skip security because a feature “is only frontend” when it changes data,
  roles, flows, cost, or a boundary.
- Do not move fixes into `$anti-ai-audit`; preserve its strictly read-only mode.
- Do not let `$anti-ai-remediate` fix unapproved recommendations.
- Do not promote a visual preference to a vulnerability or defect ID.
- Do not inherit authorization from one phase for a commit, push, deployment, or production change.

## Suggested incorporation order

1. Implement DF-01, DF-02, DF-03, and DF-04 to create the flow and resumption contract.
2. Implement DF-07, DF-08, and DF-09 to close the planning → code → evidence connection.
3. Implement DF-10 and DF-11 to address security decisions early.
4. Implement DF-12, DF-13, DF-14, and DF-15 to make validation independent and traceable.
5. Implement DF-16 and DF-17 to preserve the remediation contract.
6. Implement DF-05, DF-06, DF-18, DF-19, and DF-20 as operational refinements.
7. Implement DF-21 and DF-22 in the same commit as the new skill; add DF-23
   before promoting the repository for sensitive use.
8. Apply DF-24 and DF-25 only with already verified release and update commands.

## Conclusion

The external unit's strongest contribution is a journey model with chained
artifacts, pausing, resumption, and post-build review. The five current skills are
already stronger in evidence, authorization, falsification, accessibility,
security, and remediation, so they should not be replaced by a rigid sequence.

Given authorization to create new skills and the requirement for cross-cutting
resumption, the correct improvement is to add `$anti-ai-design-flow` as an
explicit orchestrator. It should connect outputs to the existing contracts of the
five skills and contain only state, transitions, definition of done, invalidation,
and handoffs. This preserves all current public names and compatibility, reduces
ritual work, and adds traceability where the main gap currently exists.
