# Unit analysis: `grill-me`

## Scope and conclusion

This analysis compares the `grill-me` unit with the plugin's five current skills.
The plugin was not changed.

The unit's most useful contribution is a dependency-oriented decision protocol:

1. discover everything verifiable in the repository;
2. separate facts from choices that belong to the user;
3. ask only about material decisions that remain open;
4. include a reasoned recommendation with every question;
5. continue working on independent branches;
6. stop when the required decisions have been resolved, safely assumed, or
   recorded as real blockers.

The plugin already applies much of steps 1 and 2 and contains strong evidence,
scope, and authorization gates. The main gap is making the decision tree,
dependencies among questions, origin of each answer, and stopping criterion
explicit. Importing an unlimited interview or turning all five skills into
interrogations is not recommended.

## Complete inventory

### Unit analyzed

| File | Role |
|---|---|
| external unit `grill-me/SKILL.md` | Activation metadata, usage examples, and interview-flow instructions |

This unit has no `agents/openai.yaml`, `references/`, `scripts/`, or `assets/`.

### Current plugin

#### `anti-ai-design`

| File | Observed role |
|---|---|
| `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md` | Scope, preparation, workflow, modes, and output contract |
| `plugins/anti-ai-craft/skills/anti-ai-design/agents/openai.yaml` | Name, short description, default prompt, and explicit invocation |
| `plugins/anti-ai-craft/skills/anti-ai-design/references/accessibility-baseline.md` | Normative baseline and manual accessibility matrix |
| `plugins/anti-ai-craft/skills/anti-ai-design/references/design-antipatterns.md` | Contextual signs, false positives, and critique questions |
| `plugins/anti-ai-craft/skills/anti-ai-design/references/design-principles.md` | Decision model, composition, components, language, content, and responsiveness |
| `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md` | Mandate, thesis, invariants, references, media, states, and production |
| `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md` | Preflight, passes, capture, comparison, human gate, and reporting |
| `plugins/anti-ai-craft/skills/anti-ai-design/references/sources.md` | Evidence hierarchy and application criteria |

#### `anti-ai-code`

| File | Observed role |
|---|---|
| `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md` | Scoped review and implementation, evidence, validation, and output |
| `plugins/anti-ai-craft/skills/anti-ai-code/agents/openai.yaml` | Name, short description, default prompt, and explicit invocation |
| `plugins/anti-ai-craft/skills/anti-ai-code/references/architecture-antipatterns.md` | Abstraction, fragmentation, compatibility, API, performance, and observability |
| `plugins/anti-ai-craft/skills/anti-ai-code/references/code-antipatterns.md` | Contracts, failures, state, concurrency, security, and implemented UI |
| `plugins/anti-ai-craft/skills/anti-ai-code/references/debugging-and-evidence.md` | Falsifiable hypotheses, change/evidence, oracles, and API verification |
| `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md` | Scope gates, system model, discovery, fix, validation, and reporting |
| `plugins/anti-ai-craft/skills/anti-ai-code/references/sources.md` | Evidence rules and application criteria |
| `plugins/anti-ai-craft/skills/anti-ai-code/references/testing-antipatterns.md` | Test sensitivity, mocks, waits, snapshots, and honest execution |

#### `anti-ai-audit`

| File | Observed role |
|---|---|
| `plugins/anti-ai-craft/skills/anti-ai-audit/SKILL.md` | Strictly read-only audit, baseline, coverage, and findings |
| `plugins/anti-ai-craft/skills/anti-ai-audit/agents/openai.yaml` | Name, short description, default prompt, and explicit invocation |
| `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md` | Coverage by evidence, area, and family |
| `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md` | Structure for findings, closure, coverage, validations, and next steps |
| `plugins/anti-ai-craft/skills/anti-ai-audit/references/severity-model.md` | Severity, confidence, priority, classification, and calibration |

#### `anti-ai-remediate`

