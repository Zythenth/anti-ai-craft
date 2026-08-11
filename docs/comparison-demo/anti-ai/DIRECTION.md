# Direction contract — Cadence

## Scope and sources of truth

- Surface: local operation of a translation queue.
- Mandate: create an isolated static implementation with no previous identity to preserve.
- Sources read: `README.md`; `docs/comparison-demo/SHARED-BRIEF.md`;
  `docs/comparison-demo/data.js`; installed skill `anti-ai-design` 0.4.0 and its
  references `design-principles.md`, `design-antipatterns.md`,
  `accessibility-baseline.md`, `direction-contract.md`, and `review-workflow.md`.
- Authoritative source of records: only `window.DEMO_TRADUCAO`, loaded from `../data.js`.

## Contract

1. **Thesis:** present the batch as a compact operational run sheet in which
   status, blocker, and action align on the same reading line.
2. **Mode and dominant task:** operate; locate a chapter, recognize its situation,
   and perform the next safe action.
3. **First viewport:** at 1280 × 800, the header identifies the environment and
   batch; the summary confirms queue composition; search, filters, and all four
   rows are immediately reachable.
4. **Primary path:** read summary → locate or filter → recognize status → inspect
   context → perform a simulated action and receive confirmation without losing focus.
5. **Structure:** minimal header, batch context, a single summary/execution band,
   tools, and table. Details appear next to their source row.
6. **Color and type:** deep green structures the environment; light paper supports
   reading; red is reserved for blockers/actions; amber, green, and gray identify
   other states, always accompanied by text and a symbol. Sans serif drives
   operations, serif appears only in the title, and monospace only in IDs, times,
   and the pipeline identifier.
7. **Signature:** chapter codes act as the margin of a run sheet, while the cadence
   mark uses three restrained beats in the header.
8. **Rejected default:** do not use a card/KPI dashboard, promotional hero,
   ellipsis menus, or hidden important actions; the data call for row-by-row
   comparison and direct actions.
9. **Primary risk:** table density may reduce readability or cause overflow.
   Validate 1280 × 800 and narrow reflow; below 720 px, each row preserves priority
   order without global horizontal scrolling.
10. **Invariants:** four records and their exact values; data labeled as a
    demonstration; no external mutation; search, filters, details, selection,
    blocker recovery, visible focus, and action announcements.

## Component decisions

- `data.js`: reuse directly, without copying or mutation.
- Queue table: create with native HTML because it compares homogeneous records in two dimensions.
- Search and filters: compose with `input[type=search]` and buttons using `aria-pressed`.
- Per-chapter actions: create as visible buttons without overflow because they are frequent and there are no more than two per row.
- Details and recovery: extend the row with an adjacent region; this avoids a modal and retains the blocked chapter's context.
- Batch selection: create only for records marked `selectable`; other controls remain disabled and named.
- Dependencies, network calls, fonts, and external assets: out of scope.

## States and recovery

- Search/filter: update results in an `aria-live` region; zero results provides explicit restoration.
- Details: the button exposes `aria-expanded` and keeps details in the row's flow.
- Selection: native checkbox, `checked` state, visual change, and disabled batch action until a valid selection exists.
- Blocked glossary: opening retains the region next to `ch115`; local confirmation enables retry without changing the fixture.
- Actions: all end with a visible, announced message; none run scripts or write files.

## Verifiable criteria

- Open through `file://` with no external dependency or JavaScript error.
- Display all four IDs and the fixture summary `4 / 15,743 / 1 / 1 / 1 / 1`.
- Working search by ID/title, clearing, and four filters.
- Details available for every chapter.
- Batch selection/application available only for the ready record.
- `ch115` flow: resolve → confirm → retry, always with simulated feedback.
- Visible focus; native controls; landmarks, headings, labels, and programmatic messages.
- No global horizontal scrolling in the target viewport or implemented narrow reflow.

## Delivered files

- `index.html`: semantic structure and loading of the shared source.
- `styles.css`: visual direction, states, focus, reflow, high-contrast modes, and reduced motion.
- `app.js`: fixture rendering, search, filters, details, selection, recovery, and simulated feedback.
- `DIRECTION.md`: contract, decisions, criteria, validations, and boundaries for this branch.

## Validations and limitations

- Exercised: syntax of `app.js` and `data.js`; loading and freezing of
  `window.DEMO_TRADUCAO`; four IDs; total of 15,743 words; a single reference to
  `../data.js`; no external URL in HTML; no copied titles in JavaScript; and
  `git diff --check` in the branch directory.
- Visual browser review, real Tab/Shift+Tab traversal, screen reader, zoom, text
  spacing, and forced colors: not exercised in this session because no browser was
  available in the integrated runtime.
- The CSS includes compositions for 1280 × 800 and reflow below 720 px, but the
  lack of a real capture limits claims about finish and clipping to what was
  statically verified.
