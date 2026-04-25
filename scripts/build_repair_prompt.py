#!/usr/bin/env python3
"""
Combines validation + canon + LLM audit reports into a repair prompt.

Writes .tmp/chunk_<id>_repair_prompt.md

Usage:
  python scripts/build_repair_prompt.py
  python scripts/build_repair_prompt.py 001
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / ".tmp"


def read(path: Path, default: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else default


def load_manifest() -> dict:
    return json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))


def find_spec(chunk_id: str) -> Path:
    matches = sorted((ROOT / "specs").glob(f"{chunk_id}_*.md"))
    if not matches:
        raise FileNotFoundError(f"No spec found for chunk {chunk_id}")
    return matches[0]


def main() -> None:
    manifest = load_manifest()
    chunk_id = sys.argv[1] if len(sys.argv) > 1 else manifest["current_chunk"]

    canon_context = "\n\n".join([
        read(ROOT / "canon" / "canon_summary.md"),
        read(ROOT / "canon" / "portal_worlds_canon.md"),
        read(ROOT / "canon" / "executioner_floor1_canon.md")
    ])

    repair_base = read(ROOT / "prompts" / "automated_repair_prompt.md")
    validation_report = read(ROOT / "reports" / f"chunk_{chunk_id}_validation.json", "{}")
    canon_report = read(ROOT / "reports" / f"chunk_{chunk_id}_canon_cross_check.json", "{}")
    brutal_report = read(ROOT / "reports" / f"chunk_{chunk_id}_brutal_audit.md", "")

    prompt = f"""{repair_base}

================================================================================
MASTER FILE
================================================================================

{manifest["master_file"]}

================================================================================
CHUNK SPEC
================================================================================

{read(find_spec(chunk_id))}

================================================================================
CANON CONTEXT
================================================================================

{canon_context}

================================================================================
DETERMINISTIC VALIDATION REPORT
================================================================================

{validation_report}

================================================================================
CANON CROSS-CHECK REPORT
================================================================================

{canon_report}

================================================================================
BRUTAL AUDIT REPORT
================================================================================

{brutal_report}

================================================================================
REPAIR TASK
================================================================================

Patch the master manuscript directly.

Repair only the assigned chunk and any directly related status/table-of-contents
references needed for canon consistency.

After patching, stop.
"""

    TMP.mkdir(exist_ok=True)
    out = TMP / f"chunk_{chunk_id}_repair_prompt.md"
    out.write_text(prompt, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
