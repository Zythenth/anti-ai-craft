# Analysis of the `design-brief` unit

## Scope and decision

This analysis compares the external `design-brief` unit in full with the plugin's
five current skills. The plugin was not changed. The recommendation is to absorb
only the brief contract and controlled persistence while preserving public names,
explicit invocation, and the existing separation among design, code, audit,
remediation, and security.

The unit is useful as a discovery flow and document format, but it should not be
incorporated literally. Its unlimited questionnaire, automatic writes, and
searches oriented toward specific stacks conflict with stronger controls already
present in the plugin.

## Complete inventory

### External unit examined

- external unit `design-brief/SKILL.md`
  - Defines activation for a brief request, page or feature planning, and interface direction.
  - Starts from a description provided by the user.
  - Explores tokens, themes, component libraries, component catalogs, UI dependencies, fonts, routes, and layouts.
  - Conducts an interview about the user, job to be done, success, tone, references, constraints, and content.
  - Produces one Markdown file per feature in a persistent directory.
  - Offers a template covering the problem, solution, principles, aesthetic direction, existing patterns, components, interactions, responsiveness, accessibility, and out-of-scope items.

This unit has no supporting files, interface configuration, or additional references.

### `anti-ai-design`

- `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
  - Scope; mandate to preserve, refine, or redesign; discovery; direction contract; operating modes; validation; and output contract.
- `plugins/anti-ai-craft/skills/anti-ai-design/agents/openai.yaml`
  - Public name, short description, default prompt, and disabled implicit invocation.
- `plugins/anti-ai-craft/skills/anti-ai-design/references/accessibility-baseline.md`
  - Semantics, keyboard, focus, menus, modals, tabs, forms, messages, contrast, reflow, motion, and a manual matrix.
- `plugins/anti-ai-craft/skills/anti-ai-design/references/design-antipatterns.md`
  - Contextual signs of generic composition, reflexive aesthetics, controls, motion, and responsiveness; includes rejection of authorship inference.
- `plugins/anti-ai-craft/skills/anti-ai-design/references/design-principles.md`
  - Decision model, briefing, identity, composition, components, overflow, tokens, writing, states, responsiveness, and portable criteria.
- `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
  - Surface, mandate, thesis, invariants, references, media, states, and production checks.
- `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
  - Preflight, structure, content, alternatives, authorized implementation, screenshots, independent passes, comparison, and human gate.
- `plugins/anti-ai-craft/skills/anti-ai-design/references/sources.md`
  - Evidence hierarchy, traceability, and limits of heuristics.

### `anti-ai-code`

- `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md`
  - Scoped review and implementation, repository inspection, API verification, falsifiable investigation, minimum change, and honest validation.
- `plugins/anti-ai-craft/skills/anti-ai-code/agents/openai.yaml`
  - Public name, short description, default prompt, and disabled implicit invocation.
- `plugins/anti-ai-craft/skills/anti-ai-code/references/architecture-antipatterns.md`
  - Abstraction, fragmentation, overengineering, compatibility, API, performance, observability, and documentation.
- `plugins/anti-ai-craft/skills/anti-ai-code/references/code-antipatterns.md`
  - Invented contracts, fabricated certainty, hidden failures, state, concurrency, security, local quality, and intersection with UI.
- `plugins/anti-ai-craft/skills/anti-ai-code/references/debugging-and-evidence.md`
  - Reproduction, hypotheses, experiments, evidence fitness, oracles, mocks, time, and API verification.
- `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
  - Scope, system model, discovery, validation, fix, and reporting.
- `plugins/anti-ai-craft/skills/anti-ai-code/references/sources.md`
  - Evidence matrix and limits of generalization.
- `plugins/anti-ai-craft/skills/anti-ai-code/references/testing-antipatterns.md`
  - Regression, false confidence, mocks, waits, snapshots, cases, oracles, and execution.

### `anti-ai-audit`

- `plugins/anti-ai-craft/skills/anti-ai-audit/SKILL.md`
  - Strictly read-only audit, baseline, ledger, finding rules, and closure.
- `plugins/anti-ai-craft/skills/anti-ai-audit/agents/openai.yaml`
  - Public name, short description, default prompt, and disabled implicit invocation.
