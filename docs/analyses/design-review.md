# Analysis of the `design-review` unit

## Scope and method

This analysis compares the external `design-review` unit in full with the
plugin's five current skills and all associated references and interface
configurations. The objective is to identify capabilities already covered, real
gaps, and adaptable improvements without copying text, changing public
identifiers, or mixing review with editing.

No plugin file was changed in this stage. This document is only a research report.

## Inventory examined

### External unit

| Artifact | Observed function |
|---|---|
| `design-review/SKILL.md` | Defines a structured critique based on a brief, code, and screenshots; proposes responsive coverage, states, accessibility, severity, and a persistent report. |

### Current plugin

| Skill | Role relevant to this analysis | Coverage examined |
|---|---|---|
| `anti-ai-design` | Contextual visual direction, review, and implementation | Primary contract, agent configuration, and six references |
| `anti-ai-code` | Scoped code inspection and change | Primary contract, agent configuration, and six references |
| `anti-ai-audit` | Broad, strictly read-only audit | Primary contract, agent configuration, and three references |
| `anti-ai-remediate` | Application of confirmed, approved findings | Primary contract, agent configuration, and three references |
| `anti-ai-security` | Analysis and remediation of abuse paths | Primary contract, agent configuration, and four references |

The README, plugin manifest, and marketplace entry were also considered to verify
names, invocation, compatibility, and public promises.

## Executive conclusion

The plugin already contains the most valuable parts of design review: sources of
truth; a preserve/refine/redesign mandate; real screenshots; code inspection;
three viewport bands; critical states; accessibility; separate visual and
technical passes; traceable evidence; and approval before broad changes.

The main gaps are not in the visual checklist. They are in review operations:

1. there is no explicit evidence-sufficiency contract to distinguish review of a
   running app, a supplied screenshot, and code-only inspection;
2. there is no formal coverage matrix by route, state, viewport, and theme;
3. there is no dedicated design-review template with stable IDs and separate
   severity, confidence, priority, and delivery gate;
4. there is no definition of where screenshots may be stored without turning a
   review into silent editing;
5. there is no explicit handoff from approved findings to remediation.

The external unit also contains rigid rules that should not be transplanted.
Requiring a self-produced capture in every case, writing artifacts into the
project without authorization, imposing universal viewport sizes, or treating a
CSS strategy as a requirement would conflate method, evidence, and permission.

## Recommended review modes

The plugin should retain existing modes and make four evidence profiles explicit
within **Review** mode:

| Profile | Sufficient input | Permitted claims | Required limits |
|---|---|---|---|
| Full runtime | Executable application, accessible routes, and browser tooling | Visual outcome, responsive behavior, interaction, observed states, and causes confirmed in code | Record the environment, data, viewport, theme, and states actually exercised |
| Partial runtime | Part of the app is executable, but routes, credentials, or data are unavailable | Claims only about reachable surfaces | List gaps by route/state and do not mark the rest approved |
| Visual artifact | Screenshots or video provided by the user | Hierarchy, composition, and defects visible in the supplied frame | Do not infer focus, keyboard, responsiveness, transitions, semantics, or absent states |
| Code only | Code, diff, or components without reliable execution | Structure, tokens, potential semantics, implemented coverage, and technical risks | Do not claim rendered visual quality; label visual conclusions unverified |

These profiles create no new skills and do not change invocation. They only
prevent partial evidence from producing a total conclusion.

## Visual evidence and code evidence

### Sufficiency principle

Each claim should use the appropriate type of evidence:

- a screenshot or runtime observation demonstrates the rendered symptom, not necessarily the cause;
- code and the accessibility tree help locate a cause but do not alone demonstrate the visual outcome;
- an automated test detects programmed rules but does not replace visual, keyboard, or assistive-technology inspection;
- a supplied screenshot demonstrates only the state, viewport, and moment represented;
- a diff shows what changed but does not automatically limit every affected surface;
- an environment failure does not confirm a product defect.

### Minimum evidence manifest

For every capture used in a finding, record:

- capture identifier or path;
- route or surface;
- state and data;
- width, height, and scale;
- theme and relevant preferences;
- browser or environment;
- origin: captured during execution or supplied;
- comparison point when before/after evidence exists.

For every cause attributed to code, record the component, file, stable line when
available, execution path, and relationship between implementation and the visual symptom.

### Storage

A review without edit authorization should not create permanent directories in
the repository. Captures may remain in a temporary directory or be presented in
the conversation. Persisting screenshots or a report inside the project should
require explicit authorization and use the path already adopted by the
repository. The absence of a dedicated directory never authorizes creating a new convention.

## Coverage of routes, states, viewports, and themes

### Surface inventory

Before captures, list:

