# Final visual-library report

Date: 2026-08-13

## Outcome

- Candidates researched across the original and legal-first passes: **221**.
- Rejected or superseded: **121**.
- Accepted in the public catalog: **100**.
- Images locally versioned: **100**.
- Main-catalog link-only references: **0**.
- Versioned image size: **19,494,768 bytes**.

The legal-first rebuild replaced every permission-unclear or explicitly restricted main-catalog screenshot. Earlier proprietary research is summarized separately and does not count toward the 100.

## Theme distribution

| Theme | Count |
| --- | ---: |
| Dark | 55 |
| Light | 44 |
| Mixed | 1 |
| System/adaptive | 0 |

## Family distribution

| Family | Count |
| --- | ---: |
| Dense professional | 14 |
| Command / keyboard-first | 8 |
| Canvas / spatial | 10 |
| Document-centric | 10 |
| Industrial / tool-like | 12 |
| Expressive / playful | 10 |
| Technical / developer | 12 |
| Communication | 8 |
| Content / catalog | 8 |
| Minimal / utilitarian | 8 |

## Product distribution

| Product | Count | Product | Count |
| --- | ---: | --- | ---: |
| GitHub | 5 | Blender | 5 |
| Visual Studio Code | 3 | Godot | 4 |
| Penpot | 6 | Zulip | 6 |
| Mattermost | 6 | Nextcloud | 5 |
| GIMP | 6 | FreeCAD | 6 |
| KiCad | 5 | OpenShot | 6 |
| Actual Budget | 4 | Immich | 5 |
| Documenso | 5 | Excalidraw | 3 |
| Element | 2 | darktable | 6 |
| Kdenlive | 6 | Grafana | 3 |
| Apache Superset | 3 |  |  |

No product contributes more than six references.

## Originally mandatory proprietary set

The user's later legal-first direction superseded mandatory main-catalog coverage when the screenshot file could not be redistributed. Counts in the local public catalog are:

| Product | Count | Product | Count |
| --- | ---: | --- | ---: |
| Linear | 0 | Raycast | 0 |
| PostHog | 0 | Attio | 0 |
| Sentry | 0 | Railway | 0 |
| Resend | 0 | Superlist | 0 |
| Notion | 0 | Figma | 0 |
| Blender | 5 | Ableton Live | 0 |
| Teenage Engineering | 0 | Nothing | 0 |
| Gumroad | 0 | Are.na | 0 |
| Craigslist | 0 | GitHub | 5 |
| Discord | 0 | Steam | 0 |

The absent products remain only as a product-level superseded-research summary; their images are not present.

## Rights and license findings

- 94 items require attribution; 6 FreeCAD documentation images are CC0.
- License coverage: AGPL 3.0 (21), Apache 2.0 (9), CC BY 3.0 (14), CC BY 3.0 US (3), CC BY 4.0 (5), CC BY-SA 4.0 (11), CC0 (6), GFDL 1.2 (6), GPL 3.0 (12), MIT (7), MPL 2.0 (6).
- The 87 earlier proprietary/link-only items were superseded because redistribution permission was unclear or restricted.
- Five Joplin candidates were rejected because the repository license separately reserves logos and icons visible in the screenshots.
- Visual Studio Code screenshots require the full product name, an unaltered full screenshot, and “Used with permission from Microsoft.”
- License texts and attribution details are stored in `../LICENSES/` and `../ATTRIBUTIONS.md`.
- Trademark rights are not granted; inclusion does not imply endorsement. This is a conservative repository audit, not legal advice.

## Created and modified files

- Created `catalog.jsonl` with 100 records.
- Created 100 image files across 21 product directories.
- Created 10 family indexes.
- Created `README.md`, `ATTRIBUTIONS.md`, 11 license texts, image-storage guidance, progress/checkpoint/rejection records, qualitative audit, and this report.
- Created research maintenance, generation, integrity, and validation scripts.
- Modified only the existing `anti-ai-design/SKILL.md`, adding one progressive-disclosure reference-loading rule.
- `direction-contract.md` and `sources.md` were intentionally left unchanged because their dominant-reference and evidence-boundary rules already apply without duplication.

## Validation results

- Catalog schema/count/family/theme/product/local-file validator: **pass**.
- IDs VR-001 through VR-100 without gaps: **pass**.
- Image SHA-256 exact duplicates: **none**.
- Image integrity and recorded dimensions: **100/100 pass**.
- Family local-image links: **100/100 pass**.
- Python compilation for all research scripts: **pass**.
- `git diff --check`: **pass**.
- Files outside the skill/library scope changed: **none**.

The dHash detector reported VR-051/VR-052 at distance 3. Manual review retained both because VR-051 shows heterogeneous direct construction while VR-052 shows a generated polar array; the shared FreeCAD canvas explains the visual similarity, but their operations and domain relationships differ materially.

## Ten-scenario audit

The qualitative audit passed for operational CRM, technical assistance, web IDE, observability, document editing, messaging, asset catalog, creative production, expressive entry/landing, and dense administration. Ten different products supplied the dominant references. Retrieved alternatives included ledgers, boards, trees, playbook documents, evidence drawers, debuggers, diffs, command palettes, flame graphs, knowledge documents, topic hierarchies, catalogs, timelines, 3D workspaces, mosaics, matrices, and permission tables.

See `qualitative-audit.md` for dominant and secondary IDs and the dark-mode bias test.

## Remaining limitations

- License and trademark interpretation can change and should be rechecked before a major public release.
- Copyleft and attribution obligations must remain attached when assets are redistributed downstream.
- Earlier superseded proprietary research now retains product-level counts and source entry points rather than all individual item URLs.
- Perceptual hashing is a review aid, not proof of semantic duplication.
- Screenshots demonstrate an existing structure; they do not prove that the structure is effective or appropriate in another product.
