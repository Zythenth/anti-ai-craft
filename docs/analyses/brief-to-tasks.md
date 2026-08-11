# Analysis of the brief-to-tasks decomposition unit

## Executive summary

The external unit offers a useful idea that remains incomplete in the plugin:
turn a brief into an executable sequence of vertical deliverables, each with an
observable outcome. The plugin is already strong in reading context, preserving
scope, defining measurable criteria, validating through evidence, representing
interface states, using sensitive tests, and maintaining remediation gates. The
main gap is not a need to “plan more,” but to connect these capabilities to an
explicit task format with dependencies, evidence of completion, and persistent
state.

The recommended incorporation does not create a sixth skill, rename the five
existing skills, or impose a fixed directory path. The behavior should be
distributed:

- `$anti-ai-design` turns a brief and interface inventory into product slices;
- `$anti-ai-code` turns requirements and invariants into small changes with their own evidence;
- `$anti-ai-audit` produces a coverage map and suggested remediation order without editing;
- `$anti-ai-remediate` turns approved IDs into safe batches while preserving gates;
- `$anti-ai-security` adds dependencies and adversarial criteria to affected slices.

The expected gain is a smaller, executable, auditable plan. The main risk is
producing long lists that look precise but do not correspond to the repository or
demonstrate completion. Every proposed task must therefore include evidence of
its origin, a verifiable outcome, and a stopping criterion.

## Inventory examined

### External unit

| Item | Count | Content observed |
|---|---:|---|
| Primary skill file | 1 | Brief discovery, frontend inspection, component classification, decomposition, ordering, and checklist storage |
| Additional references | 0 | No separate material for security, code, acceptance criteria, or persistence |
| Agent configuration | 0 | No interface-specific metadata |
| Scripts, templates, or assets | 0 | The output model is embedded in the primary file |

### Current plugin

| Skill | Primary file | References | Agent configuration | Capabilities most relevant to this analysis |
|---|---:|---:|---:|---|
| `anti-ai-design` | 1 | 6 | 1 | brief, inventory, direction contract, states, responsiveness, accessibility, visual evidence |
| `anti-ai-code` | 1 | 6 | 1 | scope, invariants, minimum change, regression, change–evidence cycle, architecture, and tests |
| `anti-ai-audit` | 1 | 3 | 1 | coverage, candidate ledger, severity, acceptance criteria, and read-only reporting |
| `anti-ai-remediate` | 1 | 3 | 1 | eligibility, plan, application, frozen verification, rollback, and per-finding status |
| `anti-ai-security` | 1 | 4 | 1 | threat model, surfaces, controls, abuse, positive/negative tests, and residual risk |

Thirty-two plugin files were examined in full: five primary files, 22 references,
and five agent configurations. The comparison considers the complete set, not
only the primary files.

## What the external unit actually adds

### 1. Outcome-oriented decomposition

Its central contribution is requiring a task to produce something that can be
built and checked as a unit. This avoids artificially separating markup, styling,
and interaction that belong to the same behavior. The plugin already prescribes
small, verifiable changes, but does not yet clearly define the anatomy of an
implementation task.

A useful slice should cross only the layers required to deliver an observable
behavior. It may include UI, domain, persistence, and tests when all are required
for the same outcome. “Vertical” does not mean touching every layer or creating a
complete architecture; it means not declaring a fragment complete when it still
produces neither value nor evidence.

### 2. Explicit dependencies

The external unit recognizes dependencies but mixes three ordering criteria
without resolving conflicts: foundation, visual prominence, and risk. The
improved version should record hard dependencies, preferred ordering, and
opportunities for parallel work. Final order should follow the critical path and
the cost of discovering an incorrect hypothesis late.

### 3. Inventory before creation

It appropriately requires inspection of components, pages, tokens, conventions,
tests, and dependencies before tasks are created. The plugin already reads nearly
all these sources but does not consolidate them into an operational
classification:

- reuse unchanged;
- modify;
- create;
- out of scope;
- unknown until evidence is obtained.

This classification reduces duplicate tasks and prevents the plan from inventing
components or infrastructure.

