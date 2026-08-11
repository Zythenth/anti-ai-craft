# Analysis of the `design-tokens` unit

## Scope and method

This analysis compares the external `design-tokens` unit in full with the plugin's
five current skills. The objective is to identify coverage, gaps, and adaptable
improvements without copying text, imposing a stack, creating automatic
aesthetics, or breaking names and compatibility.

No plugin file was changed. This document is the only artifact produced by this analysis.

### Inventory examined

| Unit | Files examined in full |
|---|---|
| External unit | `design-tokens/SKILL.md` |
| `anti-ai-design` | `SKILL.md`, `agents/openai.yaml`, `references/accessibility-baseline.md`, `references/design-antipatterns.md`, `references/design-principles.md`, `references/direction-contract.md`, `references/review-workflow.md`, `references/sources.md` |
| `anti-ai-code` | `SKILL.md`, `agents/openai.yaml`, `references/architecture-antipatterns.md`, `references/code-antipatterns.md`, `references/debugging-and-evidence.md`, `references/review-workflow.md`, `references/sources.md`, `references/testing-antipatterns.md` |
| `anti-ai-audit` | `SKILL.md`, `agents/openai.yaml`, `references/audit-checklist.md`, `references/report-template.md`, `references/severity-model.md` |
| `anti-ai-remediate` | `SKILL.md`, `agents/openai.yaml`, `references/approval-gates.md`, `references/remediation-protocol.md`, `references/validation-checklist.md` |
| `anti-ai-security` | `SKILL.md`, `agents/openai.yaml`, `references/remediation-workflow.md`, `references/security-checklist.md`, `references/sources.md`, `references/validation-and-severity.md` |

## Inventory of the external proposal

The external unit focuses on creating or completing a project's visual
foundation. Its ideas can be grouped into eight blocks:

1. discover variables, framework configuration, theme providers, token files, and UI dependencies;
2. extend an existing system instead of replacing it;
3. read a visual brief before choosing values;
4. choose the output format according to the stack;
5. organize color, typography, spacing, layout, shape, elevation, motion, and breakpoints;
6. produce light and dark variants;
7. make components consume tokens instead of loose values;
8. save the outcome in the appropriate location and explain decisions.

Its primary value lies in the operational discovery process and breadth of the
inventory. The parts that should not be imported literally are the mandatory
defaults: a dark theme in every project, predetermined numerical scales,
device-class breakpoints, selection of a brief by modification date, dependency
on another aesthetic unit, and automatic selection of CSS when the architecture
is uncertain.

## What the plugin already has

### `anti-ai-design`

This skill has the greatest coverage. It already:

- reads the design system, tokens, components, code, assets, and local rules before proposing aesthetics;
- establishes a mandate to preserve, refine, or redesign;
- organizes tokens as `primitive → semantic → component`;
- requires real consumers and identifies values that bypass the chain;
- covers color and typography roles, states, contrast, themes, and forced colors;
- chooses responsiveness based on content breakage, not fixed devices;
- preserves architecture, identity, content, and media;
- rejects universal numbers for colors, fonts, animations, and stacks;
- validates the real interface, states, viewports, and accessibility.

The gap is not conceptual. What is missing is a specific procedure for token
requests: where to look, how to select the authoritative source, how to
distinguish source from a generated file, how to record aliases and consumers,
which families to examine, and which output to produce.

### `anti-ai-code`

It already detects magic values, inline styles that bypass the architecture,
excessive configuration, speculative compatibility, and abstractions without a
consumer. It also requires preservation of the stack and verification through
builds, tests, and execution.

What is missing is explicit token-specific failure coverage: a missing or circular
alias, editing a generated artifact, consumption of a primitive value where the
project requires semantics, manual theme branches that duplicate policy, orphaned
tokens, and bulk replacement without confirming the value's function.

### `anti-ai-audit`

It already audits roles for typography, color, shadow, borders, radius, icons, and
motion, and loads the design principles directly. Its evidence and falsification
discipline prevents visual preferences from becoming defects.

What is missing is a token-specific auditable path: authoritative source, layers,
aliases, consumers, hardcodes, modes, states, generated files, and observable
effect. Current coverage is high-level and can be completed without examining the
implementation of the token system.