| File | Observed role |
|---|---|
| `plugins/anti-ai-craft/skills/anti-ai-remediate/SKILL.md` | Eligibility, planning, application, verification, and output by ID |
| `plugins/anti-ai-craft/skills/anti-ai-remediate/agents/openai.yaml` | Name, short description, default prompt, and explicit invocation |
| `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md` | Permitted actions, new approval, interruption, and completion |
| `plugins/anti-ai-craft/skills/anti-ai-remediate/references/remediation-protocol.md` | Complete protocol and rollback |
| `plugins/anti-ai-craft/skills/anti-ai-remediate/references/validation-checklist.md` | General, data, UI, and handoff validation |

#### `anti-ai-security`

| File | Observed role |
|---|---|
| `plugins/anti-ai-craft/skills/anti-ai-security/SKILL.md` | Modes, threat model, discovery, validation, fix, and output |
| `plugins/anti-ai-craft/skills/anti-ai-security/agents/openai.yaml` | Name, short description, default prompt, and explicit invocation |
| `plugins/anti-ai-craft/skills/anti-ai-security/references/remediation-workflow.md` | Fixes by boundary, rate limiting, preservation, and validation |
| `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md` | Contextual controls and minimum tests by risk |
| `plugins/anti-ai-craft/skills/anti-ai-security/references/sources.md` | Evidence limits and control corpus |
| `plugins/anti-ai-craft/skills/anti-ai-security/references/validation-and-severity.md` | Recording, falsification, severity, deduplication, and the fix gate |

## Behavior of the analyzed unit

### Activation

The unit was designed for situations in which the user asks for an idea, plan, or
design to be challenged or stress-tested. Its focus is decision discovery, not
implementation, normative audit, or remediation.

### Observed flow

1. Receive an incomplete idea or plan.
2. Decompose the subject into related decisions.
3. Traverse branches in an order that respects dependencies.
4. Investigate the project when an answer exists in code, components, styles, or tokens.
5. Ask the user only when the existing material cannot resolve the decision.
6. Accompany every question with a recommendation.
7. Continue until the user and agent share sufficient understanding.

### Implicit decision tree

```text
pending decision
├─ is the answer verifiable in the project?
│  ├─ yes → investigate and record the evidence
│  └─ no
├─ does the answer depend on another decision?
│  ├─ yes → resolve the dependency first
│  └─ no
├─ does the decision materially change the product, risk, or direction?
│  ├─ yes → ask with a recommendation
│  └─ no → adopt a safe assumption and state it
└─ are there other independent branches?
   ├─ yes → continue while waiting for or recording the decision
   └─ no → stop or declare a precise blocker
```

The original unit contains the core principles of this tree but does not
formalize states, a ledger format, a verifiable stopping criterion, or blocker handling.

### Question types

| Type | Appropriate handling |
|---|---|
| Repository fact | Read files, history, components, configuration, tests, or runtime; do not ask |
| Existing convention | Locate precedents and real consumers; do not ask for an abstract preference |
| Low-risk ambiguity | Choose the most coherent default, state the assumption, and continue |
| Product or identity decision | Ask, presenting a recommendation, alternatives, and consequences |
| Material contract, security, or compatibility decision | Ask before a change that could break or expose the system |
| Authorization for an external or destructive effect | Block only the dependent action until explicit authorization |
| Unavailable external information | Record the gap and continue work that does not depend on it |

### Current output

The unit defines no structured final artifact. The expected outcome is shared
understanding reached during the conversation. It lacks fields for:

- resolved decisions;
- origin of the answer;
- dependencies among decisions;
- recommendation and alternative;
- adopted assumptions;
- branches still open;
- impact of leaving the question unresolved;
- next executable step;
- stopping condition.

### Current limits

The following are not explicit:

- maximum number of questions per round;
- difference between a necessary question and curiosity;
- permission to continue on independent branches;
- criterion for not repeating an answered question;
- interview scope boundary;
- handling conflict between the repository and the user's statement;
- difference between an objective recommendation and a preference;
- protection for read-only modes;
- authorization gates for editing, commits, pushes, or external actions.

