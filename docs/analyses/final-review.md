# Final coverage review

Date: 2026-07-24

Update from 2026-07-25: version `0.4.0` retains hybrid activation. Anti-AI Design,
Anti-AI Code, and Anti-AI Security may be selected implicitly from context;
Anti-AI Design Flow, Anti-AI Audit, and Anti-AI Remediation remain exclusively
manual. This change preserves the authorization boundaries described in the
report. The same version expands Anti-AI Design with 101 original,
outcome-oriented principles, loaded by theme and subordinate to the task,
evidence, and protections for autonomy.

## Verdict

**PASS for committable content.**

All eight units were analyzed in full, each has its own report, and all 99 titled
recommendations were rechecked. Ninety-eight were incorporated. One remains
deliberately and safely deferred: `DF-23`, because private vulnerability reporting
for the repository was checked and is disabled. Creating `SECURITY.md` before a
monitored channel exists would make a false promise.

The five previous skills retain their identifiers. The only public addition is
`$anti-ai-design-flow`, explicit and optional for journeys with three or more
phases.

## Artifacts examined

- the eight reports under `docs/analyses/`;
- `README.md` and the marketplace;
- the manifests, metadata, and contracts for all six skills;
- every internal reference in the six skills;
- Git state and the complete repository diff.

## Complete recommendation matrix

`Incorporated` means that the contract and acceptance evidence are present in the
final state. The `BT-*` identifiers were assigned only in this review because the
original task report uses priority-based titles instead of IDs.

### Design flow

| ID | Recommendation | Status |
|---|---|---|
| DF-01 | Route the complete flow to the orchestrator | Incorporated |
| DF-02 | Formalize criteria for skipping phases | Incorporated |
| DF-03 | Create a resumable checkpoint | Incorporated |
| DF-04 | Define invalidation across phases | Incorporated |
| DF-05 | Make information architecture a minimum output | Incorporated |
| DF-06 | Define completion criteria for tokens | Incorporated |
| DF-07 | Produce a verifiable build plan | Incorporated |
| DF-08 | Consume the plan in code | Incorporated |
| DF-09 | Require evidence before completing a task | Incorporated |
| DF-10 | Add a security gate before the build | Incorporated |
| DF-11 | Propagate changes to the threat model | Incorporated |
| DF-12 | Create a review-readiness gate | Incorporated |
| DF-13 | Validate the decision chain | Incorporated |
| DF-14 | Make the audit recognize flow artifacts | Incorporated |
| DF-15 | Record flow coverage | Incorporated |
| DF-16 | Preserve IDs in the remediation handoff | Incorporated |
| DF-17 | Reconcile state after remediation | Incorporated |
| DF-18 | Standardize pausing and resumption | Incorporated |
| DF-19 | Use material gates without ritual confirmation | Incorporated |
| DF-20 | Make handoffs explicit | Incorporated |
| DF-21 | Publish the new skill without changing the five existing ones | Incorporated |
| DF-22 | Update public selection guidance | Incorporated |
| DF-23 | Define private vulnerability disclosure | Deferred: depends on an operational private channel |
| DF-24 | Add a release gate | Incorporated |
| DF-25 | Explain the risk of mutable updates | Incorporated |

### Interview and decisions

| ID | Recommendation | Status |
|---|---|---|
| GRM-01 | Add an explicit decision gate to design | Incorporated |
| GRM-02 | Close visual-direction branches | Incorporated |
| GRM-03 | Separate technical discovery from contract choices | Incorporated |
| GRM-04 | Order decisions by dependency | Incorporated |
| GRM-05 | Ask questions without interrupting independent coverage | Incorporated |
| GRM-06 | Structure pending decisions in the report | Incorporated |
| GRM-07 | Distinguish missing information from missing approval | Incorporated |
| GRM-08 | Classify questions at gates | Incorporated |
| GRM-09 | Make the threat model traceable | Incorporated |
| GRM-10 | Record dependencies and recommendations in security work | Incorporated |
| GRM-11 | Preserve metadata and compatibility | Incorporated |

### Design brief

| ID | Recommendation | Status |
|---|---|---|
| DB-01 | Add a brief mode with a write boundary | Incorporated |
| DB-02 | Create a dedicated brief reference | Incorporated |
| DB-03 | Make discovery adapt to the repository | Incorporated |
| DB-04 | Classify inputs and questions by impact | Incorporated |
| DB-05 | Use a traceable brief schema | Incorporated |
| DB-06 | Persist without silent overwrite | Incorporated |
| DB-07 | Define document states and failures | Incorporated |
| DB-08 | Integrate safely with implementation | Incorporated |
| DB-09 | Cover the brief in audits, including unverifiable items | Incorporated |
| DB-10 | Do not let a brief authorize remediation | Incorporated |
| DB-11 | Make security and privacy conditional | Incorporated |
| DB-12 | Expose the brief without renaming the skill | Incorporated |

### Information architecture

| ID | Recommendation | Status |
|---|---|---|
| IA-01 | Add a structural reference within design | Incorporated |
| IA-02 | Route to the reference from the primary contract | Incorporated |
| IA-03 | Add structural invariants to the direction contract | Incorporated |
| IA-04 | Add a structural pass to visual review | Incorporated |
| IA-05 | Include structural coverage in audits | Incorporated |
| IA-06 | Add a remediation gate for navigation and URLs | Incorporated |
| IA-07 | Add routes and state to the code contract | Incorporated |
| IA-08 | Address information architecture security | Incorporated |
| IA-09 | Define measurable information architecture criteria | Incorporated |
| IA-10 | Preserve existing public metadata | Incorporated |

### Design tokens

