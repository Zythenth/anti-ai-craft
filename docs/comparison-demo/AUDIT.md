# Independent equivalence audit

Date: July 28, 2026

Scope: `baseline/` and `anti-ai/` frozen at the state identified by the hashes below.

Question: did both versions receive and implement the same data, requirements,
and interactions without a structural advantage that invalidates the comparison?

## Verdict

**The comparison is valid for evaluating visual organization, access to actions,
status readability, and recovery at the defined viewport.** No blocking divergence
in data, function, or task was found. Both versions use the same frozen fixture,
present the same four chapters, and implement all six minimum tasks without
external calls.

The differences found are interface decisions permitted by the brief: the
baseline uses dialogs and confirmations; the other version keeps details and
recovery next to the row. This changes the path and hierarchy—the precise object
of the comparison—without changing the outcome each person can reach.

The experiment alone does not demonstrate reduced time, errors, or cognitive load
and should not be presented as a usability test or causal evidence. It is also
more accurate to call it **baseline versus the skill-guided version** than a
literal “before/after” transformation of the same code.

## Audited state

| File | SHA-256 |
|---|---|
| `SHARED-BRIEF.md` | `856C3440C089C096D26013971787E568C8174DF8CDC4C767DA292DC2889CF945` |
| `data.js` | `590BEC1FCC251DE4F588F43A8B5DC6F9712A2E24E64BFDF38B37CCC27F21C0E6` |
| `baseline/index.html` | `E3F04C84C095BC1E73CD8066CF5D4C533A3EBB47F87A379C4ECDBF53CB0C94FA` |
| `baseline/styles.css` | `97E37B4D26031CDAC59FEBCA390F9E06D22777BF60FB37E996463F6BAB742395` |
| `baseline/app.js` | `F12CA6A47BF50194FB7F6A8276C5EA59C1CB5AEF69005F68B180F8EC1D8A5C00` |
| `anti-ai/index.html` | `F1CD690A17562C90835F9DE4412DA9D649827E74857C1844981E93EB42AE9DAF` |
| `anti-ai/styles.css` | `DA45C068E92F3CC22A940B2E02968CD0EEA4B19E403F6778BB1D72F6AC855CB2` |
| `anti-ai/app.js` | `F46F4FD5411C4528D509747C3A4337EDCA3983021EDFC161DD56F3D17239AD99` |

If any hash changes, this audit no longer covers the modified file.

## Data equivalence

| Control | Baseline | Skill-guided version | Outcome |
|---|---|---|---|
| Record source | loads `../data.js` and reads `window.DEMO_TRADUCAO` | same | equivalent |
| Records | iterates over `fixture.chapters` | same | equivalent |
| IDs | `ch114`, `ch115`, `ch116`, `ch117` | same IDs | equivalent |
| Total | 4 chapters and 15,743 words | same summary | equivalent |
| Distribution | 1 ready, 1 blocked, 1 under review, 1 queued | same | equivalent |
| Metadata | surface, project, batch, date, time, pipeline, and fixture notice | same | equivalent |
| `ch115` | two terms, interruption without changes, and three recovery paths | same | equivalent |
| Fixture mutation | not found | not found | equivalent |
| External effect | no `fetch`, XHR, WebSocket, remote URL, storage, or process execution found | same | equivalent |

`data.js` recursively freezes the object. Isolated execution confirmed all four
IDs, the total of 15,743 words, and `Object.isFrozen` on the object, collection,
and chapters. Neither version keeps a competing copy of the records in its own JavaScript.

## Requirement and interaction equivalence

| Brief task | Baseline | Skill-guided version | Outcome |
|---|---|---|---|
| Search by ID/title | `input[type=search]`, fixture filtering, and a counter | same functional mechanism | equivalent |
| Clear and recover from zero results | `Clear` and `Show all` buttons | `Clear` and `Clear search and show all` | equivalent |
| Four required filters | generated from `fixture.filters` | generated from the same source | equivalent |
| View any chapter | native dialog populated from the record | expandable adjacent details | equivalent |
| Perform the simulated next action | dialog confirmation and local message | direct action and local message | equivalent |
| Resolve `ch115` and retry | details → glossary confirmation → retry enabled | inline details → confirmation → retry enabled | equivalent |
| Select `ch114` and apply as a batch | selectable checkbox and batch button | selectable checkbox and batch button | equivalent |
| Unavailable state | inapplicable checkboxes are disabled and named | same | equivalent |
| Feedback | status/toast region; does not change the fixture | status region; does not change the fixture | equivalent |