## Comparison matrix

| Capability | State in the plugin | Current evidence | Decision |
|---|---|---|---|
| Investigate the repository before asking | **Already present** | All five `SKILL.md` files require reading relevant sources and state | Preserve |
| Examine components, styles, and tokens before requesting visual direction | **Already present** | `anti-ai-design` inventories and reads the design system, tokens, code, and assets | Preserve |
| Ask only when the answer materially changes the outcome | **Already present** | `anti-ai-design` limits material questions; `anti-ai-code` separates low- and high-risk ambiguity | Generalize with consistent language |
| Resolve dependencies among decisions before asking | **Partial** | Remediation gates and the threat model have ordering, but no tree or recorded dependencies | Incorporate |
| Provide a recommendation with every material question | **Absent** | Alternatives and tradeoffs exist, but no mandatory per-question contract | Incorporate with rationale |
| Record answer origin: project, user, requirement, or assumption | **Partial** | Fact, inference, and unknown are separated and sources are traceable | Add origin and confidence to the ledger |
| Continue independent branches without waiting for an answer | **Partial** | Audit requires complete coverage and code accepts low-risk assumptions, but behavior is not shared across all skills | Incorporate |
| Explicit interview stopping criterion | **Absent** | Completion gates exist per task, not for decision saturation | Incorporate |
| Avoid repeating an already resolved question | **Partial** | Current state is revalidated in remediation and security, but there is no uniform conversational record | Incorporate |
| Keep questions and decisions in the report | **Partial** | Audit separates pending decisions; other outputs cite approvals and limitations | Incorporate only for material decisions |
| Persistent, unlimited interview | **Do not incorporate** | Conflicts with autonomy, context economy, and the two- or three-question design limit | Replace with short, impact-oriented rounds |
| Ask about facts already in the project | **Do not incorporate** | Contradicts all five skills and repository instructions | Investigate directly |
| Activate implicitly when detecting a vague idea | **Do not incorporate** | All five skills preserve explicit invocation | Do not change policy |
| Create a sixth skill or rename the five existing skills | **Do not incorporate** | The value fits a cross-cutting protocol; a new skill would fragment the flow | Preserve names, paths, and compatibility |
| Require a user answer before any progress | **Do not incorporate** | Many branches can be verified or executed independently | Block only the dependent action |
| Recommend when evidence is insufficient | **Do not incorporate** | Conflicts with evidence, security, and anti-hallucination controls | Recommend only with stated basis and confidence |

## Improved protocol for nonblocking questions

### 1. Build the ledger before asking

Record only material decisions:

| Field | Content |
|---|---|
| ID | Stable decision identifier |
| Decision | What needs to be defined |
| Depends on | IDs that must be resolved first |
| Possible origin | Project, requirement, user, external environment, or assumption |
| Status | Resolved, assumed, open, blocking, not applicable, or superseded |
| Evidence | File, line, command, test, screen, or contract |
| Recommendation | Suggested option and reason |
| Consequence | What changes if another option is chosen |
| Next step | Work that can continue now |

Do not record trivial preferences or questions asked from curiosity.

### 2. Research in the least expensive, most reliable order

1. project instructions and the current request;
2. README, specification, and documentation;
3. configuration, manifests, and lockfiles;
4. code, components, tokens, and callers;
5. tests and fixtures;
6. Git history when it clarifies intent;
7. runtime or a read-only command;
8. official documentation for the exact version when necessary;
9. the user, only if the decision remains materially open.

### 3. Ask in a short round

Ask one question at a time when an answer changes the next question. Group no more
than two or three when they are independent and the user can answer them together.

Recommended format:

```text
Decision:
What I found:
My recommendation:
Alternatives and consequences:
Safe default if you have no preference:
What I can continue without this answer:
```

Do not present a preference as a technical recommendation. When evidence is
insufficient, state confidence and explain what is missing.