### 4. Definition of done per task

The external unit requires visual verifiability but does not define a robust
standard of evidence. The plugin already has the necessary foundation:
reproduction, an independent oracle, sensitive tests, real execution, equivalent
screenshots, accessible validation, and a record of limitations. What is missing
is a concise per-task contract that brings these together.

### 5. Plan persistence

Saving the plan helps continuity, handoffs, and resumption, but a fixed path and
automatic write conflict with read-only modes and each repository's architecture.
Persistence should be optional, authorized, and adapted to local conventions. If
there is no authorization, the plan should remain only in the response.

## Recommended decomposition model

### Minimum input

Before creating tasks, gather:

1. the objective and expected outcome;
2. sources of truth that were actually read;
3. the current state demonstrated in the repository or product;
4. included and excluded scope;
5. affected users, flows, data, states, and invariants;
6. material risks, pending decisions, and limitations;
7. official commands and available means of validation.

When multiple briefs, features, or targets are plausible, do not silently choose
the most recent file. Selection must come from an explicit reference, an
unambiguous project convention, or user confirmation.

### Anatomy of a task

Each implementation task should contain only fields that guide execution and
evidence:

| Field | Content |
|---|---|
| Outcome | Observable behavior or capability delivered |
| Origin evidence | Requirement, finding, screen, flow, file, or decision that justifies the task |
| Scope | Likely files, components, boundaries, or areas, without pretending to know details before investigation |
| Strategy | Reuse, modify, or create; preserve relevant contracts |
| Dependencies | Real blockers, pending decisions, and tasks that can proceed in parallel |
| States and risks | Applicable failure cases, edge cases, accessibility, and security |
| Definition of done | Observable and measurable conditions |
| Validation | Command, scenario, screenshot, or inspection that proves each condition |
| Status | Pending, in progress, blocked, validated, partial validation, or rejected |

Do not require fictional time estimates, an advance list of every file, or
implementation details that can be known only while performing the task.

### Vertical slices

A good slice:

- delivers a recognizable flow, state, or control;
- reuses the existing architecture;
- includes the tests and validations specific to that outcome;
- can fail or be reversed without invalidating the entire plan;
- makes explicit what it still does not deliver;
- avoids artificial dependencies on isolated “structure,” “CSS,” “tests,” or
  “documentation” tasks.

A horizontal task is acceptable only when it produces a necessary, independently
verifiable outcome, such as a compatible migration, a semantic token that is
actually consumed, a tested API contract, or indispensable test infrastructure.
“Prepare the structure” without an immediate consumer should not be included.

### Ordering

Apply this decision sequence:

1. respect hard dependencies;
2. address the hypothesis with the greatest risk or irreversibility early;
3. deliver a representative slice early to validate direction, architecture, or contract;
4. group tasks that share a cause without hiding their independent criteria;
5. leave isolated polish until after the primary behavior;
6. indicate parallelism only when there is no contention over the same contract,
   critical file, or decision.

Foundation work does not receive automatic priority. Tokens, shells,
abstractions, and infrastructure come early only when an immediate slice proves
their use.

### Definition of done

A task is done only when:

- the described outcome exists on the real path;
- applicable states and boundaries have been exercised;
- the evidence was executed after the last relevant change;
- legitimate use still works;
- the diff is limited to the outcome;
- limitations and residual risk were recorded;
- any persistent documentation reflects the observed state, not future intent.

For UI, include viewport and state; for code, reproduction and regression; for an
audit, coverage and disposition; for security, negative and positive tests; for
remediation, per-ID status and frozen verification.

## Comparison matrix

