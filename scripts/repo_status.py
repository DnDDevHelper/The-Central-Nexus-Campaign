#!/usr/bin/env python3
"""
Prints current campaign-book automation status.

Usage:
  python scripts/repo_status.py
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    manifest_path = ROOT / "manifest.json"
    if not manifest_path.exists():
        print("manifest.json missing")
        return

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    master_path = ROOT / manifest["master_file"]
    master_exists = master_path.exists()
    master_words = 0

    if master_exists:
        text = master_path.read_text(encoding="utf-8")
        master_words = len(text.split())

    print("# Central Nexus Campaign Book Repo Status")
    print()
    print(f"Project: {manifest.get('project_name')}")
    print(f"Repo version: {manifest.get('repo_version')}")
    print(f"Current chunk: {manifest.get('current_chunk')} — {manifest.get('current_chunk_title')}")
    print(f"Completed chunks: {', '.join(manifest.get('completed_chunks', [])) or 'none'}")
    print(f"Next chunks: {', '.join(manifest.get('next_chunks', [])) or 'none'}")
    print(f"Master manuscript exists: {master_exists}")
    print(f"Master manuscript word count: {master_words}")


if __name__ == "__main__":
    main()
