#!/usr/bin/env python3
"""
Extracts a JSON object from an LLM audit markdown file.

Saves to reports/chunk_<id>_brutal_audit.json.
Exits 1 if no JSON found or if parsed JSON says passed=false.

Usage:
  python scripts/parse_audit_report.py 001
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def extract_json(text: str) -> dict:
    # Try fenced json first.
    fenced = re.findall(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    for block in fenced:
        try:
            return json.loads(block)
        except json.JSONDecodeError:
            pass

    # Fallback: first large object.
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    raise ValueError("No valid JSON object found in audit output.")


def main() -> None:
    chunk_id = sys.argv[1] if len(sys.argv) > 1 else "001"

    md_path = ROOT / "reports" / f"chunk_{chunk_id}_brutal_audit.md"
    if not md_path.exists():
        raise FileNotFoundError(md_path)

    data = extract_json(md_path.read_text(encoding="utf-8"))

    out = ROOT / "reports" / f"chunk_{chunk_id}_brutal_audit.json"
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(json.dumps(data, indent=2))

    if not data.get("passed", False):
        sys.exit(1)


if __name__ == "__main__":
    main()
