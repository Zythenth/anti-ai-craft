# Analysis of the `frontend-design` unit

## Scope and method

This analysis compares the external `frontend-design/SKILL.md` unit in full with
the plugin's five current skills:

- `anti-ai-design`: `SKILL.md`, `agents/openai.yaml`, and six references;
- `anti-ai-code`: `SKILL.md`, `agents/openai.yaml`, and six references;
- `anti-ai-audit`: `SKILL.md`, `agents/openai.yaml`, and three references;
- `anti-ai-remediate`: `SKILL.md`, `agents/openai.yaml`, and three references;
- `anti-ai-security`: `SKILL.md`, `agents/openai.yaml`, and four references.

The plugin was not changed. The comparison considers the intent of each rule, not
textual similarity. The useful ideas below were reformulated to preserve the
current model: context before aesthetics, evidence before claims, editing only
when authorized, applicable accessibility, and no mandatory stack or style.

## Inventory of the external unit

The unit contains a single `SKILL.md`, with no supporting references or agent
configuration of its own. Its content is divided into:

1. examples of interface-creation requests;
2. project inspection before writing code;
3. understanding the problem, audience, tone, and constraints;
4. explicit selection of an aesthetic direction;
5. a catalog of eight visual philosophies with prescriptions for typography,
   color, composition, spacing, motion, and finish;
6. visual implementation guidance;
7. mandatory mobile-first rules;
8. dark-theme generation and motion reduction.

### Strengths

- Requires inspection of the project before generating components.
- Looks for existing components, tokens, themes, fonts, layout patterns, and dependencies.
- Prefers composing or extending components to duplication.
- Requires declaring a visual direction instead of impulsively mixing styles.
- Treats typography, color, layout, spacing, motion, and details as a coherent system.
- Calls attention to touch, reading width, compact navigation, contrast across themes, and reduced motion.

### Limitations

- Turns several contextual choices into universal rules.
- Mixes architectural discovery with assumptions about specific directories, frameworks, and libraries.
- The aesthetic catalog may become a preset selector and produce another form of homogenization.
- Prescribes font families, palettes, durations, effects, and navigation types without demonstrating a connection to the product or brand.
- Recommends remote font loading by default without considering project policy, privacy, CSP, availability, performance, or offline behavior.
- Declares mobile-first mandatory even when the task, audience, or predominant surface may require another strategy.
- Requires a dark theme even when there is no requirement, design system, or capacity to maintain two themes correctly.
- Validation is weaker than in the current plugin: it does not require real execution, comparable screenshots, extreme states, complete focus behavior, zoom, reflow, text spacing, a screen reader, or approval gates.
- Does not address action hierarchy or reflexive use of kebab/ellipsis menus.

## Assessment by area

### Preimplementation

The plugin already requires reading sources of truth; classifying the surface;
choosing a preserve/refine/redesign mandate; inventorying screens, routes,
components, states, and media; and defining acceptance criteria. The external unit
adds a useful operational list of places to look for components, tokens, themes,
stories, fonts, and dependencies.

The real gain is not fixing directory or framework names, but making preflight
verifiable: for the relevant scope, record the candidate component, public API,
states, token consumers, theme source, executable examples, and visual
dependencies. Requiring every component in a large repository to be listed would
be expensive and disproportionate.

### Reuse

The plugin already preserves local architecture, tokens, and components and
prohibits unnecessary dependencies, frameworks, or refactors. It needs only to
make explicit the choice to reuse, compose, extend, or create for directly
affected components.

This record reduces duplication and also counters a common anti-AI pattern:
generating a new button, card, modal, or token system because the model did not
look for an existing equivalent. It should be proportional to scope, not a census
of the entire repository.

### Responsiveness

The current plugin is safer: it uses adaptive compositions, content-determined
breakpoints, reflow at 320 CSS px, zoom, text spacing, long strings, orientation,
safe areas, the virtual keyboard, and absence of hover. The external requirement
to always begin at 375 px and use only growth-oriented media queries should not be
incorporated.

Two improvements are useful:

- on reading surfaces, validate line measure and rhythm in each relevant
  composition without turning a numerical range into a universal standard;
- in mobile forms, verify that focus does not cause zoom, clipping, or loss of
  context and that the primary action remains available with the virtual keyboard.

Touch targets should continue to follow the normative baseline and the larger
target established by the platform or product. A single number should not replace
context, spacing among targets, and applicable exceptions.

### Accessibility

Current coverage is substantially stronger. It includes applicable WCAG,
semantics, keyboard, focus, modals, tabs, menus, forms, live regions, contrast,
forced colors, reflow, zoom, text spacing, touch, motion, and a manual matrix.

From the external unit, only the reminder to validate reduced motion together
with the theme deserves operational reinforcement. Numerical rules or navigation
choices should not replace the existing baseline.