### Runtime evidence supplied by primary QA

In the same browser at `1280 × 800`, primary QA reported that **both** passed:

- search with one result and clearing;
- `Needs attention` filter with one row;
- opening `ch115` details;
- selecting `ch114` and simulated batch application;
- glossary confirmation, enabling retry, and running another attempt;
- console without warnings or errors.

This evidence was supplied by the primary agent; it was not repeated by this auditor.

## Minimum accessibility and capture conditions

In static inspection, both use a persistent search label, native controls, a
semantic table, accessible names, disabled states, `aria-live` feedback, visible
focus, and text alongside states. Neither relies on color alone. Both include
`prefers-reduced-motion` handling. The skill-guided version adds details such as
`aria-expanded` in the inline flow and `forced-colors` styles; these are
improvements beyond the shared floor, not exclusive requirements granted to one branch.

For comparable captures, preserve the following in both:

- identical browser, system, theme, and scale;
- a 1280 × 800 CSS px viewport and 100% zoom;
- top of the page and initial state, with no search, filter, selection, or details open;
- the fixture and hashes above without changes;
- no crop that hides relevant content from only one version.

## Nonblocking divergences

1. The baseline uses a modal dialog for details and confirmation; the other
   version expands details beside the row and confirms common actions through status.
2. In the baseline, individual `Apply diff` and application by selection are
   separate paths. In the other version, the individual `ch114` button depends on
   selection. Both still offer the specified individual task and batch task.
3. The baseline also keeps the `ch115` incident in a persistent section; the other
   version reveals it in that row's details. Content and recovery are the same.
4. The baseline presents the summary as six metrics; the other version presents
   it in one textual line. Values come from the same source.
5. Both add the interface name “Cadence,” which is not a fixture record. Because
   the addition is symmetrical and changes no data, task, or state, it favors neither branch.

None of these divergences invalidates the comparison. They should not be “fixed”
before capture because they represent the decisions the comparison is intended to reveal.

## Reproducible checks

Run in PowerShell from `docs/comparison-demo`:

```powershell
node --check .\data.js
node --check .\baseline\app.js
node --check .\anti-ai\app.js

node -e "global.window={}; require('./data.js'); const d=window.DEMO_TRADUCAO; console.log({ids:d.chapters.map(x=>x.id), words:d.chapters.reduce((n,x)=>n+x.words,0), frozen:Object.isFrozen(d)&&Object.isFrozen(d.chapters)&&d.chapters.every(Object.isFrozen)})"

rg -n --fixed-strings '<script src="../data.js"></script>' .\baseline\index.html .\anti-ai\index.html
rg -n 'window\.DEMO_TRADUCAO|fixture\.chapters|fixture\.filters|fixture\.summary' .\baseline\app.js .\anti-ai\app.js
rg -n 'fetch\(|XMLHttpRequest|WebSocket|https?://|localStorage|sessionStorage|\.writeFile|exec\(|spawn\(' .\baseline .\anti-ai
rg -n ':focus-visible|prefers-reduced-motion|forced-colors|overflow-x' .\baseline\styles.css .\anti-ai\styles.css
```

Outcome of this execution: all three `node --check` commands returned code 0; the
fixture returned all four IDs, 15,743 words, and true frozen status; both HTML
files load the same source; the search for external effects returned no matches.

## Boundaries

- This auditor did not repeat screen-reader navigation, 400% zoom, text spacing, or forced colors.
- Static inspection and runtime QA support functional equivalence, not a conclusion about visual preference.
- Any claim of “faster,” “fewer errors,” or “easier” requires measurement with
  people and controlled tasks; an isolated capture supports only observable differences.