- `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md`
  - Coverage of scope, interface, accessibility, code, architecture, tests, classification, and evidence.
- `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
  - Structure for summary, counts, findings, candidates, coverage, false positives, and validations.
- `plugins/anti-ai-craft/skills/anti-ai-audit/references/severity-model.md`
  - Severity, confidence, priority, classification, calibration, and deduplication.

### `anti-ai-remediate`

- `plugins/anti-ai-craft/skills/anti-ai-remediate/SKILL.md`
  - Approved input, preparation, gates, minimum fix, boundaries, and per-finding status.
- `plugins/anti-ai-craft/skills/anti-ai-remediate/agents/openai.yaml`
  - Public name, short description, default prompt, and disabled implicit invocation.
- `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md`
  - Permitted actions, new approval, interruption, prohibitions, and completion.
- `plugins/anti-ai-craft/skills/anti-ai-remediate/references/remediation-protocol.md`
  - Initial state, eligibility, plan, application, verification, validation, handoff, and rollback.
- `plugins/anti-ai-craft/skills/anti-ai-remediate/references/validation-checklist.md`
  - Evidence, preservation, regression, data, UI, and handoff.

### `anti-ai-security`

- `plugins/anti-ai-craft/skills/anti-ai-security/SKILL.md`
  - Analysis/fix modes, contextual threat, abuse by authenticated users, overlooked controls, evidence, and remediation.
- `plugins/anti-ai-craft/skills/anti-ai-security/agents/openai.yaml`
  - Public name, short description, default prompt, and disabled implicit invocation.
- `plugins/anti-ai-craft/skills/anti-ai-security/references/remediation-workflow.md`
  - Evidence, boundary, resource consumption, functional preservation, validation, and reporting.
- `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`
  - Threats, authentication, authorization, resources, inputs, client, files, secrets, dependencies, privacy, flows, and agents.
- `plugins/anti-ai-craft/skills/anti-ai-security/references/sources.md`
  - Sources used for controls and inference limits.
- `plugins/anti-ai-craft/skills/anti-ai-security/references/validation-and-severity.md`
  - Recording, falsification, severity, deduplication, and the fix gate.

## Observed behavior of the unit

### Project discovery

Discovery is suitable for familiar web applications: it looks for visual values,
styling configuration, library themes, component directories, component catalogs,
dependencies, fonts, and existing pages. The sound rule is to treat existing
components as the initial vocabulary.

Its limitations are:

- it assumes particular conventions and technologies, potentially overlooking
  different stacks, native applications, or differently organized design systems;
- it does not order authority among project instructions, product requirements,
  code, the design system, tests, and user preferences;
- it does not require recording the files actually read, weakening traceability;
- it does not explicitly cover data contracts, content, states, media, analytics,
  localization, performance, and integrations;
- it does not define what to do when no repository exists, the project is
  incomplete, or sources conflict.

The plugin already has broader discovery and a better order of authority. The only
part worth importing is an operational list of places to look for the visual
system, used heuristically and adapted to the repository.

### Inputs

Expected inputs are a description of what will be built, audience, constraints,
ideas, references, and interview answers. There is no contract distinguishing
required, optional, unknown, or decision-dependent data.

It also lacks:

- an explicit mandate to preserve, refine, or redesign;
- classification of the predominant surface;
- brief status, such as draft, blocked, or approved;
- explicit authorization to create or replace the file;
- identification of untrusted sources, sensitive data, or secrets that must not be persisted;
- a rule for requests that already provide enough information and need no interview.

### Output contract

The output template covers the foundation of a brief: human problem, intended
experience, a few principles, direction, existing patterns, components,
interactions, responsiveness, accessibility, and out-of-scope items.

It lacks elements required to connect planning with verifiable execution:

- the source and status of each relevant claim;
- functional requirements and invariants;
- real content and data, including edge cases and unavailability;
- a map of flows and states per interaction;
- acceptance criteria and a validation plan;
- risks, open decisions, assumptions, and decision owners;
- behavior that must remain unchanged;
- conditional requirements for security, privacy, localization, performance, and media;
- an unambiguous indication that the document is ready or still a draft.

### Persistence

Persistence per feature avoids collisions among different briefs and creates an
integration point for later work. Automatic writing, however, conflicts with the
current Anti-AI Design planning mode, which must not edit.

There is no policy for:

- authorization to write;
- safe normalization of the feature identifier;
- an existing file;
- incremental updates versus replacement;
- preservation of manual content;
- multiple briefs for the same feature;
- detecting that a brief is stale relative to code;
- staging, committing, or any other Git mutation;
- resuming after an incomplete interview.

### Failures and interruptions

The unit allows steps to be omitted but does not define failures. Unhandled cases include:

- insufficient context or contradictory answers;
- absence of a project, components, or tokens;
- missing assets or real content;
- denied access to a file or tool;
- conflict between documentation and implementation;
- inability to validate accessibility, responsiveness, or runtime;
- path collision;
- an attempt to overwrite an existing brief;
- accidental inclusion of a secret, personal data, or untrusted external content;
- a request combining a brief and implementation without clear authorization for each.

The correct response is to produce a marked draft, record gaps, and block only
material decisions. Missing information must not be filled with plausible details.

## Comparison matrix

| Capability | State | Where it exists today | Decision |
|---|---|---|---|
| Read the project before defining direction | Already present | `anti-ai-design/SKILL.md`, `design-principles.md` | Keep the current rule. |
| Discover tokens, components, themes, fonts, routes, and layouts | Partial | Broad discovery exists without a standardized operational inventory | Add an adaptable scan without binding it to stacks. |
| Treat existing components as the initial vocabulary | Already present | Preservation of architecture, tokens, components, and local patterns | Make explicit in brief mode. |
| Define user, task, context, constraints, and success | Already present | Design preparation and briefing | Reorganize as brief inputs without duplicating rules. |
| Recommend answers during the interview | Partial | The skill recommends direction and alternatives but defines no question protocol | Offer recommendations only for material decisions, with rationale and consequence. |
| Unlimited, exhaustive interview | Do not incorporate | Conflicts with the current question limit and may block work | Use short dependency-based rounds and stop when information is sufficient. |
| Classify surface and mandate | Already present, stronger | `anti-ai-design/SKILL.md` and `direction-contract.md` | Make mandatory in the brief. |
| Dominant reference and anti-defaults | Already present, stronger | Direction contract | Preserve and record in the brief when visual direction applies. |
| Human problem and intended experience | Partial | Task, user, and direction exist, but not in a stable document | Include in the persistent template. |
| Limit experience principles | Not present as a contract | General principles exist, not a short feature-specific selection | Adopt up to three, each resolving a real tension. |
| Existing/modify/new inventory | Partial | A component inventory exists without a brief decision table | Adopt with rationale and dependencies. |
| Detailed state contracts | Already present, stronger | `direction-contract.md` and the design workflow | Reference them; do not create a reduced version. |
| Responsiveness based on behavior change | Already present, stronger | Principles and viewport validation | Record feature-specific decisions. |
| Accessibility | Already present, much stronger | Complete baseline and manual validation | The brief should point to applicable requirements, not repeat the entire baseline. |
| Real content and placeholder distinction | Already present | Principles, antipatterns, and workflow | Record source, edge cases, and gaps in the brief. |
| Explicit out-of-scope section | Partial | Scope is controlled, but no mandatory brief section exists | Adopt to reduce expansion during implementation. |
| Persistent file per feature | Absent | Planning delivers a brief but defines no file | Adopt only with write authorization. |
| Update and collision policy | Absent | Missing | Adopt before any persistence. |
| Draft/approved/blocked status | Absent | Missing | Adopt so a hypothesis cannot become a contract. |
| Acceptance criteria and validation | Partial | The output contract already requires them, but the external template does not | Make a mandatory brief section. |
| Traceability of consulted sources | Already present | Workflow and evidence matrix | Bring into the brief as operational evidence, not an ornamental inventory. |
| Handoff to code | Partial | Code reads specifications and requirements, but there is no brief rule | Treat only an approved brief as a source, subordinate to project authorities. |
| Handoff to audit | Partial | Audit covers specifications/SDDs | Include an approved brief in coverage when in scope. |
| Handoff to remediation | Partial | Remediation requires approved findings and IDs | Prohibit a brief alone from authorizing fixes. |
| Document security and privacy | Absent in brief mode | Security covers the project, not persistence of the brief | Do not persist secrets/PII; include a conditional risk section. |
| Rigid search for specific names and frameworks | Do not incorporate as a rule | May produce false negatives and import architecture | Use as examples of clues, never a mandatory checklist. |
| Automatic writing during planning | Do not incorporate | Violates the current no-edit boundary | Require explicit authorization. |
| File as a mandatory bus for future skills | Do not incorporate | Creates coupling and assumes nonexistent skills | Accept a brief as an optional source, not a mandatory dependency. |

## Prioritized recommendations

The instructions below are new syntheses. They do not require renaming skills,
changing their identifiers, permitting implicit invocation, or altering current
public commands.

### DB-01 — Brief mode with a write boundary

- **Priority:** P0.
- **Exact target file:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`.
- **Concrete instruction:** under “Operate by mode,” add a “Design brief” subtype.
  It should discover the project, resolve material decisions, produce a structured
  document, and remain no-edit by default. Persist only when the user requests the
  file or authorizes writing; implementation remains separate authorization.