### 4. Do not block independent work

- continue reading, inventory, diagnosis, and validation that do not depend on the answer;
- during analysis, record the gap without interrupting all coverage;
- during implementation, pause only affected files or behaviors;
- during remediation, do not edit a blocked ID, but continue independent approved IDs;
- during security work, mark an external control as infrastructure-dependent and continue on other surfaces;
- never treat user silence as authorization for destructive, external, or materially incompatible action.

### 5. Stop at a verifiable condition

End the protocol when:

- every material decision is resolved, explicitly assumed, superseded, or classified as a blocker;
- no remaining question changes acceptance criteria, security, compatibility, identity, scope, or authorization;
- the next step can be executed and validated without inventing a requirement;
- the report clearly identifies any residual risk.

## Recommendations by file

### GRM-01 — Make the decision gate explicit in design

- **Priority:** P0
- **Exact current file:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Concrete instruction:** expand step 6 under “Prepare the work” to require a
  short ledger of material decisions, research the project first, order questions
  by dependency, include a recommendation and consequence, and continue
  independent branches. Keep the current maximum of two or three questions per round.
- **Reason:** design is the most direct application of the protocol and currently
  limits the number of questions, but not their structure or dependencies.
- **Risk:** increasing the preamble and making simple tasks bureaucratic.
- **Acceptance criterion:** in a project with defined tokens and components, the
  skill does not ask about palette or library; when faced with a real identity
  conflict, it asks no more than three questions, each with evidence,
  recommendation, impact, and a safe default.

### GRM-02 — Record closure of direction branches

- **Priority:** P1
- **Exact current file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Concrete instruction:** add to preflight an optional decision table with ID,
  dependency, origin, status, and evidence; in the report, require only decisions
  that change direction, product, or risk. Define closure as the point when no
  open branch changes the direction contract or acceptance criteria.
- **Reason:** the workflow already covers alternatives and a human gate, but does
  not show why one question preceded another or whether a branch remained open.
- **Risk:** duplicating the direction contract.
- **Acceptance criterion:** the ledger references the contract instead of
  repeating it and makes it possible to identify at a glance which decisions came
  from the project, user, or an assumption.

### GRM-03 — Separate technical discovery from contract choices

- **Priority:** P0
- **Exact current file:** `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md`
- **Concrete instruction:** after step 4 under “Prepare,” add this rule: verifiable
  facts must be investigated; ambiguities in contract, compatibility, behavior,
  or security become decisions with a recommendation, alternatives, and impact;
  low-risk ambiguities receive a stated assumption. Permit continued investigation
  and independent changes.
- **Reason:** the skill already distinguishes ambiguities but does not explain how
  to ask or how to prevent a localized uncertainty from pausing the entire task.
- **Risk:** the agent recommending an API or contract based on preference.
- **Acceptance criterion:** the recommendation cites local evidence or a
  requirement; without sufficient evidence, the skill presents the option as a
  hypothesis and does not edit the dependent path.

### GRM-04 — Order technical decisions by dependency