### Themes

This is the primary useful gap. The plugin tests light/dark and forced colors and
has a token chain, but does not define a complete theme contract.

When the product already provides or requires more than one theme, the workflow
should record:

- source of truth and token layers;
- themes and preferences actually supported;
- precedence among the system, product configuration, and manual choice;
- persistence and behavior before hydration;
- semantic roles for surfaces, text, borders, focus, and states;
- behavior of images, icons, native form controls, overlays, and shadows;
- contrast and readability in each state;
- relationship to forced colors and reduced motion.

The plugin should not generate a dark theme automatically. Adding a theme doubles
the maintenance surface and requires authorization when it expands identity or scope.

### Aesthetics

The current direction contract is already more robust because it begins with the
task, identity, content, state, and invariants. The external catalog can serve
only as an example that a direction must form a coherent system.

The adaptable improvement is to expand the direction contract to record, when relevant:

- typography;
- color roles;
- composition and grid;
- density and spacing;
- motion;
- surfaces and details;
- media and iconography.

Do not incorporate closed catalogs, mandatory fonts, ready-made palettes, fixed
timings, bans on popular families, or requirements for asymmetry, noise,
gradients, texture, or ornament. These prescriptions can replace one generic
default with another.

### Components

The plugin already has detailed coverage for tables, lists, forms, modals, tabs,
menus, search, tooltips, cards, and bento layouts. It also connects visual
structure to semantics, keyboard behavior, and states.

The external unit does not improve this set, but reinforces the need to locate
APIs and examples for existing components before creating another. This point
should enter preflight and reuse evidence.

#### Kebab and ellipsis menus

The external unit does not address action hierarchy. The current plugin behavior
should be preserved:

- kebab/ellipsis menus are not prohibited and do not indicate authorship;
- they serve two or more genuinely secondary, related, infrequent actions, or a
  demonstrated space constraint;
- a single action should be shown directly;
- primary or frequent actions remain visible;
- the control needs an accessible name, expanded state, keyboard support, focus,
  Escape behavior, and focus return;
- review should count occurrences and inspect real contents instead of accepting a
  repeated actions column by convention.

This contextual treatment is stronger than any aesthetic prohibition.

### Media

The current plugin is also stronger here: it preserves assets, slots, aspect
ratios, crops, alternative text, captions, loading state, and content integrity.
The external suggestion to create atmosphere with backgrounds, textures, and
gradients should not become a requirement.

A cross-cutting improvement is to prohibit automatic introduction of a remote
font, image, script, or stylesheet. When an external resource is genuinely
necessary, the decision should pass through applicable checks for local
architecture, project policy, origin, privacy, CSP, performance, cache, fallback,
integrity, and offline availability.

### Motion

The plugin already requires function, interruption, and a reduced alternative,
and rejects staggered motion, bounce, particles, hover lift, animated backgrounds,
and theatrical delay without reason.

It can become more verifiable by classifying each relevant motion as:

- state feedback;
- spatial relationship or transition;
- orientation;
- decorative or ambient.

Decorative or ambient motion should have justification, containment, and an
alternative. Do not incorporate libraries, curves, durations, or animation styles
as defaults.

### Validation

The current plugin requires real execution, screenshots, before/after comparison,
narrow/intermediate/wide viewports, extreme states, independent visual and
technical passes, lint, tests, build, and a human gate. The external unit contains
no sufficient equivalents.

Useful additions are:

- record the reuse decision for in-scope components;
- include a theme matrix when multiple themes exist;
- verify line measure on editorial surfaces;
- test field focus with a virtual keyboard and browser zoom behavior on applicable mobile browsers;
- record every new visual-resource origin as a dependency or boundary change.

## Coverage matrix