- **Reason:** uses the flow without violating the current promise that planning does not edit.
- **Risk:** ambiguous wording could make the skill write or begin implementation by inference.
- **Acceptance:** a “plan this screen” request returns the brief in conversation
  without mutation; “save the brief” creates only the authorized document; neither
  changes product code.
- **Requirement:** required to enable safe persistence.

### DB-02 — Dedicated reference for the brief contract

- **Priority:** P0.
- **Exact target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-brief.md` (new).
- **Concrete instruction:** define inputs, discovery, interview rounds, output
  schema, document states, persistence policy, failures, and completion criteria.
  Reuse current direction, state, accessibility, and review baselines by reference;
  do not duplicate them.
- **Reason:** avoids inflating `SKILL.md` and creates a verifiable contract for
  brief creation and updates.
- **Risk:** duplicating existing rules and allowing future divergence.
- **Acceptance:** every detailed brief rule lives in this file; `SKILL.md` only
  defines when to load it; there is no competing copy of the accessibility
  baseline or direction contract.
- **Requirement:** required if the mode is incorporated.

### DB-03 — Repository-adaptive discovery inventory

- **Priority:** P0.
- **Exact target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-brief.md`.
- **Concrete instruction:** guide the search for instructions, documentation,
  tokens/themes, components and catalogs, fonts/assets, routes/layouts,
  content/data, states, visual tests, and dependencies. File or framework names are
  conditional clues; first discover the real stack and commands. Record the path
  and relevance only of what was read.