- **Priority:** P1
- **Exact current file:** `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
- **Concrete instruction:** under “Resolve scope,” record open decisions and their
  dependencies; resolve contract/invariant first, then boundary/API, and only then
  implementation. In the report, list open decisions that prevented evidence or change.
- **Reason:** prevents premature implementation questions when the real decision is still contractual.
- **Risk:** excessive formality for a localized fix.
- **Acceptance criterion:** no ledger is emitted for a simple unambiguous bug; for
  two interpretations of a requirement, the workflow resolves interpretation
  before discussing architecture.

### GRM-05 — Ask audit questions without interrupting coverage

- **Priority:** P0
- **Exact current file:** `plugins/anti-ai-craft/skills/anti-ai-audit/SKILL.md`
- **Concrete instruction:** add a rule that questions about product,
  infrastructure, or the baseline should include a recommended answer and effect
  on severity/confidence, but should not interrupt independent families. Only
  missing scope, an indeterminate target, or authorization required for external
  access may block the dependent portion.
- **Reason:** the skill already requires continuing after the first finding; the
  same principle should apply to open decisions.
- **Risk:** issuing a premature finding when the answer is missing.
- **Acceptance criterion:** an infrastructure-dependent candidate remains a gap
  while the audit completes other areas and does not promote it to a confirmed vulnerability.

### GRM-06 — Structure pending decisions in the audit report

- **Priority:** P1
- **Exact current file:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
- **Concrete instruction:** turn “Pending decisions and preferences” into a table
  with ID, question, origin researched, dependency, recommendation, alternatives,
  impact on the report, status, and work completed independently.
- **Reason:** the current template separates decisions but lacks enough
  traceability to resume the audit without repeating questions.
- **Risk:** confusing a pending decision with a finding.
- **Acceptance criterion:** decision IDs use a prefix distinct from findings and
  never enter severity counts.

### GRM-07 — Distinguish missing information from missing approval

- **Priority:** P0
- **Exact current file:** `plugins/anti-ai-craft/skills/anti-ai-remediate/SKILL.md`
- **Concrete instruction:** before requesting information, require a search of the
  report, current state, code, tests, and relevant history. If a material decision
  remains missing, ask with a recommendation, risk, and preserved behavior; block
  only dependent IDs and continue independent approved IDs.
- **Reason:** remediation requires sufficient input but can avoid redundant
  questions and blocking the entire batch.
- **Risk:** fixing IDs in an order that conflicts with the blocked ID.
- **Acceptance criterion:** the skill checks dependencies among IDs before
  proceeding; an independent ID can be validated and fixed while the blocked one
  retains explicit status and no related file is edited.

### GRM-08 — Classify questions at approval gates

- **Priority:** P1
- **Exact current file:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md`
- **Concrete instruction:** add three classes: discoverable in the target,
  assumable without changing the contract, and blocking because of
  authorization/product/risk. Require a recommendation only for decision classes;
  never treat a suggested default as implicit authorization.
- **Reason:** avoids conflating missing technical context with required consent.
- **Risk:** incorrect classification allowing a material change without approval.
- **Acceptance criterion:** commits, pushes, destructive changes, migrations, and
  broad changes remain blocked without specific authorization even when there is
  a recommendation.

### GRM-09 — Turn the threat model into a traceable decision tree

- **Priority:** P0
- **Exact current file:** `plugins/anti-ai-craft/skills/anti-ai-security/SKILL.md`
- **Concrete instruction:** in the threat model, connect decisions by dependency
  among asset, actor, boundary, input, control, impact, and environment. For an
  unverifiable external configuration or product threshold, ask with a recommended
  posture, basis, impact, and confidence; continue on independent surfaces.
- **Reason:** security already has the closest material to a tree, but does not
  record questions and recommendations as resumable decisions.
- **Risk:** presenting a conservative posture as a universal requirement.
- **Acceptance criterion:** the skill distinguishes normative requirements, local
  evidence, hardening, and product decisions; rate-limit values are not invented,
  and a gateway gap does not end the authorization or flow review.

### GRM-10 — Include dependency and recommended response in security records

- **Priority:** P1
- **Exact current file:** `plugins/anti-ai-craft/skills/anti-ai-security/references/validation-and-severity.md`
- **Concrete instruction:** add the fields “depends on,” “decision required,”
  “origin researched,” “recommended posture,” “effect if unanswered,” and
  “independent work completed” to the candidate record. Keep pending decisions
  outside confirmed vulnerabilities.
- **Reason:** improves resumption, falsification, and handoff without lowering the evidence standard.
- **Risk:** mixing a control hypothesis with a fix recommendation.
- **Acceptance criterion:** every external or product-dependent candidate clearly
  shows whether the question affects confirmation, severity, priority, or only hardening.

### GRM-11 — Preserve metadata and compatibility

