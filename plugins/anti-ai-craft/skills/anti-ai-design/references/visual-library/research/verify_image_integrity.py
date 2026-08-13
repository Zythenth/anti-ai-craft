#!/usr/bin/env python3
"""Verify that every catalog image opens and matches recorded dimensions."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    entries = [json.loads(line) for line in (ROOT / "catalog.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    errors = []
    for entry in entries:
        path = ROOT / entry["image_path"]
        with Image.open(path) as image:
            actual = image.size
            expected = (entry["dimensions"]["width"], entry["dimensions"]["height"])
            if actual != expected:
                errors.append(f"{entry['id']}: expected {expected}, found {actual}")
            image.verify()
    if errors:
        raise SystemExit("Image integrity failed:\n- " + "\n- ".join(errors))
    print(f"Image integrity passed: {len(entries)} files opened; all dimensions match the catalog.")


if __name__ == "__main__":
    main()