| Capability | State in the plugin | Where it appears today | Decision |
|---|---|---|---|
| Read the brief and sources of truth before planning | Already present | Design, code, audit, and security | Keep |
| Inspect components, routes, tokens, tests, and dependencies | Already present | Design and code | Keep and condense into an operational inventory |
| Classify each element as reuse, modify, create, or out of scope | Partial | Preservation and inventory exist, without mandatory classification | Incorporate |
| Create tasks as complete vertical outcomes | Partial | Minimum change and behavior/states exist, but there is no task contract | Incorporate |
| Link a task to a requirement, finding, or evidence | Partial | Audit and remediation are strong; design/code planning is less explicit | Incorporate |
| Declare hard dependencies, preferred ordering, and safe parallelism | Absent | Cause/dependency ordering exists, without a common model | Incorporate |
| Order by critical path and risk of late discovery | Partial | Security and remediation prioritize risk; design prioritizes direction | Incorporate |
| Validate a representative slice early | Partial | The direction contract and focused tests already support this | Make explicit |
| Define done criteria and evidence per task | Partial | Global and per-finding criteria exist, not generic per-task criteria | Incorporate |
| Persist plan state for resumption | Absent | Reports record state, but not a delivery plan | Incorporate as optional |
| Update the plan from evidence and scope changes | Partial | Security updates the threat model; remediation requires a new gate | Generalize |
| Automatically create a task file | Absent | Planning modes may be read-only | Do not incorporate by default |
| Use a fixed path and name for the plan file | Absent | The plugin respects local conventions | Do not incorporate |
| Automatically choose the latest brief | Absent | The plugin asks when a decision is material | Do not incorporate |
| Assume a particular frontend structure | Absent | The plugin is portable across stacks | Do not incorporate |
| Require every task to fit into one session | Absent | Small changes are required without a fixed time unit | Do not incorporate as an absolute rule |
| Require a flat list with universal depth | Absent | Format varies by task | Do not incorporate as an absolute rule |
| Create fixed foundation, UI, state, and polish phases | Partial | The areas exist, but not as a mandatory sequence | Do not incorporate as a universal template |
| End with a differently named review command or skill | Absent | Audit and validation already cover the handoff | Do not incorporate; preserve current names |

## Recommendations by priority

### P0 — Define a common contract for verifiable tasks

- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
- **Concrete instruction:** add a short planning section that requires outcome,
  origin, scope, reuse/modify/create strategy, dependencies, definition of done,
  and validation. Specify that a task is created only when tied to an observable
  requirement, finding, or risk.
- **Reason:** provides a common language without creating a new skill or
  duplicating workflows.
- **Risk:** turning every small fix into bureaucracy.
- **Acceptance criterion:** in an implementation request, every planned task
  identifies an observable outcome and its evidence; inapplicable fields are
  omitted, and there are no infrastructure tasks without a consumer.

### P0 — Make vertical slices explicit in design planning

- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Concrete instruction:** in planning mode, require deliverables to combine
  structure, content, behavior, states, and validation only as needed for the same
  flow. Prohibit automatic decomposition by technology or discipline.
- **Reason:** prevents “write HTML, then CSS, then interaction” plans that delay
  real validation.
- **Risk:** producing tasks that are too large.
- **Acceptance criterion:** each slice can be demonstrated independently; when it
  exceeds one coherent flow, it is split by user outcome, not technical layer.

### P0 — Add operational classification to the inventory

- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Concrete instruction:** after inventorying screens, routes, components, tokens,
  media, and states, classify relevant items as direct reuse, necessary change,
  creation, out of scope, or unknown. Require evidence for the classification.
- **Reason:** avoids creating a task for something that already exists and exposes
  gaps before implementation.
- **Risk:** creating an excessive inventory of the entire repository.
- **Acceptance criterion:** only elements reachable from the scope are classified,
  and each task references at least one item to be changed or created.

### P0 — Preserve remediation gates within every plan

- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/remediation-protocol.md`
- **Concrete instruction:** represent each remediation batch as one or more slices
  tied to approved IDs, preserving eligibility, a no-edit plan, application, and
  frozen verification. Prohibit treating a task list as new authorization.
- **Reason:** a generic planner cannot weaken approval, scope, or reproduction.
- **Risk:** grouping different findings for convenience.
- **Acceptance criterion:** every batch shows IDs, a shared cause when one exists,
  dependencies, independent validation, and final status per ID.

### P0 — Include security in the definition of done, not as a final phase

- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-security/SKILL.md`
- **Concrete instruction:** when a slice changes a boundary, identity, tenant,
  persistence, external input, cost, or protected operation, attach the expected
  control, an adversarial scenario, and a legitimate scenario during planning.
  Update the threat model when execution reveals a material change.