### `anti-ai-remediate`

It already preserves the design system, identity, architecture, and preexisting
work; requires before/after comparison and viewport validation; and requires
approval for broad visual change.

What is missing is guidance for token fixes: change the authoritative source,
regenerate outputs with the official command, limit replacements to demonstrated
consumers, validate every affected mode, and treat a global token change as
potentially broad even when the diff is small.

### `anti-ai-security`

Static design tokens do not belong to this skill's core. Current coverage of
untrusted input, sinks, configuration, and external content is sufficient for most
projects.

There is only one conditional extension: when themes or tokens are accepted from a
user, tenant, CMS, remote file, or integration, they cross a trust boundary. In
that case, names, types, values, resource references, and the application
mechanism require validation. Without controllable external input and a relevant
sink, this should not produce a security finding.

## Analysis by dimension

### Hierarchy and lifecycle

The plugin already has the correct hierarchy and requirement for real consumers.
The needed improvement is to operationalize the lifecycle:

1. locate the authoritative source;
2. identify derived files and the command that generates them;
3. resolve aliases and dependencies;
4. map tokens to consumers and states;
5. change the lowest layer capable of expressing the intent;
6. regenerate, validate, and review the diff;
7. remove only orphans created by the change or demonstrated to have no consumers.

A complete taxonomy on paper is insufficient. The following should also be
treated as failures: an unresolved alias, a cycle, an incompatible type, a unit
invalid for the consumer, divergence between source and generated output, a token
declared without a consumer, and a consumer that ignores the established semantic
layer.

### Themes and modes

The plugin already tests light/dark and forced colors when present, but correctly
does not require dark mode in every product. The adapted rule should be:

- preserve the adopted theme mechanism;
- generate only modes required by the product or already supported;
- maintain semantic and state parity among existing modes;
- respect system preference and manual choice only if that contract already exists or is requested;
- do not simultaneously introduce competing selectors, providers, and media queries;
- treat theme, brand, high contrast, and density as independent axes when the project actually models them.

The validation point is not “there are two palettes,” but “each semantic role
remains readable, distinguishable, and functional in every supported mode.”

### Typography

The plugin already selects families based on voice, reading, languages,
performance, and function. It should additionally request an inventory of
typographic tokens and verify:

- family, fallback, and availability;
- text roles rather than an arbitrary collection of sizes;
- size, weight, line height, and tracking as a set;
- readability with zoom, text spacing, translation, long strings, and supported scripts;
- distinction among reading text, display text, data, and code;
- actual consumption by components.

There should be no mandatory number of families, steps, or weights. The scale
should extend the local system or be derived from content and required roles.

### Color

The plugin already requires a semantic or identity role, contrast, and
communication beyond color. The improvement is to make the minimum applicable map explicit:

- surfaces and backgrounds;
- text and icons;
- borders and separators;
- actions and focus;
- interaction states;
- success, warning, error, and information;
- overlays and elevation when present.

This map is a checklist, not a requirement to create every token. Missing states
are a gap only when a corresponding consumer or contract exists. Names should
express intent; value-based names may remain in the primitive layer, not in the
semantic API.

### Spacing, dimensions, shape, and elevation

Spacing is the largest direct gap. The plugin discusses rhythm, grouping, density,
targets, and radius, but does not describe how to audit or create the scale.

The adapted rule should:

- discover and extend the existing scale;
- derive steps from real grouping, density, touch, and layout needs;
- avoid near-duplicates without a function;
- allow justified local exceptions;
- not replace intrinsic dimensions, media proportions, or layout calculations with artificial tokens;
- connect radius and shadow to shape, state, or elevation, not generic finish.

A fixed base and universal multipliers should not be incorporated.

### Motion

The plugin already has the correct functional guidance and reduced-motion
behavior. It can improve by distinguishing:

- duration;
- curve;
- delay;
- distance or intensity;
- reduced variant;
- consumer and state transition.

Only repeated values that represent a transition language are worth tokenizing.
Do not create a complete scale for one animation, adopt bounce as a default, or
turn duration into a universal rule. Validation should confirm interruption, final
state, absence of theatrical delay, and a reduced alternative.

### Breakpoints and layout

