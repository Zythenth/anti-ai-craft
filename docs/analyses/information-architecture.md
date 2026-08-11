# Analysis of the `information-architecture` unit

## Executive summary

The external unit treats information architecture as the structural layer between
product definition and visual design. The material is useful mainly because it
makes explicit the surface map, navigation model, content hierarchy, flows,
vocabulary, structural reuse, content growth, and URL rules.

The current plugin already covers a substantial part of this discipline,
especially in `anti-ai-design`: it requires reading the project, inventorying
screens and routes, identifying users and tasks, preserving existing navigation,
defining state contracts, prioritizing responsively, and validating in the real
product. `anti-ai-audit`, `anti-ai-remediate`, `anti-ai-code`, and
`anti-ai-security` complement that foundation with evidence, change control,
persistence, and trust boundaries.

The gap does not justify a sixth skill. The recommendation is to add a concise
information-architecture reference to `anti-ai-design` and propagate only the
necessary controls to the other four skills. This preserves the five public
identifiers, visible names, and explicit-invocation behavior.

## Inventory of what was analyzed

### External unit

| Area | What the unit intends to produce or decide |
|---|---|
| Point in the work | Product structure before visual detail and task decomposition |
| Product input | Brief, audience, objective, and existing structure |
| Repository discovery | Routes, navigation components, layouts, pages, URL patterns, and the content/data layer |
| Human decisions | Priority tasks, acceptable depth, content growth, distinct audiences, and predominant surface |
| Map | Tree of pages or views with their paths |
| Navigation | Primary destinations, local navigation, utilities, and mobile adaptation |
| Hierarchy | Content order and rationale per page |
| Flows | Critical paths with branches and destinations |
| Language | Consistent vocabulary for concepts and actions |
| Reuse | Shared layouts, containers, and structural elements |
| Growth | Search, filters, pagination, archive, and future expansion |
| URL | Segments, parameters, and construction conventions |
| Artifact persistence | Structural document saved alongside the brief |

### Current plugin coverage

| Skill | Related coverage |
|---|---|
| `anti-ai-design` | Users, tasks, screens, routes, content, states, flows, hierarchy, navigation, responsiveness, action names, URL as state, focus return, and structural preservation |
| `anti-ai-code` | Inputs, transformations, effects, persistence, outputs, APIs, states, concurrency, idempotency, integration, and preservation of local architecture |
| `anti-ai-audit` | Scope, users, tasks, data, states, surfaces, requirement coverage, path-based evidence, and candidate closure |
| `anti-ai-remediate` | Changes by approved ID, preservation of behavior and architecture, approval gates, regression, rollback, and before/after comparison |
| `anti-ai-security` | Surfaces, endpoints, roles, tenants, boundaries, alternative routes, controllable URLs, cache, storage, queues, sessions, authorization, and out-of-order flows |

## Adapted input and output model

### Minimum inputs

1. Objective of the product or change.
2. Audience and tasks that actually need to be completed.
3. Authorized scope: plan, review, or implement.
4. Existing sources of truth.
5. Routes, layouts, navigation, content models, and persistence already implemented.
6. Relevant authentication, authorization, tenant, and availability states.
7. Compatibility, accessibility, SEO, analytics, and platform constraints.

A brief at a fixed path should not be required. When one exists, it should be
treated as one source of truth among others. When none exists, the analysis may
start from the request, README, specification, and code. Questions are necessary
only when the answer would materially change the structure.

### Output proportional to scope

A complete analysis may contain:

- surface map;
- navigation model;
- hierarchy by surface;
- primary, alternative, and recovery flows;
- URL strategy;
- interface-state persistence model;
- vocabulary of concepts and actions;
- structural reuse map;
- content-growth plan;
- edge cases and terminal states;
- preserved, changed, and rejected decisions;
- acceptance criteria and validation plan.

A local change does not need an extensive document. In that case, it is enough to
record the affected structure, invariants, flow, persistence, and criteria that
prevent regression.

### Artifact destination