- relevant routes and variants;
- shared shell, navigation, and overlays;
- components reused across routes;
- roles and permissions;
- data and network states;
- themes and accessibility preferences;
- critical flows and recovery.

For a change review, the inventory should begin with requested scope and changed
files but include affected reachable consumers and surfaces. When the target is a
branch or diff, document the baseline instead of assuming it.

### Coverage matrix

The report should include a matrix like this:

| Surface | Criticality | States exercised | Viewports | Theme/input | Evidence | Status |
|---|---|---|---|---|---|---|
| route or component | critical, important, or supporting | normal, loading, empty, error, permission, etc. | narrow, intermediate, wide | light/dark, keyboard/touch, etc. | capture, execution, code | covered, partial, blocked, or not applicable |

The matrix does not require the Cartesian product of every combination. Selection
should be guided by risk, reuse, and criticality. A shared component may reduce
repetition as long as variations by route, content, and state are verified.

### Viewports

Project breakpoints and actual content failures take precedence. When no criteria
are defined, the following may be used as initial probes:

- narrow: `375 × 812`;
- intermediate: `768 × 1024`;
- wide: `1280 × 800`;
- additional reflow: `320 CSS px`, when applicable.

These dimensions are operational defaults, not universal requirements. The goal
is to find points where hierarchy, reading, navigation, touch, or actions stop
working. For before/after comparison, keep data, state, viewport, scale, and theme equivalent.

### States

Select according to the component and flow:

- normal, hover, focus, active, selected, expanded, and disabled;
- empty, loading, partial, success, warning, error, offline, and permission denied;
- long strings, minimum/maximum content, missing media, and extreme data;
- modals, menus, drawers, tooltips, tabs, and forms in meaningful states;
- focus return, interruption, retry, undo, and recovery;
- reduced motion, forced colors, and dark theme when supported.

An inapplicable state should be marked as such, not silently omitted.

## Severity, confidence, priority, and gate

The external unit groups items as requirements, recommendations, and polish. This
structure helps reading but mixes impact with work order. The plugin already has a
better model and should reuse it:

- **severity:** observable consequence of the problem;
- **confidence:** strength of evidence;
- **priority:** recommended order of the fix;
- **gate:** pass, pass with reservations, block, or human decision.

For design, calibration should consider:

- blockage of the primary task or recovery;
- applicable normative accessibility failures;
- an invisible or unreachable primary action;
- loss of information, focus, state, or content;
- reach across routes, roles, devices, and shared components;
- task frequency;
- reversibility and cost of error;
- runtime evidence versus a code hypothesis.

An aesthetic preference without observable harm remains an observation or pending
decision. It should not be artificially elevated to a defect.

## Recommended report

A dedicated design-review report should include:

1. scope, mandate, and sources of truth actually read;
2. environment, baseline, and evidence profile;
3. capture manifest;
4. coverage matrix;
5. summary and gate decision;
6. findings with stable IDs, for example `ADR-001`;
7. for each finding: severity, confidence, priority, surface, state, viewport,
   visual evidence, code evidence, impact, rule, disconfirming evidence, suggested
   fix, risk, and acceptance;
8. decisions that work and should be preserved;
9. rejected false positives and preferences kept separate;
10. environment failures, gaps, and untested areas;
11. an optional application plan by ID, without editing;
12. residual risk.

The report should be saved in the repository only when authorized. Otherwise, it
should be delivered in the conversation.

## Optional application and separation of permissions

Review ends with the report. A suggested fix is not authorization to change files.

Safe flow:

1. produce findings with IDs and acceptance criteria;
2. ask the user to select IDs;
3. route only approved IDs to `anti-ai-remediate`, or enter the
   `anti-ai-design` implementation mode if the user explicitly requests it;
4. revalidate current state and evidence;
5. capture before/after evidence under equivalent conditions;
6. request new approval if identity, navigation, architecture, scope, or risk changes.

Capturing a screen for observation does not authorize fixing the component.
Saving a capture, creating a report, installing a dependency, starting a mutable
service, or changing a fixture must also respect scope and project rules.

## Failure handling

| Failure | Recommended response | What not to conclude |
|---|---|---|
| Application does not start | Record command, output, environment, and try only the official safe procedure | Do not automatically call it a visual defect |
| Browser or capture unavailable | Use supplied artifacts or reduce the evidence profile | Do not declare a complete visual review |
| Route requires unavailable credentials/data | Mark the surface blocked and request the minimum needed | Do not invent a fixture or account |
| External font, image, or API fails | Distinguish an environmental problem from inadequate product fallback | Do not attribute cause without tracing network and code |
| Screenshot differs because of data/theme/viewport | Invalidate the comparison and recapture under equivalent conditions | Do not declare an improvement or regression |
| Automated test passes | Record only the control actually tested | Do not infer overall visual quality |
| Evidence conflicts | Preserve both sides, formulate a hypothesis, and run a discriminating test | Do not choose the more convenient evidence |
| Finding would require editing to confirm | Stop at the risk and request authorization or another means of proof | Do not edit silently |
| Capture would require a permanent file | Use a temporary location or request authorization | Do not create a project convention |
| Scope becomes too broad | Record the cutoff and residual risk | Do not finish without stating unreviewed areas |