The plugin's current approach is stronger than the external proposal: breakpoints
should emerge when content, interaction, reading, or navigation stops working.
They should not be named after rigid devices or receive universal values.

Breakpoints may be part of the system when the stack treats them as shared
configuration, but they should not be forced into the same format as color or
spacing. Output should respect stack capabilities; for example, a token source
should not promise consumption in a context where that variable type is not resolved.

### Formats and outputs

The plugin preserves architecture but offers no operational token map. The
improvement should identify, without imposing:

- variables and style layers;
- framework configuration;
- theme objects;
- structured token files;
- native platform resources;
- generated files and transformation tools.

When a pipeline exists, edit only the source and run the official generator. When
there is more than one source, resolve authority through documentation, imports,
scripts, and consumers; do not choose by file name. If the architecture remains
ambiguous, request a decision instead of creating a new `tokens.css`.

The ideal output includes:

- inventory and authoritative source;
- applicable modes and families;
- tokens preserved, added, changed, and rejected;
- affected consumers;
- source file and regenerated files;
- commands and validations;
- deviations and pending decisions.

### Detection of the existing system

External detection is useful but should be expanded and made independent of
specific names. Look for:

- definitions, imports, and consumers of variables;
- stack configuration and dependencies;
- theme providers, contexts, attributes, and preferences;
- structured files and generation scripts;
- native resources and component libraries;
- repeated or hardcoded values;
- aliases, references, and generated outputs;
- visual tests, documentation, and design tools;
- multiple brands, themes, or platforms.

Classify the outcome as:

- nonexistent;
- informal, with repeated values;
- partial, with some semantics or generation;
- established, with a source, layers, and consumers;
- fragmented, with competing sources.

This classification determines whether the correct action is to create, extend,
consolidate, connect consumers, or merely document.

## Coverage and decision matrix

| Idea assessed | State | Current situation and decision |
|---|---|---|
| Read the design system, tokens, code, and components before acting | Already present | Covered in design preparation and preservation rules. |
| Extend an existing system instead of replacing it | Already present | Covered by the preserve/refine mandate and visual workflow. |
| `primitive → semantic → component` hierarchy | Already present | Explicit in the principles and direction contract. |
| Require real consumers and detect bypass of the semantic layer | Already present | Explicit, though it could gain operational checks. |
| Preserve stack, identity, and architecture | Already present | Covered across the five skills according to mode. |
| Semantic roles for color and typography | Already present | Strong conceptual coverage; a family-based token inventory is missing. |
| Contrast, states, forced colors, and reduced motion | Already present | Covered in design and accessibility. |
| Breakpoints derived from content breakage | Already present | The current rule is preferable to device presets. |
| Detect formats, providers, structured files, and dependencies | Partial | General project reading exists, but not a specific, verifiable procedure. |
| Distinguish authoritative source from generated artifact | Absent | Should be included to avoid editing the wrong file. |
| Resolve aliases, cycles, types, and units | Absent | This technical token failure is not yet in the checklist. |
| Map tokens to consumers, states, and modes | Partial | Consumers and states exist, but without an inventory format. |
| Role-based typographic scale | Partial | Family and readability criteria exist; scale and joint validation do not. |
| Contextual spacing scale | Absent | Rhythm and density exist, but not scale creation/audit. |
| Shape, elevation, and layout tokens | Partial | Roles are discussed, but not the tokenization process. |
| Duration, curve, and reduced-variant tokens | Partial | Functional motion is covered; a value system is not. |
| Parity among already supported themes or modes | Partial | Theme tests exist, but not a token × mode × state matrix. |
| Output compatible with the stack and pipeline | Partial | Preservation exists; format mapping and official generation do not. |
| Report of preserved, changed, and rejected tokens | Partial | The general output contract covers decisions, not a dedicated inventory. |
| Audit hardcodes, orphans, and generation divergence | Absent | Should be added with a requirement for impact and a real consumer. |
| Fix at the authoritative source and regenerate officially | Absent | Missing from the remediation protocol. |
| Mandatory light and dark themes in every project | Do not incorporate | Imposes product, maintenance, and aesthetics without a requirement. |
| Fixed spacing, typography, motion, or breakpoint values | Do not incorporate | Numbers should come from the system, content, capability, and accessibility. |
| Choose the brief by most recently modified file | Do not incorporate | File date establishes neither authority nor intent. |
| Delegate visual philosophy to another mandatory unit | Do not incorporate | Creates coupling and may replace project direction. |
| Create CSS by default when the stack is uncertain | Do not incorporate | Uncertainty should be resolved through evidence or a user decision. |
| Apply system preference and a manual selector simultaneously | Do not incorporate by default | Adopt only when the theme contract and architecture require both. |
| Turn every visual value into a token | Do not incorporate | Unique, intrinsic, or calculated values may remain local when justified. |
| New skill or renaming the five skills | Do not incorporate | The content fits existing skills and names must remain compatible. |