- **Reason:** avoids a late, generic “review security” task.
- **Risk:** applying a security checklist to tasks with no relevant surface.
- **Acceptance criterion:** only slices with applicable risk receive security
  requirements, and completion includes a negative test, positive test, and
  residual risk.

### P1 — Record dependencies with useful semantics

- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
- **Concrete instruction:** distinguish hard blockers, preferred ordering, and safe
  parallelism. Order by critical path, risk of late discovery, and the value of a
  representative first slice.
- **Reason:** “dependencies first” is insufficient when foundation, risk, and
  visual feedback compete.
- **Risk:** simulating precision without knowing the implementation.
- **Acceptance criterion:** every dependency states what must be true; items
  without a causal relationship are not marked as blockers.

### P1 — Turn audit next steps into provable batches

- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
- **Concrete instruction:** expand “Next steps” with an optional table containing
  IDs, batch outcome, dependencies, risk, acceptance criterion, and proposed
  validation, without changing the read-only nature of the audit.
- **Reason:** eases the handoff to remediation without fixing or preapproving findings.
- **Risk:** the report may suggest a single implementation when product decisions remain.
- **Acceptance criterion:** the table separates recommended order from authorization
  and marks alternatives or pending decisions.

### P1 — Make evidence part of task state

- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/validation-checklist.md`
- **Concrete instruction:** require a task to move from “implemented” to “validated”
  only when its evidence has been rerun after the last relevant change. Provide
  separate states for blocked and partial validation.
- **Reason:** prevents checklists from being marked merely because code was written.
- **Risk:** duplicating the existing per-ID status.
- **Acceptance criterion:** task status derives from ID and evidence status without
  creating a conflicting second source of truth.

### P1 — Plan accessibility per slice

- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/accessibility-baseline.md`
- **Concrete instruction:** add guidance to attach to each interactive slice only
  the accessibility checks corresponding to widgets and states it introduces or
  changes; retain an integrated final pass.
- **Reason:** reduces the chance that accessibility becomes later polish.
- **Risk:** omitting cross-cutting requirements when only isolated components are validated.
- **Acceptance criterion:** each slice covers its keyboard behavior, focus,
  semantics, and messages, and the complete flow still receives integrated validation.

### P1 — Prohibit horizontal completion without a consumer

- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-code/references/architecture-antipatterns.md`
- **Concrete instruction:** record as a sign of fragile planning any abstraction,
  token, configuration, structure, or documentation task declared complete
  without a consumer or demonstrated behavior in the same increment or the
  immediately dependent one.
- **Reason:** extends the removal test to planning.
- **Risk:** blocking legitimate foundation work such as a migration or shared contract.
- **Acceptance criterion:** exceptions identify a known consumer, real dependency,
  and their own evidence.

### P2 — Persist plans without imposing a universal file

- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md` and `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md`
- **Concrete instruction:** allow a plan to be saved only when the user requests it
  or a project convention authorizes writing. Use the path already adopted by the
  repository; if no convention exists, confirm the destination. In read-only
  mode, deliver the plan in the response.
- **Reason:** enables resumption without violating authorization or polluting projects.
- **Risk:** creating a redundant document that diverges from an issue tracker or SDD.
- **Acceptance criterion:** the plan's location and authority are explicit; there
  is no automatic write or assumed path.

### P2 — Define plan updates and closure

- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
- **Concrete instruction:** when new evidence appears, update dependencies,
  criteria, or status; do not silently rewrite already validated tasks. Record a
  split, replacement, block, or rejection with its reason. At the end, reconcile
  the plan, diff, and validations.
- **Reason:** a static checklist loses value as soon as implementation discovers
  something new.
- **Risk:** verbose history.
- **Acceptance criterion:** material plan changes have a short reason; obsolete
  items do not remain marked complete.

