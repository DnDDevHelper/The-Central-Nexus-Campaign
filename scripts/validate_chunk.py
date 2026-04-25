#!/usr/bin/env python3
"""
Validates the master manuscript for a given chunk.

This is intentionally simple and strict.
It checks:
- required headings from the chunk spec
- banned placeholder phrases
- core canon contradictions
- chunk-specific canon requirements

Usage:
  python scripts/validate_chunk.py
  python scripts/validate_chunk.py 001
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parents[1]


GLOBAL_BANNED_PHRASES = [
    "TODO",
    "placeholder",
    "DM decides",
    "insert NPC",
    "insert monster",
    "use an appropriate monster",
    "use a suitable monster",
    "generic faction agent",
    "ask the user",
    "fill this in",
    "to be determined",
    "TBD"
]


CANON_CONTRADICTIONS = [
    "Floor 1 is survivable for prepared 1st- to 3rd-level teams",
    "level-2 Floor 1",
    "level 2 Floor 1",
    "The Threshold That Weighs You is the true Floor 1",
    "The Shortcut That Smiles is the true Floor 2",
    "The Listening Dark is the true Floor 3",
    "The Executioner is not Floor 1",
    "The Tower is the main early campaign path",
    "The Tower is the early leveling path",
    "Floors 1 through 5 are early Act I leveling"
]


CHUNK_REQUIRED_CANON = {
    "001": [
        "Portal worlds are the main early campaign focus",
        "The true Spire Floor 1 is The Executioner",
        "The Executioner is a CR 10",
        "Items and followers from one portal world cannot be used in another portal world",
        "Followers are the same level as the player character from that portal world"
    ],
    "002": [
        "Nexus identity",
        "Portal-world character",
        "Export and Import Rules",
        "Followers",
        "Tower Eligibility"
    ],
    "003": [
        "Portal Plaza",
        "Gate Directory",
        "Alpha",
        "Beta",
        "Gamma",
        "Theta"
    ]
}


def read(path: Path, default: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else default


def load_manifest() -> dict:
    return json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))


def find_spec(chunk_id: str) -> Path:
    matches = sorted((ROOT / "specs").glob(f"{chunk_id}_*.md"))
    if not matches:
        raise FileNotFoundError(f"No spec found for chunk {chunk_id}")
    return matches[0]


def extract_required_headings(spec_text: str) -> list[str]:
    headings = []
    in_required = False

    for line in spec_text.splitlines():
        if line.strip().lower().startswith("## required"):
            in_required = True
            continue

        if in_required and line.startswith("## ") and not line.lower().startswith("## required"):
            # Stop when another major section starts.
            if "required" not in line.lower():
                pass

        match = re.match(r"\d+\.\s+`(.+?)`", line.strip())
        if match:
            headings.append(match.group(1))

    return headings


def validate(chunk_id: str) -> dict:
    manifest = load_manifest()
    master_path = ROOT / manifest["master_file"]
    master = read(master_path)
    spec = read(find_spec(chunk_id))

    required_headings = extract_required_headings(spec)

    missing_headings = [h for h in required_headings if h not in master]
    banned_hits = [p for p in GLOBAL_BANNED_PHRASES if p.lower() in master.lower()]
    contradiction_hits = [p for p in CANON_CONTRADICTIONS if p.lower() in master.lower()]

    required_canon = CHUNK_REQUIRED_CANON.get(chunk_id, [])
    missing_canon = [p for p in required_canon if p.lower() not in master.lower()]

    passed = not missing_headings and not banned_hits and not contradiction_hits and not missing_canon

    return {
        "chunk_id": chunk_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "passed": passed,
        "missing_headings": missing_headings,
        "banned_phrase_hits": banned_hits,
        "canon_contradiction_hits": contradiction_hits,
        "missing_required_canon": missing_canon,
        "master_file": str(master_path.relative_to(ROOT))
    }


def main() -> None:
    manifest = load_manifest()
    chunk_id = sys.argv[1] if len(sys.argv) > 1 else manifest["current_chunk"]

    result = validate(chunk_id)

    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    report_path = reports / f"chunk_{chunk_id}_validation.json"
    report_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))

    if not result["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