## Adapted recommendations

### DT-01 — Central design-token procedure

- **Priority:** P0
- **Target file:** new `plugins/anti-ai-craft/skills/anti-ai-design/references/design-tokens.md`
- **Instruction:** create an operational reference covering discovery, system
  classification, authoritative source, generated files, hierarchy, aliases,
  applicable families, modes, consumers, minimum implementation, validation, and
  output contract. Every numerical rule must be derived from the project or
  marked as a pending decision.
- **Reason:** concentrates the gaps without inflating `SKILL.md` or duplicating general principles.
- **Risk:** becoming a mandatory catalog or competing with the local design system.
- **Acceptance:** the reference distinguishes creating, extending, consolidating,
  and merely connecting consumers; prohibits replacing a format/namespace without
  authorization; does not require dark mode, a stack, a number of steps, or fixed
  values; and records the source and generated outputs.

### DT-02 — Explicit routing for token requests

- **Priority:** P0
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Instruction:** add the new document to the references section and include in
  the workflow a short branch for requests involving tokens, themes, palettes,
  scales, or a design system. The branch should first detect the existing system
  and only then propose values or files.
- **Reason:** the skill is already the correct entry point, but today a request may
  follow a generic visual flow.
- **Risk:** burdening every interface review with a complete token audit.
- **Acceptance:** the reference is read only when the request or problem involves
  tokens; the `$anti-ai-design` name, invocation policy, and default prompt remain compatible.

### DT-03 — Verifiable audit of the token system

- **Priority:** P0
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md`
- **Instruction:** add conditional items to identify the authoritative source,
  generated outputs, layers, aliases, consumers, values that bypass the system,
  parity among modes/states, and divergence between definition and runtime.
- **Reason:** turns broad visual coverage into reproducible technical evidence.
- **Risk:** promoting taxonomic purity to a finding without impact.
- **Acceptance:** a finding requires a reachable consumer and observable harm,
  violated contract, or concrete risk; an isolated, justified local value is not a
  failure; inapplicable areas are marked accordingly.

### DT-04 — Contextual token families

- **Priority:** P1
- **Target file:** new `plugins/anti-ai-craft/skills/anti-ai-design/references/design-tokens.md`
- **Instruction:** describe color, typography, spacing, dimensions, shape,
  elevation, motion, and layout as optional families. For each family, require
  intent, naming, type/unit, consumers, states, modes, and validation. Scales
  should extend the project or emerge from content and function.
- **Reason:** uses the breadth of the external proposal without importing presets.
- **Risk:** creating tokens without consumers or excessive granularity.
- **Acceptance:** every new token has at least one intended consumer and an intent;
  justified local exceptions are permitted; there is no mandatory universal list.

### DT-05 — Visual and technical token validation

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instruction:** in the technical pass, verify alias resolution, source versus
  output, representative consumers, states, and every supported mode. In the
  visual pass, compare the same data and components before/after, including
  contrast, zoom, long strings, and reduced motion when affected.
- **Reason:** a successful build does not prove visual consistency, and an isolated
  screenshot does not prove system integrity.
- **Risk:** overexpanding validation for a localized change.
- **Acceptance:** the test matrix is proportional to changed tokens; a global
  color change checks affected combinations and states, while a local token checks
  only reachable consumers.

### DT-06 — Technical token antipatterns

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-code/references/code-antipatterns.md`
- **Instruction:** add, at the UI intersection, broken/circular aliases, manual
  editing of generated output, hardcodes that bypass an existing contract,
  duplicated theme branches, tokens without consumers, and textual replacement of
  values without confirming semantics.