- **Reason:** makes exploration repeatable without assuming a technology.
- **Risk:** a long list becoming ritual and consuming context on irrelevant files.
- **Acceptance:** in an unknown stack, the scan begins with manifests and
  structure; in a project without a frontend, visual items are marked not
  applicable; the brief lists sources actually used.
- **Requirement:** discovery of sources and patterns is required; specific
  categories and technologies are conditional.

### DB-04 — Classified inputs and impact-based questions

- **Priority:** P0.
- **Exact target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-brief.md`.
- **Concrete instruction:** classify each input as confirmed, low-risk assumption,
  open decision, or blocker. Ask in rounds of no more than two or three questions
  only when the answer changes direction, contract, security, or scope. For each
  material decision, present a recommendation, rationale, and consequence; allow
  a complete request to require no interview.
- **Reason:** combines useful collaboration with the existing discipline against ritual questioning.
- **Risk:** asking too little and crystallizing an incorrect requirement.
- **Acceptance:** material gaps are visible; minor assumptions are stated; no
  question is asked without explaining which decision it unlocks.
- **Requirement:** classification and limit are required; questions are conditional.

### DB-05 — Traceable brief schema

- **Priority:** P0.
- **Exact target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-brief.md`.
- **Concrete instruction:** require these sections: document identity and status;
  user problem; outcome and success signals; users/context; surface and mandate;
  sources and existing patterns; requirements/invariants; up to three principles
  that resolve tensions; direction and invariants; content/data/media; primary and
  alternative flows; component inventory; interaction and state contracts;
  responsive behavior; applicable accessibility requirements; out-of-scope work;
  risks/open decisions; acceptance criteria and validation plan.
