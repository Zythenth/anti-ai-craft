#!/usr/bin/env python3
"""Fetch verbatim SPDX license texts required by the versioned image set."""

from __future__ import annotations

import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "LICENSES"
LICENSES = [
    "AGPL-3.0-only",
    "Apache-2.0",
    "CC-BY-3.0",
    "CC-BY-3.0-US",
    "CC-BY-4.0",
    "CC-BY-SA-4.0",
    "CC0-1.0",
    "GFDL-1.2-only",
    "GPL-3.0-only",
    "MIT",
    "MPL-2.0",
]


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for license_id in LICENSES:
        url = f"https://raw.githubusercontent.com/spdx/license-list-data/main/text/{license_id}.txt"
        request = urllib.request.Request(url, headers={"User-Agent": "anti-ai-craft-license-fetch"})
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read()
        destination = OUTPUT / f"{license_id}.txt"
        destination.write_bytes(payload)
        print(f"{license_id}: {len(payload)} bytes")


if __name__ == "__main__":
    main()