## Incorporation matrix

| Observed capability | State in the plugin | Decision |
|---|---|---|
| Read the brief, design system, code, assets, and project rules | Already present | Keep |
| Compare implementation with direction and task | Already present | Keep |
| Preserve, refine, or redesign mandate | Already present | Keep |
| Inventory screens, routes, components, content, and states | Already present | Keep |
| Inspect tokens, duplicate components, and local patterns | Already present | Keep |
| Execute the interface and use real screenshots | Already present | Keep |
| Review narrow, intermediate, and wide ranges | Already present | Keep |
| Exercise critical states, keyboard, screen reader, and recovery | Already present | Keep |
| Compare before/after under equivalent conditions | Already present | Keep |
| Separate the visual/UX pass from the technical pass | Already present | Keep |
| Cite screenshot, viewport, component, file, or line | Already present | Keep |
| Separate normative failure, inconsistency, heuristic, and preference | Already present | Keep |
| Do not edit during an audit and request approval for implementation | Already present | Keep |
| Continue coverage after the first finding | Already present in audit | Repeat explicitly in design review |
| Formal route × state × viewport × theme coverage | Partial | Incorporate with risk-based sampling |
| Evidence profile for runtime, supplied screenshots, and code | Partial | Incorporate |
| Viewport defaults when the project defines no breakpoints | Partial | Incorporate as probes, not standards |
| Screenshot manifest with environment and origin | Partial | Incorporate |
| Dark theme and accessibility preferences | Partial | Make an explicit dimension when supported |
| Exact inventory of changed files and affected consumers | Partial | Incorporate into diff review |
| Rendering defects such as missing fonts, clipping, overflow, and overlap | Partial | Make explicit in the runtime pass |
| Record what works and should be preserved | Partial | Incorporate with evidence |
| Dedicated design-review template | Absent | Create without changing the public interface |
| Stable IDs for handoff of visual findings | Absent | Incorporate |
| Rules for temporary or permanent capture storage | Absent | Incorporate |
| Taxonomy of capture and environment failures | Absent | Incorporate |
| Final gate separate from severity and priority | Not explicit in design | Incorporate |
| Requirement to capture the app in every review, including an isolated image | Do not incorporate | Evidence should follow actual scope |
| Block every review until the user supplies three screenshots | Do not incorporate | Allow a partial report with clear gaps |
| Always create a design directory and save captures | Do not incorporate | Violates local conventions and may constitute editing |
| Always save a report in the project | Do not incorporate | Requires write authorization |
| Fixed viewport sizes as a universal requirement | Do not incorporate | Breakpoints depend on content and product |
| `44 × 44` as a universal normative minimum | Do not incorporate | Preserve the distinction between an applicable requirement and a platform target |
| Require a mobile-first strategy based on a specific media-query type | Do not incorporate | Assess behavior, not implementation preference |
| Require a dark theme in a product that does not have one | Do not incorporate | Test only real support and requirements |
| Require a named aesthetic philosophy | Do not incorporate | The task, identity, and existing sources may be sufficient |
| Automatically apply the refinement list | Do not incorporate | Review and editing remain separate permissions |

## Prioritized recommendations

### ADR-R01 — Formalize evidence profiles

- **Priority:** P0
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instruction:** add the four review profiles and limit claims to what each
  profile can demonstrate.
- **Reason:** today the skill requests a real capture but does not define a
  calibrated response when runtime, a route, or a browser is unavailable.
- **Risk:** making the process bureaucratic for small reviews.
- **Acceptance:** every report identifies the profile used, distinguishes observed
  from unverified, and does not declare a complete visual review from code alone.

### ADR-R02 — Create a risk-based coverage matrix

- **Priority:** P0
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instruction:** require a surface inventory and matrix with route/component,
  criticality, states, viewports, theme/input, evidence, and disposition.
- **Reason:** “narrow, intermediate, and wide” does not ensure important routes
  and states were covered.
- **Risk:** combinatorial explosion.
- **Acceptance:** the instruction permits justified sampling, records cutoffs, and
  prevents an untested surface from being marked approved.

### ADR-R03 — Define capture and write policy