- **Reason:** these defects appear as code and may escape a purely visual review.
- **Risk:** flagging every style literal as an error.
- **Acceptance:** each candidate is evaluated against source of truth, consumer,
  repetition, and effect; intrinsic, calculated, media, or third-party values may
  remain with justification.

### DT-07 — Remediate at the source and according to actual reach

- **Priority:** P1
- **Target files:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/remediation-protocol.md` and `plugins/anti-ai-craft/skills/anti-ai-remediate/references/validation-checklist.md`
- **Instruction:** direct edits to the authoritative source, regeneration with the
  official command, and consumer verification. Require a reach inventory before
  changing a shared token and comparison of affected modes/states.
- **Reason:** one line in a global token can change many screens and brands.
- **Risk:** a small diff causing a broad visual regression or overwriting generated output.
- **Acceptance:** the handoff reports the edited source, regenerated files,
  examined consumers, commands, before/after evidence, and tested modes; there is
  no bulk replacement without a usage map.

### DT-08 — Gate for global token changes

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md`
- **Instruction:** treat a change to a global token, namespace, provider,
  pipeline, or theme strategy as materially broad when it reaches multiple
  surfaces, even if it involves few files.
- **Reason:** diff size does not represent visual reach.
- **Risk:** requesting approval for local fixes without broad impact.
- **Acceptance:** the gate uses the number and criticality of consumers, brands,
  modes, and platforms; a local alias with demonstrably limited reach does not
  require new approval.

### DT-09 — Optional evidence in the audit report

- **Priority:** P2
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
- **Instruction:** include an optional token-system table with source, layer,
  token/alias, consumers, modes/states, evidence, and disposition.
- **Reason:** simplifies deduplication and the transfer of findings to remediation.
- **Risk:** making the template mandatory and noisy for repositories without UI.
- **Acceptance:** the section is used only when tokens are in scope and may be
  omitted without leaving empty fields.

### DT-10 — Dynamic themes as untrusted input

- **Priority:** P2, conditional
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`
- **Instruction:** add a short input/output check only for tokens or themes
  supplied by a user, tenant, CMS, or integration. Validate an allowlist of names,
  value types and ranges, resource references, and application to the correct sink.
- **Reason:** a configurable visual system may become active-content input or
  trigger external resource consumption.
- **Risk:** conflating visual quality with security and creating false positives for static tokens.
- **Acceptance:** no finding is created without controllable input, a reachable
  path, a missing control, and impact; local build-time tokens remain outside this check.

## Recommended incorporation order

1. Create the central token reference and route it through `anti-ai-design`.
2. Enable audits to inventory sources, aliases, consumers, and modes.
3. Add technical failures to `anti-ai-code`.
4. Protect fixes with the authoritative source, regeneration, and a reach gate.
5. Add the security check only as a conditional branch for external themes.
6. Validate all five skills and review whether any mandatory numbers, stacks,
   themes, or files were introduced.

## Global completion criteria

- The five skill names, directories, and invocation policy remain unchanged.
- No sixth skill is created for tokens.
- The existing system is detected and classified before any generation.
- The authoritative source and generated outputs are distinguished.
- Layers, aliases, consumers, modes, and states can be audited.
- Typography, color, spacing, and motion are defined by roles and context, not universal presets.
- Dark mode is created only when requested or required by the product.
- Breakpoints remain derived from content and behavior.
- Global changes receive validation and approval proportionate to reach.
- Security applies only when there is a real trust boundary.
- The final report records what was preserved, changed, rejected, validated, and not tested.

## Final summary

The external unit adds value primarily as a discovery checklist and an inventory
of token families. The current plugin already has a more mature conceptual
foundation: an explicit hierarchy, real consumers, contextual direction,
accessibility, preservation, and rejection of absolutes.

The recommended incorporation is not to copy a ready-made scale. It is to create
an operational procedure within `anti-ai-design`, reflect that procedure in audit,
code, and remediation, and keep security conditional on external themes. This
improves the five skills without imposing dark mode, a stack, aesthetics, fixed
values, or an incompatible new skill.