### P2 — Adjust interface prompts without renaming skills

- **Target file:** `plugins/anti-ai-craft/skills/*/agents/openai.yaml`
- **Concrete instruction:** only after internal workflows are updated, mention in
  existing prompts the creation of a verifiable plan when a request includes
  planning. Preserve `name`, invocation names, and explicit-call policy.
- **Reason:** improves discovery of the new behavior without breaking compatibility.
- **Risk:** short prompts may become generic or imply automatic editing.
- **Acceptance criterion:** each prompt continues to state the skill's mode and
  limits; no new invocation is created.

## Persistence and continuity

A persisted plan should be a projection of the work, not a second specification.
To avoid divergence:

- record the source of truth for each task;
- use stable IDs only when they already exist in a requirement or finding;
- do not copy extensive requirements into the plan;
- update status only after evidence;
- keep pending decisions separate from executable tasks;
- record blockers with their unblocking condition;
- reconcile the document with the diff and commands before handoff;
- archive it or mark it superseded when another system assumes authority.

Suggested minimum format:

| Status | Outcome | Origin | Strategy | Dependencies | Done when | Evidence |
|---|---|---|---|---|---|---|
| pending | observable behavior | requirement or ID | reuse/modify/create | real condition | objective criteria | command or scenario |

Do not add a progress percentage calculated from the number of items. Tasks vary
in risk and scope, and such a percentage creates false precision.

## How to avoid excessive planning

Apply these limits:

1. **Plan only to the next decision point.** Detail the first slice and known
   dependencies; keep the rest at the level necessary to avoid blocking future choices.
2. **Use a structure budget.** If the plan requires more text than the likely
   change, reduce fields and group only items with the same outcome.
3. **Do not prewrite the implementation.** Avoid names for helpers, files, or APIs
   that have not been verified.
4. **Do not create a task for each file.** A task represents an outcome; files are
   likely scope.
5. **Do not duplicate gates.** Reuse existing audit, code, security, and remediation criteria.
6. **Do not plan debt outside the request.** Record it separately without absorbing
   it into the critical path.
7. **Do not impose ceremony on a trivial change.** For a localized fix, one task
   with cause, change, and evidence may be enough.
8. **Stop at a material decision.** Do not turn product, security, or identity
   ambiguity into invented subtasks.

## How to avoid lists without evidence

A list is invalid when its items merely name activities: “create component,” “add
tests,” “improve accessibility,” “review security,” or “polish responsiveness.”
Each item must answer:

- which behavior will change;
- what evidence requires this change;
- which observable condition represents completion;
- which evidence can fail;
- which risks and states apply;
- what remains out of scope.

Before accepting a task, apply three tests:

1. **Removal test:** if the item disappears, does any requirement, finding, risk,
   or evidence lose coverage?
2. **Falsification test:** is there a scenario in which the task appears complete
   but the criterion would reject it?
3. **Consumer test:** will any foundation created be used by a concrete, near-term flow?

If the answer is “no” to all three, the task is probably planning decoration.

## Compatibility and boundaries

- Preserve the five current names and their invocation modes.
- Do not create a new invocation for planning.
- Do not change read-only skills to editing mode.
- Do not treat a plan as authorization to edit, install, commit, or publish.
- Do not impose a frontend, framework, directory structure, or issue tool.
- Do not require a complete list when the project calls for iterative investigation.
- Do not turn “vertical” into a rule requiring every layer in every task.
- Do not replace security, accessibility, audit, or remediation gates with a
  generic “QA” field.

## Conclusion

The strongest part of the external unit is its focus on independent, verifiable
deliverables. The plugin already has nearly all the discipline needed to make
this idea safer than its source: evidence before claims, scope preservation,
sensitive validation, real states, contextual security, and gated remediation.

The recommended work is to connect these pieces through a concise task contract
and distribute it among the five skills. Priority should go to vertical slices,
reuse/modify/create classification, semantic dependencies, a definition of done
with evidence, and authorized persistence. Fixed paths, automatic selection of
the most recent brief, universal phases, and time-based lists should remain out of
scope.