- **Priority:** P0
- **Target files:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md` and `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instruction:** state that review is no-edit by default; permanent captures and
  an on-disk report require authorization, while temporary evidence may remain
  outside the target.
- **Reason:** taking screenshots can create files and contradict the separation
  between analysis and editing.
- **Risk:** losing useful artifacts at the end of a task.
- **Acceptance:** without authorization, no permanent file is created; with
  authorization, the path follows the existing convention and appears in the report.

### ADR-R04 — Add a dedicated design-review template

- **Priority:** P0
- **Target files:** new `plugins/anti-ai-craft/skills/anti-ai-design/references/design-review-template.md` and a link in `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Instruction:** create a template with scope, evidence profile, capture
  manifest, coverage, gate, `ADR-*` IDs, complete findings, preserved decisions,
  false positives, gaps, and an optional plan.
- **Reason:** the current contract describes general fields but does not guarantee
  a consistent visual report or ID-based handoff.
- **Risk:** duplication with the audit template.
- **Acceptance:** the new template reuses existing severity and evidence fields,
  adding only UI-specific dimensions.

### ADR-R05 — Separate severity, confidence, priority, and gate

- **Priority:** P1
- **Target files:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md` and the new template
- **Instruction:** reference the existing severity model and define an independent delivery gate.
- **Reason:** “fix now/later/polish” lists conflate impact, order, and release decisions.
- **Risk:** too many categories for a simple finding.
- **Acceptance:** each primary finding contains all four axes or explains why one
  does not apply; aesthetic preferences do not receive inflated severity.

### ADR-R06 — Make evidence bidirectional

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instruction:** connect the visual symptom to its code cause and require
  disconfirming evidence; prevent an isolated screenshot from proving a cause or
  isolated code from proving the rendered outcome.
- **Reason:** reduces plausible but unproven diagnoses.
- **Risk:** increasing the cost of obvious findings.
- **Acceptance:** high-severity findings have visual and technical evidence when
  both are reachable; limitations are explicit when either is missing.

### ADR-R07 — Standardize viewport probes without making them universal

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instruction:** use project breakpoints first and, when absent, suggest
  `375 × 812`, `768 × 1024`, and `1280 × 800`, retaining `320 CSS px` as an
  applicable reflow test.
- **Reason:** improves reproducibility without replacing the product's responsive decisions.
- **Risk:** agents treating defaults as a ritual list.
- **Acceptance:** the text calls the dimensions initial probes, requires adaptation
  to content, and records the dimensions actually used.

### ADR-R08 — Make environment and coverage failures explicit

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instruction:** include dispositions for unavailable runtime, blocked routes,
  missing credentials, failed captures, external assets, invalid comparisons, and
  insufficient automated tests.
- **Reason:** prevents inability to observe from being confused with approval or a defect.
- **Risk:** longer reports.
- **Acceptance:** each operational failure appears as a limitation, blocker, or
  gap; it does not become a product finding without a causal path.

### ADR-R09 — Explicit handoff for optional application

- **Priority:** P1
- **Target files:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md` and the new template
- **Instruction:** end review with IDs and offer application only after explicit
  selection, preferably through `anti-ai-remediate`.
- **Reason:** aligns design with the protocol already adopted by audit and remediation.
- **Risk:** friction in tasks where the user requested review and fixes together.
- **Acceptance:** a review-only request does not edit; a combined request keeps a
  findings stage before application and records which IDs were authorized.

### ADR-R10 — Record preserved decisions

- **Priority:** P2
- **Target file:** new `plugins/anti-ai-craft/skills/anti-ai-design/references/design-review-template.md`
- **Instruction:** include a short section for effective elements, each supported
  by evidence and marked as an invariant for future remediation.
- **Reason:** a safe visual fix needs to know not only what to change but what must not regress.
- **Risk:** generic praise used as filler.
- **Acceptance:** each item cites a surface/evidence and explains the behavior or
  decision that must remain; an empty section is allowed when nothing was proven.

## Suggested implementation order

1. ADR-R01, ADR-R02, and ADR-R03 to establish permission, evidence, and coverage.
2. ADR-R04 and ADR-R05 to stabilize the report format.
3. ADR-R06, ADR-R07, and ADR-R08 to improve reproducibility and failure handling.
4. ADR-R09 to integrate review and remediation without automatic application.
5. ADR-R10 as a preservation refinement.

## Final criterion for this analysis

The best incorporation is not to make every review more rigid. It is to make each
conclusion proportionate to evidence, every surface traceable, every failure
explicit, and every edit dependent on authorization. The public names
`anti-ai-design`, `anti-ai-audit`, `anti-ai-remediate`, `anti-ai-code`, and
`anti-ai-security` must remain unchanged.