Do not establish `INFORMATION_ARCHITECTURE.md` or a single directory as a
universal rule. Respect the project's convention. If the user requests only
planning in the conversation, do not create a file. If persistence is authorized
and no convention exists, suggest a predictable path such as
`docs/architecture/information-architecture.md` before writing.

## Required maps

### Surface map

The map should include only reachable or planned surfaces with a verifiable basis:

- pages and views;
- persistent layouts;
- overlays that represent real steps;
- public, authenticated, administrative, and internal routes;
- alternative entry through a direct link, notification, search, invitation, or resumption;
- states in which a resource is nonexistent, removed, inaccessible, or unavailable;
- relevant variations by role, tenant, language, or version.

Each item should record the following when applicable:

| Field | Control question |
|---|---|
| Identity | What is the stable name of the surface? |
| Path | How is it reached in the product and by direct link? |
| Audience | Who can see it, and in which state? |
| Task | What can the person complete there? |
| Content | Which source feeds the surface? |
| State | Which states change the structure or available action? |
| Exit | Where does the person proceed, return, or recover? |
| Persistence | What survives refresh, return, or a new session? |

The map should not blindly mirror the file tree. One route may contain multiple
functional surfaces, and multiple routes may share a single structure.

### Navigation map

The model should distinguish:

- **global:** recurring destinations across areas;
- **local:** options within the current context;
- **contextual:** links and actions that depend on the object or state;
- **utility:** account, help, preferences, and administrative operations;
- **return and location:** breadcrumbs, history, “back,” and origin trail;
- **mobile/adaptive:** equivalent access with priority appropriate to space and task.

Do not impose a fixed number of items, sidebar, top bar, hamburger, or tabs. The
choice should respond to frequency, hierarchy, volume, user role, and need for
comparison. Mobile navigation must not simply hide destinations without
demonstrating that they remain discoverable and operable.

### Content map

For each primary surface, order:

1. information needed to recognize the context;
2. the dominant action or decision;
3. data supporting the decision;
4. secondary actions;
5. progressive details;
6. help and recovery.

The order should vary by task and state. Loading, error, empty, permission-denied,
or removed-resource states are not merely messages: they may replace the hierarchy
and next step.

### Reuse map

Record shared layouts and patterns only when real reuse exists. For each element:

- consuming surfaces;
- shared behavior;
- legitimate variations;
- state and responsibility;
- coupling boundaries.

The map should not prompt abstraction creation. It describes demonstrated reuse
and helps detect divergence; it does not require extracting a component.

## Navigation, URLs, and compatibility

### URL rules

A complete strategy should decide, according to the product:

- static and dynamic segments;
- identifier versus readable slug;
- filters, sorting, pagination, tabs, and searches that must survive in the address;
- fragments for location within content;
- locale, version, workspace, or tenant when part of the contract;
- canonical URL and existing aliases;
- encoding, case, separators, and trailing slash according to local convention;
- behavior of old links, redirects, and removed resources;
- pages that can be opened directly and restore context;
- data that must never appear in the URL because it is sensitive.

Do not require the URL to reproduce the visual hierarchy. A URL is a contract for
location, sharing, history, and integration; its form should remain stable even
when visual navigation changes.

### Compatibility that must be preserved

- public identifiers of the five skills;
- visible names and explicit invocation;
- existing routes, slugs, anchors, and links unless a migration is approved;
- valid deep links and bookmarks;
- back/forward and refresh behavior;
- parameters used by analytics, integrations, SEO, or support;
- authorization and isolation associated with each route;
- preexisting state the user expects to recover.

A change to URLs or primary navigation should be considered material, not visual polish.

## Flows

### Minimum flow structure

Each relevant flow should declare:

1. actor and initial state;
2. entry point;
3. objective;
4. sequence of surfaces and actions;
5. decisions and conditions;
6. data read or written;
7. URL and history changes;
8. failures and recovery;
9. terminal state;
10. later return or resumption.

### Flow families

