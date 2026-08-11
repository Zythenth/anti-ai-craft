# Shared brief — translation queue

## Objective

Create a static operational screen for tracking a batch of chapters processed by
a translation pipeline. The person responsible needs to quickly recognize what
has finished, what is in progress, what requires a human decision, and the next
safe action for each chapter.

Both implementations in the comparison must start from this same brief and load
`data.js` without copying, replacing, or supplementing the records. The data are
demonstration fixtures and do not represent a work, client, or real execution.

## Environment and framing

- Surface: an operational application used on desktop.
- Primary user: a reviewer tracking V1, V3, diffs, and the glossary.
- Capture viewport: **1280 × 800 CSS px**, 100% zoom.
- Language: English.
- Execution: local static files, with no mandatory server, build, library, font,
  or network call.
- Initial state: exactly as defined in `window.DEMO_TRADUCAO`.
- Every mutation is simulated in the interface; no action may edit chapters or
  call real scripts.

## Required content

Display the following without changing values or inventing metrics:

1. Surface name, project, batch, reference time, and a “Demonstration data” label.
2. Batch summary: four chapters, 15,743 words, one chapter ready, one blocked, one
   under review, and one queued.
3. Pipeline execution identifier and a statement that calls are isolated.
4. The four chapters from `data.js`, each with:
   - ID, title, and word count;
   - current stage/status;
   - glossary status;
   - operational summary;
   - estimated time;
   - next action and a view-details action.
5. For `ch115`, communicate the two pending terms, that execution stopped before
   changing files, and which recovery paths are available.
6. A short explanation that actions performed in this demonstration are only simulated.

No record may be omitted, duplicated, or assigned a different status. The same
content must be present in the initial DOM of both implementations even if its
organization and means of access differ.

## Minimum tasks and interactions

The following tasks must be possible with a mouse and keyboard:

1. Search by chapter ID or title and clear the search.
2. Filter the queue by `All`, `Needs attention`, `In progress`, and `Ready`.
3. View the details of any chapter.
4. Trigger the next action for each chapter. The outcome must be only a simulated
   message and must not modify the shared data.
5. In the blocked chapter, open glossary decisions and retry after simulated
   confirmation. The interface must retain the chapter context.
6. Select the ready chapter and simulate applying the diff as a batch action.

Controls may remain visible, be grouped, appear in menus, or use another structure
as long as every task is complete and the implementation records the simulated outcome.

## Minimum states

- Default state with all four chapters.
- Filter with results and filter with no results.
- Search with no matches and an explicit way to clear/recover.
- Selected item and unavailable action when it does not apply.
- Simulated action confirmation.
- `ch115` failure with its current effect and recovery paths.
- Success or status message after every simulated action.

## Basic accessibility

- Use semantic HTML and a coherent reading and focus order.
- Give every control an accessible name; the name must include visible text when
  visible text exists.
- Make all functionality keyboard-operable without positive `tabindex` values.
- Maintain a visible focus indicator.
- Do not communicate stage, failure, selection, or availability through color or position alone.
- Associate search with a persistent label.
- Programmatically expose expansion, selection, disabled state, and dynamic messages when applicable.
- Announce simulated outcomes in a status region without moving focus.
- Keep interactive targets at least 24 × 24 CSS px.
- Respect `prefers-reduced-motion` when motion exists.

## Comparison boundaries

This brief does not prescribe layout, navigation, density, components, palette,
typography, borders, radius, icons, or motion. Each implementation may make its
own visual and structural decisions but must fully preserve the function, data,
tasks, states, viewport, and constraints above.

For the final capture, use the same browser, theme, zoom, viewport, and initial
state. Do not use different text, records, or interactions to favor one version.

## Acceptance criteria

- Opens directly as a local file and produces no JavaScript error.
- Loads `data.js` as the sole source of records.
- Renders all four IDs and exact fixture values.
- Implements all six minimum tasks with no external effect.
- Meets basic requirements for keyboard, focus, names, and state communication.
- Fits in the capture viewport without global horizontal scrolling.
- Declares any requirement not exercised instead of assuming it was validated.
