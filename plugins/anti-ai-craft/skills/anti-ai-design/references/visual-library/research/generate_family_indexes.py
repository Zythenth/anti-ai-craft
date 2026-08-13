#!/usr/bin/env python3
"""Regenerate compact Markdown indexes from catalog.jsonl."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.jsonl"
FAMILY_DIR = ROOT / "families"

FAMILIES = {
    "dense-professional": {
        "title": "Dense professional",
        "definition": "High-information work surfaces where aligned comparison, status, hierarchy, and frequent action justify visible density.",
        "tasks": "Operational queues, CRMs, issue tracking, search, analytics, review, and administration with many comparable objects.",
        "errors": "Adding density without hierarchy; replacing evidence with KPI cards; exposing every secondary action permanently.",
        "avoid": "Small collections, calm reading, promotional surfaces, or novice workflows that do not benefit from simultaneous context.",
    },
    "command-keyboard-first": {
        "title": "Command / keyboard-first",
        "definition": "Surfaces organized around fast retrieval and execution of named actions, often with shortcuts, ranking, and recent context.",
        "tasks": "Expert navigation, global actions, launchers, command palettes, and repeated workflows where recall beats browsing.",
        "errors": "Making commands undiscoverable; using a palette as the only path; mixing destructive and safe actions without cues.",
        "avoid": "Infrequent consumer tasks, touch-first flows, or situations where users cannot know the available vocabulary.",
    },
    "canvas-spatial": {
        "title": "Canvas / spatial",
        "definition": "Interfaces where position, scale, connection, sequence, or direct manipulation carries domain meaning.",
        "tasks": "Design, node graphs, timelines, maps, diagrams, media sequencing, and prototypes.",
        "errors": "Treating the canvas as decoration; hiding selection context; omitting inspectors, coordinates, or navigational anchors.",
        "avoid": "Linear forms, simple records, and tasks where spatial freedom adds ambiguity rather than expressive power.",
    },
    "document-centric": {
        "title": "Document-centric",
        "definition": "Interfaces where a persistent written or structured artifact is the primary object and surrounding controls serve its authorship, reading, or provenance.",
        "tasks": "Writing, notes, knowledge bases, specifications, collaborative documents, and research collections.",
        "errors": "Fragmenting the artifact into dashboard widgets; letting chrome dominate the document; hiding provenance or document state.",
        "avoid": "Rapid monitoring, high-volume comparison, or workflows whose core object is a graph, timeline, or queue.",
    },
    "industrial-tool-like": {
        "title": "Industrial / tool-like",
        "definition": "Purpose-built control surfaces whose geometry follows instruments, physical systems, media channels, or precise operational state.",
        "tasks": "Audio, 3D, device control, deployment, machine-like configuration, and expert production tools.",
        "errors": "Imitating hardware cosmetically; obscuring current state; removing labels in the name of minimalism.",
        "avoid": "General content browsing, simple consumer forms, or domains without a stable control-and-feedback model.",
    },
    "expressive-playful": {
        "title": "Expressive / playful",
        "definition": "Interfaces whose tone, composition, motion, or customization supports exploration, identity, delight, or creative ownership.",
        "tasks": "Personalization, creative exploration, expressive consumer tools, playful onboarding, and culturally specific products.",
        "errors": "Adding decoration unrelated to action; sacrificing legibility; assuming asymmetry or novelty is inherently human.",
        "avoid": "Safety-critical work, dense regulated operations, or contexts where visual surprise interferes with predictable control.",
    },
    "technical-developer": {
        "title": "Technical / developer",
        "definition": "Evidence-rich surfaces for building, inspecting, diagnosing, comparing, and operating software or other technical systems.",
        "tasks": "Code, diffs, logs, debugging, observability, deployment, schemas, and generated-artifact inspection.",
        "errors": "Showing summaries without evidence; using terminal aesthetics as decoration; disconnecting state from the artifact it affects.",
        "avoid": "General audiences that do not share the underlying model or lightweight tasks that need plain-language guidance.",
    },
    "communication": {
        "title": "Communication",
        "definition": "Conversation and coordination surfaces where authorship, sequence, reply structure, presence, and shared context organize interaction.",
        "tasks": "Messaging, comments, reviews, group coordination, and asynchronous discussion.",
        "errors": "Flattening threads; separating discussion from its object; turning every message into a decorative card.",
        "avoid": "One-way publication, structured records better served by fields, or urgent systems requiring acknowledged alerts.",
    },
    "content-catalog": {
        "title": "Content / catalog",
        "definition": "Browse and retrieval surfaces where recognizable items, provenance, filtering, and collection structure matter more than global metrics.",
        "tasks": "Libraries, marketplaces, media collections, research blocks, assets, products, and discovery.",
        "errors": "Using identical cards for heterogeneous media; hiding filters; relying on imagery when comparison needs aligned attributes.",
        "avoid": "Operational queues, detailed editing, and homogeneous numeric records better expressed as tables or lists.",
    },
    "minimal-utilitarian": {
        "title": "Minimal / utilitarian",
        "definition": "Focused surfaces with deliberately few controls because the task, state, or object model is genuinely narrow.",
        "tasks": "Settings, quick actions, lightweight utilities, focused retrieval, and constrained single-purpose workflows.",
        "errors": "Removing essential context; mistaking emptiness for quality; hiding infrequent but critical actions.",
        "avoid": "Complex comparison, multi-stage operations, or domains whose exceptions and relationships must remain visible.",
    },
}


def compact(text: str, limit: int = 150) -> str:
    text = " ".join(text.split()).replace("|", "\\|")
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def main() -> None:
    entries = [json.loads(line) for line in CATALOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for entry in entries:
        grouped[entry["family"]].append(entry)

    FAMILY_DIR.mkdir(parents=True, exist_ok=True)
    for slug, description in FAMILIES.items():
        items = grouped[slug]
        products = ", ".join(sorted({str(item["product"]) for item in items})) or "None yet"
        lines = [
            f"# {description['title']}",
            "",
            description["definition"],
            "",
            f"**Usually appropriate for:** {description['tasks']}",
            "",
            f"**Frequent errors:** {description['errors']}",
            "",
            f"**Do not use by default for:** {description['avoid']}",
            "",
            f"**Products represented:** {products}.",
            "",
            "This is a textual index. Open only the source or local image for the few references selected for the current task.",
            "",
            "| ID | Product | Screen | Mini summary | When to consult | Main characteristic | Theme | Image or source |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for item in items:
            target = f"../{item['image_path']}" if item.get("image_path") else item["source_url"]
            target_label = "local image" if item.get("image_path") else "source"
            lines.append(
                "| {id} | {product} | {title} | {summary} | {when} | {characteristic} | {theme} | [{label}]({target}) |".format(
                    id=item["id"],
                    product=str(item["product"]).replace("|", "\\|"),
                    title=str(item["title"]).replace("|", "\\|"),
                    summary=compact(str(item["why_selected"])),
                    when=compact(str(item["inappropriate_context"]).replace("Wrong for", "Consult for the inverse of"), 120),
                    characteristic=compact(str(item["reusable_decision"]), 130),
                    theme=item["theme"],
                    label=target_label,
                    target=target,
                )
            )
        lines.append("")
        (FAMILY_DIR / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