| Family | Control examples |
|---|---|
| Primary | The most frequent or valuable task completes without unnecessary detours |
| Alternative | Another role, origin, or content type reaches the correct outcome |
| Recovery | Error, timeout, offline state, or invalid input preserves context and the next step |
| Authentication | Login, expiration, and return to the destination do not break the flow |
| Authorization | Missing permission does not leak content and offers a coherent destination |
| Interruption | Refresh, back, close, device change, or resumption preserves what is necessary |
| Growth | Search, filters, pagination, and archives remain useful at high volume |
| Administrative | Creation, editing, revocation, deletion, and audit use their own routes and states |
| Lifecycle | Onboarding, recurring use, offboarding, and data removal remain coherent |

The “primary path” should not erase recovery and abuse paths. The interface flow,
data flow, and authorization flow need to be compared.

## Required edge cases when applicable

### Content and volume

- no items, one item, and many items;
- long text, expanding languages, and special characters;
- unstable ordering or duplicate results;
- a requested page after the set has shrunk;
- an item removed between listing and detail;
- partial or stale content;
- no search results and unavailable search.

### Identity and access

- unauthenticated person;
- session expires during the flow;
- insufficient role;
- object belonging to another user or tenant;
- expired invitation;
- deactivated account;
- access through an old or shared link.

### Navigation and device

- direct entry with no prior history;
- back/forward after a mutation;
- refresh at an intermediate step;
- multiple tabs with divergent states;
- narrow viewport, virtual keyboard, and no hover;
- focus restored after closing an overlay or returning;
- orientation, safe area, and zoom.

### Operation and persistence

- a slow, canceled, repeated, or out-of-order request;
- double submission;
- rejected optimistic update;
- partial write;
- edit conflict;
- retry after timeout;
- stale cache;
- offline state and reconnection;
- a reached limit, quota, or rate limit.

## State persistence

Before implementing a flow, classify each state:

| Type | Examples | Rule |
|---|---|---|
| Authoritative on the server | resource, permission, confirmed progress | Refetch and invalidate coherently |
| Represented in the URL | search, filter, sorting, page, shareable tab | Support direct links, refresh, and history |
| Navigation session | origin, scroll, temporary step | Preserve when return is part of the task |
| Local to the device | nonsensitive, noncritical preference | Do not confuse with a source of truth |
| Ephemeral component state | open menu, hover, animation | Do not persist without need |
| Draft | long form or incomplete creation | Define lifetime, conflict, cleanup, and privacy |

For every persisted state, record:

- source of truth;
- key and scope by user/tenant;
- lifetime and expiration;
- serialization and version;
- invalidation;
- conflict across tabs or devices;
- behavior on logout, revocation, and deletion;
- sensitivity and exposure;
- observable fallback when restoration fails.

Filters and pagination should not be kept only in memory for convenience if the
product requires sharing or return. Secrets, tokens, and sensitive data should not
move to URLs or client storage merely to simplify implementation.

## Coverage matrix

