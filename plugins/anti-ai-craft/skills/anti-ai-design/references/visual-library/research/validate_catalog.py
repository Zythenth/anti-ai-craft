#!/usr/bin/env python3
"""Validate the Anti-AI Design visual reference catalog."""

from __future__ import annotations

import hashlib
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.jsonl"
IMAGES = ROOT / "images"

FAMILY_TARGETS = {
    "dense-professional": 14,
    "command-keyboard-first": 8,
    "canvas-spatial": 10,
    "document-centric": 10,
    "industrial-tool-like": 12,
    "expressive-playful": 10,
    "technical-developer": 12,
    "communication": 8,
    "content-catalog": 8,
    "minimal-utilitarian": 8,
}
THEMES = {"dark", "light", "mixed", "system/adaptive"}
REDISTRIBUTION = {
    "redistributable",
    "attribution-required",
    "permission-unclear",
    "link-only",
}
MINIMUM_PRODUCTS = 15
MAXIMUM_REFERENCES_PER_PRODUCT = 6
REQUIRED_TEXT_FIELDS = {
    "id",
    "product",
    "title",
    "family",
    "surface_mode",
    "theme",
    "source_url",
    "source_type",
    "task",
    "structure_rationale",
    "domain_relationship",
    "generic_dashboard_loss",
    "reusable_decision",
    "product_specific_decision",
    "why_selected",
    "inappropriate_context",
    "redistribution_status",
    "license_notes",
    "license_id",
    "license_url",
    "validated_at",
}
REQUIRED_LIST_FIELDS = {
    "secondary_tags",
    "lessons",
    "anti_patterns_countered",
    "do_not_copy",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_catalog(errors: list[str]) -> list[dict]:
    entries = []
    for line_number, raw in enumerate(CATALOG.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            entry = json.loads(raw)
        except json.JSONDecodeError as exc:
            fail(errors, f"line {line_number}: invalid JSON: {exc}")
            continue
        if not isinstance(entry, dict):
            fail(errors, f"line {line_number}: entry must be an object")
            continue
        entries.append(entry)
    return entries


def validate_entry(entry: dict, index: int, errors: list[str]) -> None:
    expected_id = f"VR-{index:03d}"
    if entry.get("id") != expected_id:
        fail(errors, f"entry {index}: expected id {expected_id}, got {entry.get('id')!r}")

    for field in REQUIRED_TEXT_FIELDS:
        if not isinstance(entry.get(field), str) or not entry[field].strip():
            fail(errors, f"{expected_id}: {field} must be a non-empty string")
    for field in REQUIRED_LIST_FIELDS:
        if not isinstance(entry.get(field), list) or not entry[field]:
            fail(errors, f"{expected_id}: {field} must be a non-empty list")

    if entry.get("family") not in FAMILY_TARGETS:
        fail(errors, f"{expected_id}: invalid family {entry.get('family')!r}")
    if entry.get("theme") not in THEMES:
        fail(errors, f"{expected_id}: invalid theme {entry.get('theme')!r}")
    if entry.get("redistribution_status") not in REDISTRIBUTION:
        fail(errors, f"{expected_id}: invalid redistribution_status")
    if not re.match(r"^https://", str(entry.get("source_url", ""))):
        fail(errors, f"{expected_id}: source_url must use HTTPS")

    dimensions = entry.get("dimensions")
    if not isinstance(dimensions, dict) or not all(
        isinstance(dimensions.get(axis), int) and dimensions[axis] > 0
        for axis in ("width", "height")
    ):
        fail(errors, f"{expected_id}: positive integer dimensions are required")

    validation = entry.get("validation")
    if not isinstance(validation, dict) or not validation:
        fail(errors, f"{expected_id}: validation checklist is required")
    elif not all(value is True for value in validation.values()):
        fail(errors, f"{expected_id}: every recorded validation check must be true")

    image_path = entry.get("image_path")
    status = entry.get("redistribution_status")
    if status not in {"redistributable", "attribution-required"}:
        fail(errors, f"{expected_id}: public catalog entries must be locally redistributable")
    if status in {"redistributable", "attribution-required"} and not image_path:
        fail(errors, f"{expected_id}: redistributable entry requires image_path")
    if image_path:
        local_path = ROOT / image_path
        if not local_path.is_file():
            fail(errors, f"{expected_id}: missing image {image_path}")
        else:
            digest = hashlib.sha256(local_path.read_bytes()).hexdigest()
            if entry.get("sha256") != digest:
                fail(errors, f"{expected_id}: SHA-256 mismatch")
    elif entry.get("sha256") is not None:
        fail(errors, f"{expected_id}: link-only entry must use null sha256")
    if not re.match(r"^https://", str(entry.get("license_url", ""))):
        fail(errors, f"{expected_id}: license_url must use HTTPS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partial", action="store_true", help="validate an in-progress catalog")
    args = parser.parse_args()
    errors: list[str] = []
    entries = load_catalog(errors)
    for index, entry in enumerate(entries, 1):
        validate_entry(entry, index, errors)

    if not args.partial and len(entries) != 100:
        fail(errors, f"expected 100 entries, found {len(entries)}")

    families = Counter(entry.get("family") for entry in entries)
    if not args.partial and families != Counter(FAMILY_TARGETS):
        fail(errors, f"family counts differ: {dict(families)}")
    if args.partial:
        for family, count in families.items():
            if count > FAMILY_TARGETS[family]:
                fail(errors, f"{family}: partial count {count} exceeds final target {FAMILY_TARGETS[family]}")

    themes = Counter(entry.get("theme") for entry in entries)
    if not args.partial and not 55 <= themes["dark"] <= 60:
        fail(errors, f"expected 55 to 60 dark references, found {themes['dark']}")

    products = Counter(entry.get("product") for entry in entries)
    if not args.partial and len(products) < MINIMUM_PRODUCTS:
        fail(errors, f"expected at least {MINIMUM_PRODUCTS} products, found {len(products)}")
    for product, count in products.items():
        if count > MAXIMUM_REFERENCES_PER_PRODUCT:
            fail(errors, f"{product}: maximum {MAXIMUM_REFERENCES_PER_PRODUCT} references, found {count}")

    sha_entries: dict[str, list[str]] = {}
    for entry in entries:
        if entry.get("sha256"):
            sha_entries.setdefault(entry["sha256"], []).append(entry["id"])
    for digest, ids in sha_entries.items():
        if len(ids) > 1:
            fail(errors, f"duplicate SHA-256 {digest}: {', '.join(ids)}")

    research_sha_entries: dict[str, list[str]] = {}
    for entry in entries:
        if entry.get("research_sha256"):
            research_sha_entries.setdefault(entry["research_sha256"], []).append(entry["id"])
    for digest, ids in research_sha_entries.items():
        if len(ids) > 1:
            fail(errors, f"duplicate research SHA-256 {digest}: {', '.join(ids)}")

    near_duplicate_warnings = []
    perceptual = [(entry["id"], entry.get("perceptual_hash")) for entry in entries]
    perceptual = [(entry_id, value) for entry_id, value in perceptual if value]
    for position, (left_id, left_hash) in enumerate(perceptual):
        for right_id, right_hash in perceptual[position + 1:]:
            if len(left_hash) == len(right_hash):
                distance = (int(left_hash, 16) ^ int(right_hash, 16)).bit_count()
                if distance <= 6:
                    near_duplicate_warnings.append(f"{left_id}/{right_id}: dHash distance {distance}")

    catalog_paths = {entry["image_path"] for entry in entries if entry.get("image_path")}
    disk_paths = {
        path.relative_to(ROOT).as_posix()
        for path in IMAGES.rglob("*")
        if path.is_file() and path.name != "README.md"
    }
    for orphan in sorted(disk_paths - catalog_paths):
        fail(errors, f"local image without catalog entry: {orphan}")

    if errors:
        print("Catalog validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    label = "partial" if args.partial else "final"
    print(f"Catalog {label} validation passed: {len(entries)} unique, complete references.")
    print(f"Themes: {dict(themes)}")
    print(f"Families: {dict(families)}")
    print(f"Products: {dict(products)}")
    if near_duplicate_warnings:
        print("Near-duplicate candidates for manual review:")
        for warning in near_duplicate_warnings:
            print(f"- {warning}")
    else:
        print("Near-duplicate detector: no dHash pair at distance <= 6.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
