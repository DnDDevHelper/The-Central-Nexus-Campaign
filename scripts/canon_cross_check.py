#!/usr/bin/env python3
"""
Deterministic canon cross-check scanner.

Checks master manuscript for required canon phrases and known contradictions.
Writes reports/chunk_<id>_canon_cross_check.json.

Usage:
  python scripts/canon_cross_check.py
  python scripts/canon_cross_check.py 001
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_CANON_BY_CHUNK = {
    "001": [
        "Portal worlds are the main early campaign focus",
        "The true Spire Floor 1 is The Executioner",
        "The Executioner is a CR 10",
        "Items and followers from one portal world cannot be used in another portal world",
        "Followers are the same level as the player character from that portal world",
        "Spire Seeker Orientation Trials"
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
        "World Gate Directory",
        "Alpha",
        "Beta",
        "Gamma",
        "Theta"
    ]
}


CONTRADICTIONS = [
    "Floor 1 is survivable for prepared 1st- to 3rd-level teams",
    "Floor 1 is survivable for level 2",
    "level-2 Floor 1",
    "level 2 Floor 1",
    "The Threshold That Weighs You is the true Floor 1",
    "The Shortcut That Smiles is the true Floor 2",
    "The Listening Dark is the true Floor 3",
    "The Executioner is not Floor 1",
    "The Executioner is optional Floor 1",
    "The Tower is the main early campaign path",
    "The Tower is the early leveling path",
    "Floors 1 through 5 are early Act I leveling",
    "portal-world followers can freely enter other portal worlds",
    "items from one portal world can be used in any other portal world"
]


def load_manifest() -> dict:
    return json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))


def main() -> None:
    manifest = load_manifest()
    chunk_id = sys.argv[1] if len(sys.argv) > 1 else manifest.get("current_chunk", "001")

    master_path = ROOT / manifest["master_file"]
    if not master_path.exists():
        raise FileNotFoundError(master_path)

    text = master_path.read_text(encoding="utf-8")
    lower = text.lower()

    required = REQUIRED_CANON_BY_CHUNK.get(chunk_id, [])
    missing = [x for x in required if x.lower() not in lower]
    contradictions = [x for x in CONTRADICTIONS if x.lower() in lower]

    result = {
        "chunk_id": chunk_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "passed": not missing and not contradictions,
        "required_checked": required,
        "missing_required_canon": missing,
        "contradictions_found": contradictions,
        "master_file": manifest["master_file"]
    }

    out = ROOT / "reports" / f"chunk_{chunk_id}_canon_cross_check.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))

    if not result["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
