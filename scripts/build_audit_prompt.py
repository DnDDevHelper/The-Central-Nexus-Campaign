#!/usr/bin/env python3
"""
Builds a brutal audit prompt using canon, spec, manuscript excerpt,
validation report, and canon report.

Writes .tmp/chunk_<id>_audit_prompt.md

Usage:
  python scripts/build_audit_prompt.py
  python scripts/build_audit_prompt.py 001
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


def extract_chunk(text: str, chunk_id: str) -> str:
    markers = [
        f"<!-- CHUNK {chunk_id} START -->",
        f"# CHUNK {chunk_id}",
        f"# CHUNK {int(chunk_id)}" if chunk_id.isdigit() else ""
    ]

    start = -1
    for marker in markers:
        if marker and marker in text:
            start = text.find(marker)
            break

    if start == -1:
        return text[:80000]

    # Find next chunk after start.
    following = text.find("<!-- CHUNK ", start + 20)
    if following == -1:
        following = text.find("\n# CHUNK ", start + 20)
    if following == -1:
        return text[start:start + 120000]
    return text[start:following]


def main() -> None:
    manifest = load_manifest()
    chunk_id = sys.argv[1] if len(sys.argv) > 1 else manifest["current_chunk"]

    master = read(ROOT / manifest["master_file"])
    chunk_text = extract_chunk(master, chunk_id)

    canon_context = "\n\n".join([
        read(ROOT / "canon" / "canon_summary.md"),
        read(ROOT / "canon" / "portal_worlds_canon.md"),
        read(ROOT / "canon" / "executioner_floor1_canon.md")
    ])

    validation_report = read(ROOT / "reports" / f"chunk_{chunk_id}_validation.json", "{}")
    canon_report = read(ROOT / "reports" / f"chunk_{chunk_id}_canon_cross_check.json", "{}")
    schema = read(ROOT / "schemas" / "audit_report_schema.json")
    base = read(ROOT / "prompts" / "brutal_auditor_prompt.md")

    prompt = f"""{base}

================================================================================
AUDIT JSON SCHEMA
================================================================================

{schema}

================================================================================
GLOBAL CANON CONTEXT
================================================================================

{canon_context}

================================================================================
CHUNK SPEC
================================================================================

{read(find_spec(chunk_id))}

================================================================================
DETERMINISTIC VALIDATION REPORT
================================================================================

{validation_report}

================================================================================
CANON CROSS-CHECK REPORT
================================================================================

{canon_report}

================================================================================
MANUSCRIPT CHUNK TO AUDIT
================================================================================

{chunk_text}

================================================================================
AUDIT INSTRUCTIONS
================================================================================

Audit this chunk now.

Return:
1. Human-readable Markdown audit.
2. Valid JSON matching the schema.

If there are any fatal or major issues, passed must be false.
"""

    TMP.mkdir(exist_ok=True)
    out = TMP / f"chunk_{chunk_id}_audit_prompt.md"
    out.write_text(prompt, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