- **Reason:** connects intent to implementation and testing instead of producing
  only aesthetic direction.
- **Risk:** making small briefs bureaucratic.
- **Acceptance:** if a section does not apply, it is marked not applicable with a
  reason; if it is unknown and material, the document remains draft or blocked;
  no section is filled with invented content.
- **Requirement:** problem, outcome, users, mandate, sources, invariants, flow,
  states, out-of-scope work, acceptance, and gaps are required; aesthetic
  direction, media, security, and other areas are conditional.

### DB-06 — Persistence without silent overwrite

- **Priority:** P0.
- **Exact target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-brief.md`.
- **Concrete instruction:** when authorized, use
  `.design/<safe-slug>/DESIGN_BRIEF.md`. Derive a lowercase, hyphenated identifier
  only from product text, remove path segments and unsafe characters, confirm the
  final directory is within `.design`, check for an existing file, and ask for a
  decision before replacing manual content. Updates should produce a small diff
  and preserve sections outside the request.
- **Reason:** provides a predictable address without collision, traversal, or loss.
- **Risk:** rigid adoption of the directory may conflict with an existing project convention.
- **Acceptance:** a documented local convention takes precedence; an existing file
  is never silently replaced; no stage, commit, push, or code change occurs as an
  implicit consequence.
- **Requirement:** path safety and no silent overwrite are required when
  persisting; the default path is conditional on the absence of a local convention.

### DB-07 — Document states and failures

- **Priority:** P0.
- **Exact target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-brief.md`.
- **Concrete instruction:** use `draft`, `blocked`, and `approved` states. Record the
  reason, missing decisions, and validations not run. Tool, access, runtime, or
  context failures should produce an explicit gap; source conflicts should
  preserve alternatives and request a decision when material. Never turn absence
  into a placeholder presented as fact.
- **Reason:** prevents an incomplete document from being treated as a final contract.
- **Risk:** the agent assigning the “approved” label without a human decision.
- **Acceptance:** only explicit user confirmation changes the document to approved;
  an external failure is not presented as design failure; every blocker states
  the data or decision needed to proceed.
- **Requirement:** required.

### DB-08 — Safe integration with implementation

- **Priority:** P1.
- **Exact target file:** `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`.
- **Concrete instruction:** while building the system model, read the brief only
  when provided, cited by the project, or directly related to scope. Record its
  status and logical date relative to the code. Treat an approved brief as a
  requirement source, but subordinate it to higher-authority instructions and
  current behavior the user asked to preserve. Map acceptance criteria to paths
  and tests; a draft does not authorize implementation.
- **Reason:** creates continuity between planning and code without mandatory coupling.
- **Risk:** a stale document being used against valid implementation.
- **Acceptance:** divergences are reported before editing; material criteria become
  specific evidence; absence of a brief does not block code tasks.
- **Requirement:** conditional on the brief's existence and relevance.

### DB-09 — Brief coverage in audits

- **Priority:** P1.
- **Exact target file:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md`.
- **Concrete instruction:** when an approved brief is in scope, record its
  version/status, map every requirement and acceptance criterion to implemented,
  partial, missing, divergent, ambiguous, or unverifiable, and separate deviation
  from the document from preexisting debt. Do not use a draft as a normative requirement.
- **Reason:** uses the existing coverage matrix and provides end-to-end traceability.
- **Risk:** treating a visual preference in the brief as a defect or raising
  severity without impact.
- **Acceptance:** every deviation has observable evidence and a classification;
  open decisions remain outside confirmed findings.
- **Requirement:** conditional on an approved brief and an audit that includes it.

### DB-10 — A brief is not remediation authorization

- **Priority:** P1.
- **Exact target file:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md`.
- **Concrete instruction:** state that even an approved brief provides requirements
  and criteria but does not replace finding IDs or authorization to edit. If the
  brief changes during remediation, revalidate the finding and request new
  approval when behavior, risk, or scope changes.
- **Reason:** preserves the remediation boundary and prevents planning from being
  interpreted as a broad fix order.