| Capability | State | Current evidence or gap | Decision |
|---|---|---|---|
| Read existing structure before proposing | Already present | Preparation and workflow in `anti-ai-design`, `anti-ai-code`, `anti-ai-audit`, and `anti-ai-security` | Preserve |
| Inventory screens, routes, components, and flows | Already present | `anti-ai-design` requires the inventory | Preserve and detail |
| Identify users, tasks, data, and states | Already present | Contract shared by design and audit | Preserve |
| Preserve existing navigation and routes | Already present | Preserve/refine/redesign mandate and direction contract | Preserve |
| Represent filters, tabs, or pages in the URL when needed | Already present | Direction production checklist | Preserve |
| Recognition rather than recall | Already present | Principles, content, and review pass | Preserve |
| Consistent terms and action names | Already present | Principles and content pass | Preserve |
| Explicit global/local/contextual/utility navigation model | Partial | Components are evaluated, but the model is not requested as an artifact | Incorporate |
| Hierarchical surface map with routes | Partial | An inventory exists without defined fields or coverage | Incorporate proportionately |
| Content hierarchy by surface | Partial | Hierarchy is required but not systematically connected to each screen/state | Incorporate |
| Flows with decisions, failures, and resumption | Partial | Primary paths and states exist, but there is no complete format | Incorporate |
| URL conventions | Partial | Preservation and some URL state exist without a comprehensive strategy | Incorporate |
| Deep link, refresh, back, and forward | Partial | Return and preservation appear, but not as a flow matrix | Incorporate |
| Persistence by state type | Partial | Code covers persistence; design does not classify interface state | Incorporate |
| Content growth | Partial | Search, pagination, filters, and extreme data appear separately | Incorporate |
| Structural reuse map | Partial | Local components and patterns are preserved without a consumer inventory | Incorporate with protection against premature abstraction |
| Edge cases for removed resources, old links, and tab conflicts | Not explicit | General states exist, but these cases are not systematic | Incorporate |
| Navigation and URL migration | Not explicit | A human gate exists for navigation, but not redirects, aliases, or deprecation | Incorporate |
| IA coverage in the audit report | Absent | The template has no dedicated structural section | Incorporate |
| Information-architecture acceptance criteria | Absent | Criteria are general and visual | Incorporate |
| Mandatory brief at a fixed path | Absent | The plugin accepts multiple sources of truth | Do not incorporate |
| Automatically choose the latest brief | Absent | Could select the wrong feature | Do not incorporate |
| Mandatory interview before any work | Absent | The plugin limits questions to material decisions | Do not incorporate |
| Fixed number of navigation items or levels | Absent | The plugin avoids context-free universals | Do not incorporate |
| Hamburger, tabs, or sidebar as the default solution | Absent | The plugin requires contextual rationale | Do not incorporate |
| Extensive document for every local change | Absent | Current output is proportional to mode | Do not incorporate |
| Create a sixth information-architecture skill | Absent | Would fragment design, audit, and remediation | Do not incorporate |
| Write an artifact during planning without authorization | Absent | Planning is no-edit by default | Do not incorporate |
| Make the URL structure mirror the visual tree | Absent | Contracts may require a URL more stable than the UI | Do not incorporate |

## Adapted recommendations

The recommendations below describe future changes. This report does not change the skills.

### IA-01 — Structural reference within design

- **Priority:** P0
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/information-architecture.md`
- **Concrete change:** create a concise reference with a surface map, navigation,
  hierarchy, flows, URLs, growth, edge cases, and persistence, using condensed
  versions of the models in this report.
- **Reason:** coverage is scattered and depends on the agent inferring the complete discipline.
- **Risk:** turning all visual work into heavy documentation.
- **Mitigation:** require proportional depth and permit compact output for local changes.
- **Acceptance criterion:** in a task with multiple routes, output connects
  surface, audience, task, path, URL, states, and persistence; in a local
  adjustment, it does not create an unnecessary artifact.

### IA-02 — Route the reference from the primary contract

- **Priority:** P0
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Concrete change:** load the new reference when a request involves site/app
  structure, navigation, routes, content organization, onboarding, search,
  filters, documentation, or flow across screens.
- **Reason:** an unread reference does not change behavior.
- **Risk:** excessive activation for a purely aesthetic task.
- **Mitigation:** make structural triggers explicit and retain invocation of the skill as a requirement.
- **Acceptance criterion:** information-architecture requests use the reference;
  an isolated color or typography review is not automatically expanded.

### IA-03 — Direction contract with structural invariants

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Concrete change:** add a compact section for affected navigation, routes/URLs,
  entry points, persisted state, and return compatibility.
- **Reason:** the contract already protects routes and navigation but does not
  require stating how the flow is preserved.
- **Risk:** duplication with the new reference.
- **Mitigation:** retain only fields that act as a gate before code.
- **Acceptance criterion:** a redesign that changes structure records invariants
  for deep links, history, persistence, and migration before implementation.

### IA-04 — Structural pass in visual review

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Concrete change:** before decoration, insert a pass comparing the planned map
  with runtime: entry points, navigation, labels, URL, return, states, and recovery.
- **Reason:** an isolated screenshot does not demonstrate that the architecture works.
- **Risk:** confusing structural failure with preference.
- **Mitigation:** require a task, path, and observable harm.
- **Acceptance criterion:** every structural finding cites the flow and condition
  in which a person becomes lost, loses state, or reaches the wrong destination.

### IA-05 — Structural coverage in audits

- **Priority:** P1
- **Target files:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md` and `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
- **Concrete change:** add controls for the surface map, role-based navigation,
  deep links, URL/canonical/redirect behavior, growth, error/resumption flows, and
  persistence; include a structural coverage matrix in the report.
- **Reason:** the current ledger is strong but does not show which routes and flows
  were actually traversed.
- **Risk:** inflating audit reports for projects without UI.
- **Mitigation:** mark the section applicable only to products with navigable surfaces.
- **Acceptance criterion:** the report distinguishes covered, partial, not
  exercised, and not applicable by surface/flow.

### IA-06 — Remediation gate for navigation and URLs

- **Priority:** P1
- **Target files:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md`, `remediation-protocol.md`, and `validation-checklist.md`
- **Concrete change:** treat changes to primary navigation, public URLs, slugs,
  persisted parameters, or return strategy as material; require before/after maps,
  compatibility, approved redirects, deep-link tests, refresh, back/forward, and rollback.
