#!/usr/bin/env python3
"""
Extracts the latest handoff summary from the master manuscript.

Usage:
  python scripts/extract_handoff.py
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_manifest() -> dict:
    return json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))


def main() -> None:
    manifest = load_manifest()
    master_path = ROOT / manifest["master_file"]

    if not master_path.exists():
        print("Master manuscript not found.")
        return

    text = master_path.read_text(encoding="utf-8")

    candidates = [
        "## Chunk Handoff Summary",
        "## Handoff Summary",
        "## Chunk 001 Handoff Summary",
        "## Chunk 002 Handoff Summary",
        "## Chunk 003 Handoff Summary",
        "## Chunk 004 Handoff Summary",
        "## Chunk 005 Handoff Summary",
        "## Chunk 006 Handoff Summary"
    ]

    pos = -1
    marker = None
    for c in candidates:
        p = text.rfind(c)
        if p > pos:
            pos = p
            marker = c

    if pos == -1:
        print("No handoff found.")
        return

    out = text[pos:pos + 8000]
    output_path = ROOT / ".tmp" / "latest_handoff.md"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(out, encoding="utf-8")

    print(f"Extracted latest handoff using marker {marker} to {output_path}")


if __name__ == "__main__":
    main()