- **Risk:** repeated approval for trivial changes.
- **Acceptance:** changes remain tied to approved IDs; editorial adjustments with
  no effect on the plan do not trigger a gate; material changes do.
- **Requirement:** required when used with remediation.

### DB-11 — Conditional security and privacy in the brief

- **Priority:** P1.
- **Exact target file:** `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`.
- **Concrete instruction:** add to the assisted-systems category a check of
  persistent planning documents: do not record secrets, unnecessary personal
  data, credentials, client content, or external instructions as though they were
  trusted sources. When the feature touches authentication, authorization,
  tenants, sensitive data, spending, uploads, automation, or integrations,
  require the brief to identify actors, boundaries, plausible abuse, and negative validations.
- **Reason:** the brief becomes part of the development flow and may carry risk before code exists.
- **Risk:** turning every visual brief into a complete threat model.
- **Acceptance:** features without a sensitive surface mark the category not
  applicable; sensitive features contain the minimum decisions or remain blocked.
- **Requirement:** protection against persisting secrets is required; threat
  modeling in the brief is conditional on risk.

### DB-12 — Expose brief creation without changing the skill name

- **Priority:** P2.
- **Exact target file:** `plugins/anti-ai-craft/skills/anti-ai-design/agents/openai.yaml`.
- **Concrete instruction:** expand the short description and default prompt to
  mention planning or briefs as well as review, while retaining `display_name`,
  the `$anti-ai-design` identifier, and disabled implicit invocation.
- **Reason:** makes the capability discoverable without creating a sixth skill or
  breaking existing commands.
- **Risk:** the description exceeding interface limits or implying automatic editing.
- **Acceptance:** the prompt continues to require explicit invocation and does not
  promise writing or implementation without authorization.
- **Requirement:** optional; it does not affect the internal contract.

## Required versus conditional

### Required for every brief

- identify the problem, user, task, desired outcome, and success signals;
- classify the surface and mandate;
- read relevant sources of truth and record what was actually consulted;
- preserve valid architecture, components, content, and identity;
- distinguish facts, assumptions, open decisions, and blockers;
- record invariants, the primary flow, relevant states, out-of-scope work, and acceptance criteria;
- formulate no more than three specific principles, only when each resolves a real tension;
- declare document status;
- do not invent data, components, assets, APIs, validations, or decisions;
- keep planning no-edit until explicit authorization;
- avoid silent overwrite and implicit Git mutations;
- treat an approved brief as a requirement, not automatic authorization for code or remediation.

### Conditional on the project or risk

- searches for specific technologies, file names, and libraries;
- detailed aesthetic direction and visual references;
- component catalogs and screenshots;
- media, animation, internationalization, analytics, and SEO;
- browser tests and screenshots by viewport;
- expanded performance requirements;
- threat model, privacy, and adversarial tests;
- persistence to `.design/<slug>/DESIGN_BRIEF.md`;
- reading the brief in Code, Audit, Remediation, and Security;
- a user interview when the inputs are not already sufficient.

### Do not incorporate

- interviewing “until everything is exhausted”;
- a mandatory recommendation for every question;
- automatic writing during planning;
- overwrite without confirmation;
- a rigid framework list as the definition of discovery;
- a persistent file as a mandatory dependency among skills;
- accessibility reduced to a few checks in the template;
- automatic code changes after brief creation;
- approval inferred by the agent;
- missing details filled by plausibility.

## Recommended implementation order

1. Implement DB-01 through DB-07 within Anti-AI Design.
2. Validate the flow in three scenarios: an existing project with a design system,
   a project with no explicit visual system, and a request without a repository.
3. Add DB-08 through DB-11 for handoffs among skills.
4. Apply DB-12 only if the public interface remains clear within text limits.
5. Run structural validation of all five skills and review the diff to confirm that
   names, identifiers, and invocation policy did not change.

## Summary

The external unit contributes two useful ideas that remain incomplete in the
plugin: one brief document per feature and an operational inventory for visual
discovery. The rest already exists, generally in stronger form, across the five
skills. The best evolution is a brief mode within `anti-ai-design`, with its own
template, opt-in writing, explicit status, traceable failures, and conditional
handoffs. There is no need to create a new skill, rename existing ones, or couple
the plugin to a single path or stack.