| Item assessed | State | Decision |
|---|---|---|
| Read the project before writing code | already present | Preserve the current workflow. |
| Identify existing components in scope | already present | Make reuse evidence more explicit. |
| Record candidate-component API, properties, events, and states | partial | Add only for components relevant to the request. |
| Examine tokens and real consumers | already present | The current chain is more complete. |
| Examine actual theme configuration | partial | Expand into a theme contract. |
| Look for stories, catalogs, or executable examples | absent | Include as an optional source of truth. |
| Examine font loading and fallback | partial | Fallback exists; explicit inventory and a remote-origin gate are missing. |
| Examine existing layout, containers, and breakpoints | already present | Preserve. |
| Examine existing visual dependencies | partial | Integrate into preflight and code/security checks. |
| Reuse, compose, or extend before duplicating | already present | Record the decision in the report. |
| Understand problem, audience, tone, and constraints | already present | Preserve. |
| Declare direction before code | already present | The current contract is more verifiable. |
| Translate direction into coherent visual axes | partial | Expand the contract without a fixed catalog. |
| Closed catalog of aesthetic philosophies | do not incorporate | May become a preset selector and import identity. |
| Specific fonts per philosophy | do not incorporate | Voice, language, license, performance, and the local system take precedence. |
| Ban popular font families by name | do not incorporate | Popularity alone does not demonstrate unsuitability. |
| Load remote fonts by default | do not incorporate | Creates dependency and privacy, CSP, availability, and performance risk. |
| Fixed formula of dominant color and strong accent | do not incorporate | Semantic roles and product identity take precedence. |
| Asymmetry, overlap, or broken grid by default | do not incorporate | Accept only when it benefits the task and content. |
| Atmospheric backgrounds and textures by default | do not incorporate | Do not replace hierarchy or real media with decoration. |
| Proportionality between visual ambition and complexity | partial | Adopt as a cost and maintenance gate, not as permission for volume. |
| Mandatory mobile-first at 375 px | do not incorporate | Strategy depends on audience, surface, and product. |
| Growth-oriented media queries as the only valid technique | do not incorporate | Preserve the project's CSS architecture and breakpoints. |
| One universal touch target | partial | Keep the normative baseline and platform/product target. |
| One universal mobile type size | do not incorporate | Test readability and zoom in the real context. |
| Mobile navigation limited to three patterns | do not incorporate | Choose based on the information model and platform. |
| Line measure verified per breakpoint | absent | Add for reading surfaces without a rigid universal range. |
| Mobile as a reprioritized composition | already present | Preserve; it is stronger than merely stacking. |
| Always generate a dark theme | do not incorporate | Requires a requirement, design system, scope, and maintenance. |
| Reuse existing theme tokens | already present | Reinforce source of truth and consumers. |
| Precedence between system preference and manual choice | absent | Add when the product supports both. |
| Avoid mechanical color inversion | partial | Formalize through semantic roles and states. |
| Contrast and reduced motion across themes | already present | Integrate into one validation matrix. |
| Motion tied to state and orientation | already present | Classify to simplify review. |
| Mandatory animation library by stack | do not incorporate | Reuse the existing stack and architecture. |
| Duration and easing prescribed by aesthetics | do not incorporate | Derive from function, platform, and user preference. |
| Media integrity, aspect ratio, crop, and loading | already present | Current coverage is stronger. |
| Real execution and comparable screenshots | already present | Current coverage is stronger. |
| Extreme states and recovery | already present | Current coverage is stronger. |
| Explicit evidence for reuse decisions | absent | Add to preflight and reporting. |
| Validation matrix by theme | partial | Consolidate themes, states, contrast, and motion. |

## Adapted recommendations

The instructions below describe new behavior in original language. They do not
require renaming skills, changing commands, changing invocation policy, or adding
dependencies.

### FD-01 — Proportionate reuse inventory

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Supporting file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instruction:** before creating a component, record only relevant candidates
  found in the design system, UI directories, stories, examples, or tests. For
  each candidate, note its public API, covered states, and a `reuse`, `compose`,
  `extend`, or `create` decision with a reason.
- **Reason:** reduces duplicate components and invented APIs without requiring a
  disproportionate scan of the entire repository.
- **Risk:** turning small tasks into excessive documentation.
- **Acceptance criterion:** every in-scope component creation has at least one
  recorded search and a reuse decision; when no candidate exists, the gap is stated.

### FD-02 — Direction profile by axes

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Supporting file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-principles.md`
- **Instruction:** expand the direction contract to record only relevant axes
  among typography, color, composition/grid, density/spacing, motion,
  surfaces/details, and media/iconography. Each choice must identify its connection
  to the task, domain, identity, or constraint.
- **Reason:** turns a “vibe” into coherent decisions without using a fixed aesthetic catalog.
- **Risk:** the contract may become long or be filled with vague adjectives.
- **Acceptance criterion:** every completed axis has a verifiable decision and
  rationale; inapplicable axes may be omitted; no font, palette, effect, or layout
  is chosen solely from the name of a style.

### FD-03 — Conditional theme contract

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Supporting file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/accessibility-baseline.md`
- **Instruction:** when more than one theme exists, record the source of truth,
  supported themes, precedence, persistence, prehydration state, semantic roles,
  assets, native controls, overlays, contrast, forced colors, and reduced motion.
  Do not create a new theme without a requirement or authorization.
- **Reason:** prevents mechanical inversion, flashes of the wrong theme, unreadable
  states, and duplicated values.
- **Risk:** expanding the scope of a localized visual fix.
- **Acceptance criterion:** every supported theme preserves hierarchy, states,
  focus, and contrast; manual choice and system preference have documented
  behavior; a new theme enters only with explicit authorization.