- **Reason:** a visual fix can break external contracts without changing the final screen.
- **Risk:** blocking a small fix through formality.
- **Mitigation:** apply only when the public contract or path across surfaces changes.
- **Acceptance criterion:** no ID is marked fixed if existing links or expected resumption regress.

### IA-07 — Route and state implementation in code

- **Priority:** P1
- **Target files:** `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md` and `references/review-workflow.md`
- **Concrete change:** when there is a routed frontend, map the route, entry point,
  equivalent loaders/actions, source of truth, URL state, cache, persistence,
  error, and return; require proportionate testing of direct links and restoration.
- **Reason:** the skill already traces persistence and effects but does not connect
  them to browser history and navigation.
- **Risk:** imposing web concepts on native apps, CLIs, or backends.
- **Mitigation:** condition the rule on navigable surfaces and adapt it to the platform.
- **Acceptance criterion:** route changes demonstrate correct behavior on direct
  entry, refresh, and return when applicable.

### IA-08 — Information-architecture security

- **Priority:** P1
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`
- **Concrete change:** cross-check the UI map with the endpoint inventory; verify
  authorization on direct routes, sensitive data in URLs/history/logs, redirects,
  removed resources, per-tenant cache, and state restoration after an identity change.
- **Reason:** hiding a destination in navigation does not protect the route;
  persistence and URLs may cross boundaries.
- **Risk:** duplication with existing authorization and input controls.
- **Mitigation:** add the flow and location perspective without repeating the vulnerability taxonomy.
- **Acceptance criterion:** analysis attempts direct access and state restoration
  with different users, roles, and tenants without treating the UI as a control.

### IA-09 — Measurable information-architecture criteria

- **Priority:** P2
- **Target file:** `plugins/anti-ai-craft/skills/anti-ai-design/references/information-architecture.md`
- **Concrete change:** define portable criteria: critical task is reachable;
  labels are consistent; direct entries recover; no dead ends; state is preserved
  or discarded deliberately; error flows have a next step; coverage is recorded.
- **Reason:** without criteria, the document becomes a description with no validation power.
- **Risk:** creating false universal numbers.
- **Mitigation:** measure through scenarios and contracts, not a fixed limit on clicks or items.
- **Acceptance criterion:** every relevant structural decision has a verifiable scenario and expected outcome.

### IA-10 — Do not change public metadata

- **Priority:** P0 for compatibility
- **Target files:** all `agents/openai.yaml` files and front matter in the five `SKILL.md` files
- **Concrete change:** preserve `anti-ai-design`, `anti-ai-code`, `anti-ai-audit`,
  `anti-ai-remediate`, and `anti-ai-security`, their visible names, and
  `allow_implicit_invocation: false`.
- **Reason:** information architecture is an internal design and review capability,
  not a new invocation contract.
- **Risk:** no functional risk; only less discoverability for someone seeking a separate skill.
- **Mitigation:** mention information architecture in the descriptive triggers of
  `anti-ai-design` without renaming the skill.
- **Acceptance criterion:** existing prompts and scripts continue to work without migration.

## What not to copy

1. Mandatory dependency on a brief file in a specific directory.
2. Silent selection of the most recent file when more than one context is possible.
3. A ritual interview before every task.
4. A universal maximum number of navigation items or depth.
5. A predetermined mobile solution.
6. A URL hierarchy mechanically derived from the visual tree.
7. A complete document for a change to one surface.
8. Automatic artifact writing during analysis.
9. Component extraction because two surfaces look similar.
10. An assumption that the most-used page consumes a fixed percentage of time.

These points may serve as questions, never as rules without context and evidence.

## When information architecture is necessary or excessive

### Apply the complete stage

Use complete structural analysis when at least one of these signs exists:

- a new product with more than one surface;
- a change to primary navigation;
- creation, removal, or migration of public routes;
- multiple roles, tenants, or entry points;
- content that will grow and require search, filters, pagination, or archives;
- onboarding or a multistep flow;
- requirements for deep links, resumption, sharing, or SEO;
- inconsistent names, paths, or hierarchy across areas;
- a redesign that may change structure, not only appearance;
- a history of people becoming lost or failing to find content;
- security risk tied to routes, URLs, state, or direct access.

### Apply a compact version

Use only a mini-contract when:

- the change affects one screen but changes priority, an action, or state;
- a modal/drawer introduces a recoverable step;
- a filter or tab now needs a URL;
- a long form needs to preserve a draft;
- a component changes how the person returns to the previous context.

The mini-contract may fit in five fields: entry point, task, path, persisted state,
and return/error criterion.

### Consider it excessive

Do not require a complete artifact when:

- the fix is purely visual and changes no hierarchy, label, action, route, or state;
- there is one simple surface and the flow is already explicit;
- the request is a local contrast, focus, or semantic fix;
- the system has no navigation or growing content;
- the document would fully repeat routes and contracts already maintained by an authoritative source;
- structure is not being decided and the task is only to implement an approved finding.

Even in these cases, preserving existing invariants remains required.

## When to use artificial intelligence for this stage

To avoid ambiguity, information architecture and artificial intelligence are not the same thing.

### Justified use

Model assistance helps when it is necessary to:

- inventory many routes, layouts, roles, and states;
- cross-check code, documentation, and tests for divergences;
- generate decision questions from concrete gaps;
- compare alternatives using explicit criteria;
- build an initial coverage matrix for human review;
- find edge cases and alternative paths that will later be tested.

### Excessive use

It is excessive to use a model to:

- invent pages or flows without a requirement;
- replace user observation, analytics, or a product decision;
- produce an extensive map of a trivial flow;
- impose navigation patterns based on frequency in training examples;
- declare that the structure works without executing links and flows;
- create abstractions or files only to appear complete;
- decide alone on a material change to navigation, a public URL, or identity.

Every assisted output should be reconciled with code, runtime, project rules, and
human decisions. The model may organize and test hypotheses; it does not become a
source of truth.

## Recommended incorporation plan

1. Create the information-architecture reference in `anti-ai-design`.
2. Route it from the primary contract only for structural triggers.
3. Add the structural pass and acceptance criteria.
4. Extend audits with a coverage matrix.
5. Extend remediation with compatibility and navigation/URL tests.
6. Add minimum integrations to code and security.
7. Validate all five skills and check for repetition, scope expansion, or identifier changes.

## Final checklist for this analysis

- [x] The external unit was read in full.
- [x] The five current skills, their references, and their `agents/openai.yaml` files were read in full.
- [x] Inputs and outputs were compared.
- [x] Maps, navigation, URLs, flows, edge cases, and persistence were covered.
- [x] Existing, partial, missing, and rejected capabilities were separated.
- [x] Every recommendation has a priority, target file, change, reason, risk, and acceptance criterion.
- [x] Proportionality rules and use of artificial intelligence were recorded.
- [x] Public names and compatibility were preserved.
- [x] No plugin file was changed by this analysis.
