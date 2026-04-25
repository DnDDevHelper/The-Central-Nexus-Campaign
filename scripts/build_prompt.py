#!/usr/bin/env python3
"""
Builds a chunk prompt for Jules, Gemini CLI, Codex, or another agent.

Usage:
  python scripts/build_prompt.py
  python scripts/build_prompt.py 001
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
    path = ROOT / "manifest.json"
    if not path.exists():
        raise FileNotFoundError("manifest.json not found")
    return json.loads(path.read_text(encoding="utf-8"))


def find_spec(chunk_id: str) -> Path:
    matches = sorted((ROOT / "specs").glob(f"{chunk_id}_*.md"))
    if not matches:
        raise FileNotFoundError(f"No spec found for chunk {chunk_id}")
    return matches[0]


def extract_latest_handoff(master_text: str) -> str:
    markers = [
        "## Chunk Handoff Summary",
        "## CHUNK Handoff Summary",
        "## Handoff Summary",
        "## Chunk 001 Handoff Summary",
        "## Chunk 002 Handoff Summary",
        "## Chunk 003 Handoff Summary",
        "## Chunk 004 Handoff Summary",
        "## Chunk 005 Handoff Summary",
        "## Chunk 006 Handoff Summary"
    ]

    last_pos = -1
    last_marker = None
    for marker in markers:
        pos = master_text.rfind(marker)
        if pos > last_pos:
            last_pos = pos
            last_marker = marker

    if last_pos == -1:
        return "No prior handoff found."

    return master_text[last_pos:last_pos + 6000]


def main() -> None:
    manifest = load_manifest()
    chunk_id = sys.argv[1] if len(sys.argv) > 1 else manifest["current_chunk"]

    master_file = ROOT / manifest["master_file"]
    spec_file = find_spec(chunk_id)

    canon_files = [
        ROOT / "canon" / "canon_summary.md",
        ROOT / "canon" / "portal_worlds_canon.md",
        ROOT / "canon" / "executioner_floor1_canon.md"
    ]

    canon_context = "\n\n".join(
        f"# SOURCE: {path.relative_to(ROOT)}\n\n{read(path)}"
        for path in canon_files
    )

    master_text = read(master_file)
    previous_handoff = extract_latest_handoff(master_text)

    base_prompt = read(ROOT / "prompts" / "base_writer_prompt.md")
    chunk_title = manifest.get("current_chunk_title", "Unknown Chunk")
    if chunk_id != manifest.get("current_chunk"):
        chunk_title = spec_file.stem

    prompt = base_prompt
    prompt = prompt.replace("{{MASTER_FILE}}", manifest["master_file"])
    prompt = prompt.replace("{{CHUNK_ID}}", chunk_id)
    prompt = prompt.replace("{{CHUNK_TITLE}}", chunk_title)
    prompt = prompt.replace("{{CANON_PRIORITIES}}", "\n".join(f"- {x}" for x in manifest["canon_priorities"]))
    prompt = prompt.replace("{{CANON_CONTEXT}}", canon_context)
    prompt = prompt.replace("{{CHUNK_SPEC}}", read(spec_file))
    prompt = prompt.replace("{{PREVIOUS_HANDOFF}}", previous_handoff)

    TMP.mkdir(exist_ok=True)
    out = TMP / f"chunk_{chunk_id}_prompt.md"
    out.write_text(prompt, encoding="utf-8")

    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