| ID | Recommendation | Status |
|---|---|---|
| DT-01 | Establish a central token procedure | Incorporated |
| DT-02 | Route token requests explicitly | Incorporated |
| DT-03 | Make token audits verifiable | Incorporated |
| DT-04 | Define contextual families | Incorporated |
| DT-05 | Validate visually and technically | Incorporated |
| DT-06 | Define technical token antipatterns | Incorporated |
| DT-07 | Remediate at the source and according to actual reach | Incorporated |
| DT-08 | Add a gate for global changes | Incorporated |
| DT-09 | Make evidence optional in the report | Incorporated |
| DT-10 | Treat a dynamic theme as untrusted input | Incorporated |

### Brief to tasks

| ID | Recommendation | Status |
|---|---|---|
| BT-01 | Use a common contract for verifiable tasks | Incorporated |
| BT-02 | Use vertical slices in design planning | Incorporated |
| BT-03 | Classify the inventory operationally | Incorporated |
| BT-04 | Preserve remediation gates in the plan | Incorporated |
| BT-05 | Include security in the definition of done | Incorporated |
| BT-06 | Give dependencies useful semantics | Incorporated |
| BT-07 | Organize next steps into provable batches | Incorporated |
| BT-08 | Make evidence part of state | Incorporated |
| BT-09 | Apply accessibility proportionately per slice | Incorporated |
| BT-10 | Prohibit a completed foundation with no consumer | Incorporated |
| BT-11 | Persist plans without a universal file | Incorporated |
| BT-12 | Update and close the plan | Incorporated |
| BT-13 | Adjust prompts without renaming skills | Incorporated |

### Frontend

| ID | Recommendation | Status |
|---|---|---|
| FD-01 | Use a proportionate reuse inventory | Incorporated |
| FD-02 | Define visual direction along explicit axes | Incorporated |
| FD-03 | Make the theme contract conditional | Incorporated |
| FD-04 | Add a gate for external visual resources | Incorporated |
| FD-05 | Validate mobile reading and forms | Incorporated |
| FD-06 | Use a proportionate theme matrix | Incorporated |
| FD-07 | Classify motion by function | Incorporated |
| FD-08 | Include reuse evidence in audits | Incorporated |

### Design review

| ID | Recommendation | Status |
|---|---|---|
| ADR-R01 | Define evidence profiles | Incorporated |
| ADR-R02 | Use a risk-based coverage matrix | Incorporated |
| ADR-R03 | Define a screenshot and write policy | Incorporated |
| ADR-R04 | Create a dedicated design review template | Incorporated |
| ADR-R05 | Separate severity, confidence, priority, and gate | Incorporated |
| ADR-R06 | Require bidirectional evidence | Incorporated |
| ADR-R07 | Use conditional, reproducible viewport probes | Incorporated |
| ADR-R08 | Represent environment failures and coverage | Incorporated |
| ADR-R09 | Make the application handoff explicit | Incorporated |
| ADR-R10 | Preserve decisions | Incorporated |

## Independent-audit corrections

The first final audit found eight P1 gaps. All were fixed and reaudited with a
result of `8/8 PASS`. An additional security pass found one more P1 gap, which was
also fixed and revalidated:

1. internal references do not simulate invocation of other skills;
2. execution and screenshots depend on the evidence profile;
3. accessibility and UI use a proportionate matrix, not a universal ritual;
4. visual findings preserve the feature, phase, artifact, and state;
5. document states were normalized;
6. the structural pass covers entry, navigation, URL, return, and recovery;
7. viewport probes are conditional fallbacks, not imposed breakpoints;
8. the audit explicitly represents the `unverifiable` state;
9. visual runtime requires a known environment, authorization for external side
   effects, a preference for fixtures, and redaction of secrets, PII, and client
   content.

## Deliberately rejected rules

The following were not incorporated:

- universal dark themes, mobile-first approaches, stacks, frameworks, scales, or breakpoints;
- automatic TDD, commits, pushes, installation, remediation, or writes;
- questions, confirmations, or phases used as rituals;
- silent selection of the most recent document;
- persistence to a fixed path;
- mandatory screenshots, browsers, screen readers, or Cartesian matrices without
  a relationship to scope and risk;
- universal concealment of actions in an ellipsis menu;
- inference of AI authorship from a visual pattern.

## Behavioral tests

### Scoped review

A test with a single `Edit` action hidden in an ellipsis menu:

- remained within the requested component;
- stated the evidence profile and limitation;
- treated the menu as a contextual heuristic, not evidence of authorship;
- produced a single traceable finding;
- did not start the complete flow.

### New flow

A test of multitenant B2B onboarding:

- kept the initial stage read-only;
- separated planning from authorization to edit;
- triggered a conditional security gate for roles, tenants, and invitations;
- did not impose a dark theme;
- asked only three material questions;
- produced phases, states, and a checkpoint without automatic persistence.

## Technical validation

- six `SKILL.md` files approved by the official validator;
- manifest approved by the official plugin validator;
- all local Markdown links in the skills resolve;
- three `allow_implicit_invocation: true` policies and three `false`, matching the hybrid mode;
- each interface prompt mentions the correct identifier;
- the README, manifest, and directories agree on six skills and version `0.4.0`;
- no citation, URL, authorship, or source-repository name remains;
- no temporary research source remains in the working tree;
- `git diff --check` passed immediately before the commit.

## Safe external dependency

`DF-23` is not a gap to fill with fictional text. The repository configuration
offers the option to enable private reports, but it was disabled when checked. The
correct action for a future version is:

1. the maintainer enables and assumes responsibility for monitoring the private channel;
2. the submission flow is confirmed;
3. only then is `SECURITY.md` published with its scope, supported versions,
   minimum required information, and a prohibition against submitting real secrets.

That configuration was not changed in this task.