### FD-04 — Gate for external visual resources

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Supporting files:** `plugins/anti-ai-craft/skills/anti-ai-code/references/code-antipatterns.md` and `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`
- **Instruction:** before adding an external font, image, stylesheet, script, or
  visual library, look for an approved local alternative and verify applicable
  needs, origin, project policy, privacy, CSP, integrity, performance, cache,
  fallback, and degraded operation.
- **Reason:** an aesthetic decision must not silently introduce a network
  dependency, new trusted origin, or supply-chain risk.
- **Risk:** blocking a legitimate asset because information is missing.
- **Acceptance criterion:** every new visual origin or dependency has a recorded
  need and validations; relevant uncertainty becomes a pending decision, not an
  automatic installation.

### FD-05 — Mobile reading and form validation

- **Priority:** P2
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/accessibility-baseline.md`
- **Supporting file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instruction:** for reading surfaces, verify line measure, rhythm, and
  continuity in relevant viewports. For mobile forms, test focus, browser zoom,
  the virtual keyboard, safe area, clipping, and access to the primary action.
- **Reason:** covers real problems raised by the external unit without imposing a
  universal width, type size, or device.
- **Risk:** treating an editorial preference as a normative failure.
- **Acceptance criterion:** the report separates observed readability from a
  normative requirement and records browser, viewport, and state; no essential
  field or action becomes inaccessible during input.

### FD-06 — Theme validation matrix

- **Priority:** P2
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Supporting file:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md`
- **Instruction:** when multiple themes are in scope, cross theme with critical
  states and at least one narrow and one wide viewport; include focus, error,
  disabled, loading, overlays, media, forced colors, and reduced motion when applicable.
- **Reason:** “has dark mode” does not demonstrate that the theme works outside the ideal state.
- **Risk:** combinatorial explosion.
- **Acceptance criterion:** the matrix is proportional to risk, covers states that
  change semantics or contrast, and states which combinations were not tested.

### FD-07 — Functional classification of motion

- **Priority:** P2
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-principles.md`
- **Supporting file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instruction:** classify relevant motion as feedback, spatial transition,
  orientation, or decoration/ambience. Require an observable function for the
  first three and justification, containment, and an alternative for the last.
- **Reason:** makes it easier to distinguish useful motion from reflexively scattered microinteractions.
- **Risk:** adding bureaucracy to trivial transitions.
- **Acceptance criterion:** material motion has a category and reduced-motion
  behavior; removed animations cannot hide content or state.

### FD-08 — Reuse evidence in audits

- **Priority:** P2
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md`
- **Instruction:** when reporting visual duplication or a generic component, first
  verify the existing component, its API, reach, and limitations. Do not declare
  duplication based on appearance alone.
- **Reason:** connects the preimplementation inventory to the audit's evidence standard.
- **Risk:** a similar component may have an incompatible contract.
- **Acceptance criterion:** the finding identifies a real reuse candidate and
  demonstrates compatibility or explains why extension/composition is viable.

## Decisions not to incorporate

Do not incorporate:

- an aesthetic catalog as a mandatory menu;
- rigid associations between aesthetics and fonts, colors, shapes, grids, or animations;
- bans on fonts, gradients, shadows, symmetry, cards, or dark mode based on appearance alone;
- requirements for asymmetry, overlap, noise, texture, or “boldness”;
- automatic generation of a dark theme;
- remote font loading by default;
- universal mobile-first, a single initial viewport, or a single CSS technique;
- type size, touch target, line measure, duration, or easing as universal numbers;
- hamburger, bottom tabs, or a drawer as the only mobile solutions;
- greater complexity merely to signal authorship or creativity.

These items conflict with the plugin's mission: preventing a recipe from
replacing the task, evidence, identity, and real constraints.

## Compatibility

The recommendations preserve:

- the five skill names and their invocation methods;
- descriptions and explicit-invocation policy;
- separation among design, code, audit, remediation, and security;
- read-only audits;
- remediation limited to approved findings;
- prohibition on a new stack, dependency, identity, or theme without need and authorization;
- the contextual rule for kebab/ellipsis menus;
- the existing accessibility and validation baseline.

No recommendation requires changing the manifest, public structure, file name,
installation command, or plugin API.

## Summary

The external unit confirms that prior inspection, reuse, and explicit visual
direction matter, but the current plugin already implements them with stronger
evidence, accessibility, and security. The best improvements are operational: a
proportionate inventory of components and APIs, a direction profile by axes, a
conditional theme contract, a gate for external resources, mobile reading/form
validation, a theme matrix, and reuse evidence.

The aesthetic catalog and universal rules for fonts, color, layout, mobile,
themes, and motion should not be incorporated. They could recreate exactly the
anti-AI behavior the plugin seeks to avoid: choosing a ready-made visual recipe
before understanding the product.
