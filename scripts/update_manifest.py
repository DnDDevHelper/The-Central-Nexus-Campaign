#!/usr/bin/env python3
"""
Marks a chunk complete and advances manifest.json.

Usage:
  python scripts/update_manifest.py 001
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    manifest_path = ROOT / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    chunk_id = sys.argv[1] if len(sys.argv) > 1 else manifest["current_chunk"]

    completed = manifest.setdefault("completed_chunks", [])
    if chunk_id not in completed:
        completed.append(chunk_id)

    next_chunks = manifest.get("next_chunks", [])
    next_chunks = [x for x in next_chunks if x != chunk_id]
    manifest["next_chunks"] = next_chunks

    if next_chunks:
        manifest["current_chunk"] = next_chunks[0]
    else:
        manifest["current_chunk"] = ""

    manifest["last_completed_chunk"] = chunk_id
    manifest["last_updated"] = datetime.utcnow().isoformat() + "Z"

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Updated manifest. Completed {chunk_id}. Current chunk: {manifest.get('current_chunk')}")


if __name__ == "__main__":
    main()