- **Priority:** P0
- **Exact current files:** `plugins/anti-ai-craft/skills/anti-ai-design/agents/openai.yaml`, `plugins/anti-ai-craft/skills/anti-ai-code/agents/openai.yaml`, `plugins/anti-ai-craft/skills/anti-ai-audit/agents/openai.yaml`, `plugins/anti-ai-craft/skills/anti-ai-remediate/agents/openai.yaml`, and `plugins/anti-ai-craft/skills/anti-ai-security/agents/openai.yaml`
- **Concrete instruction:** do not change names, default prompts, or
  `allow_implicit_invocation` because of this unit. The protocol should live in
  the body and references of the existing skills.
- **Reason:** the improvement is operational and creates no new public capability;
  changing activation would increase collisions and break expectations.
- **Risk:** no functional risk if metadata remains consistent with the `SKILL.md` files.
- **Acceptance criterion:** all five names, display names, default prompts, and
  invocation policy remain identical after implementation.

## Skill-specific adaptation

| Skill | What to ask | What to discover in the repository | What may block |
|---|---|---|---|
| `anti-ai-design` | Identity, mandate, product priority, and a material visual tradeoff | components, tokens, assets, states, patterns, and responsive behavior | broad redesign, identity, navigation, or a product alternative |
| `anti-ai-code` | ambiguous contract, public compatibility, and expected behavior | installed APIs, callers, tests, invariants, conventions, and history | contract or security decisions that change the fix |
| `anti-ai-audit` | genuinely ambiguous target/baseline and necessary external evidence | scope, merge base, code, tests, runtime, and local controls | only the portion that cannot be audited safely or with evidence |
| `anti-ai-remediate` | approved IDs, product tradeoff, risk, and additional authority | current cause, reproduction, files, regressions, and dependencies among IDs | editing the dependent ID or taking action beyond authorization |
| `anti-ai-security` | business assets, impact, thresholds, and external controls not provided | boundaries, auth, queries, configuration, CI, tests, and attack paths | fixes, rotation, production, destructive tests, or confirmation that depends on infrastructure |

## Rules that should not be incorporated

1. Do not conduct an unlimited interview.
2. Do not ask again about something already answered by the project or user.
3. Do not turn a preference question into a technical blocker.
4. Do not create dozens of decisions for a simple task.
5. Do not offer a recommendation without evidence, premises, and confidence.
6. Do not use a default as consent to edit, publish, rotate, migrate, or destroy.
7. Do not change the read-only nature of audit.
8. Do not let the question protocol replace reproduction, tests, screenshots, traces, or validation.
9. Do not create a sixth skill, rename directories, or change triggers.
10. Do not copy external examples, phrases, or structure; preserve the plugin's vocabulary and architecture.

## Recommended implementation order

1. Apply GRM-01, GRM-03, GRM-05, GRM-07, and GRM-09 in the five `SKILL.md` files.
2. Apply GRM-02, GRM-04, GRM-06, GRM-08, and GRM-10 to the specific references.
3. Confirm GRM-11 and check that no metadata changed.
4. Validate all five skills.
5. Run scenario tests without revealing this report's conclusions to the executor:
   - the answer is already available in the repository;
   - two decisions have a dependency;
   - a low-risk decision can be assumed;
   - a material decision is genuinely blocking;
   - two independent branches, one blocked;
   - unavailable external configuration;
   - a requested action requires specific authorization.
6. Reject the revision if it contains a redundant question, unnecessary global
   blocker, baseless recommendation, or compatibility change.

## Final completeness criterion

Incorporation will be complete when all five skills:

- research before asking;
- ask only about a material decision that cannot be discovered;
- present a recommendation, basis, consequence, and safe default when applicable;
- record dependencies and answer origin;
- continue independent branches;
- have an explicit stopping condition;
- preserve evidence, scope, read-only mode, and authorization gates;
- retain their current names, paths, prompts, and explicit invocation.
