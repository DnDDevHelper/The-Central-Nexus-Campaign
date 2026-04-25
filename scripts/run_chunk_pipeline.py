#!/usr/bin/env python3
"""
Main orchestrator for the chunk production pipeline.

Supports prompt-only mode and Gemini CLI mode.
Does not require AI command to be configured.
Runs deterministic validators, creates audit and repair prompts,
optionally runs LLM via TCN_LLM_COMMAND, loops up to max repair attempts.

Usage:
  python scripts/run_chunk_pipeline.py 001 --mode prompt-only
  python scripts/run_chunk_pipeline.py 001 --mode gemini-cli --max-repairs 2
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / ".tmp"
REPORTS = ROOT / "reports"


def run(cmd: list[str], allow_fail: bool = False) -> int:
    print(f"\n>>> {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=ROOT)
    if proc.returncode != 0 and not allow_fail:
        raise SystemExit(proc.returncode)
    return proc.returncode


def load_manifest() -> dict:
    return json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))


def write_report(chunk_id: str, lines: list[str]) -> None:
    REPORTS.mkdir(exist_ok=True)
    path = REPORTS / f"chunk_{chunk_id}_pipeline_report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the chunk production pipeline."
    )
    parser.add_argument("chunk_id", nargs="?", help="Chunk id, e.g. 001")
    parser.add_argument(
        "--mode",
        choices=["prompt-only", "gemini-cli"],
        default="prompt-only"
    )
    parser.add_argument("--max-repairs", type=int, default=2)
    parser.add_argument("--auto-update-manifest", action="store_true")
    args = parser.parse_args()

    manifest = load_manifest()
    chunk_id = args.chunk_id or manifest["current_chunk"]

    report = [
        f"# Chunk {chunk_id} Pipeline Report",
        "",
        f"Mode: {args.mode}",
        f"Max repairs: {args.max_repairs}",
        ""
    ]

    # ── 1. Build writer prompt ──────────────────────────────────────────
    run([sys.executable, "scripts/build_prompt.py", chunk_id])
    writer_prompt = TMP / f"chunk_{chunk_id}_prompt.md"
    report.append(f"Writer prompt: `{writer_prompt}`")

    if args.mode == "prompt-only":
        report.append("")
        report.append("Prompt-only mode selected.")
        report.append(
            "Give the writer prompt to Jules/Gemini/Codex manually, "
            "then run this pipeline again after the manuscript is patched."
        )

        # Still run deterministic checks so we know the current state.
        report.append("")
        report.append("## Current Validation State")

        validation_rc = run(
            [sys.executable, "scripts/validate_chunk.py", chunk_id],
            allow_fail=True
        )
        report.append(f"Deterministic validation: {'PASS' if validation_rc == 0 else 'FAIL'}")

        canon_rc = run(
            [sys.executable, "scripts/canon_cross_check.py", chunk_id],
            allow_fail=True
        )
        report.append(f"Canon cross-check: {'PASS' if canon_rc == 0 else 'FAIL'}")

        # Build audit prompt for manual use.
        run([sys.executable, "scripts/build_audit_prompt.py", chunk_id])
        audit_prompt = TMP / f"chunk_{chunk_id}_audit_prompt.md"
        report.append(f"Audit prompt: `{audit_prompt}`")

        # Build repair prompt for manual use.
        run([sys.executable, "scripts/build_repair_prompt.py", chunk_id])
        repair_prompt = TMP / f"chunk_{chunk_id}_repair_prompt.md"
        report.append(f"Repair prompt: `{repair_prompt}`")

        report.append("")
        report.append("## Next Steps (Manual Mode)")
        report.append(f"1. Give `{writer_prompt}` to Jules/Gemini/Codex to write the chunk.")
        report.append(f"2. After the manuscript is patched, run this pipeline again.")
        report.append(
            f"3. Give `{audit_prompt}` to a SEPARATE model for brutal review."
        )
        report.append(
            f"4. Save audit output to `reports/chunk_{chunk_id}_brutal_audit.md`."
        )
        report.append(
            f"5. Run `python scripts/parse_audit_report.py {chunk_id}` to extract JSON."
        )
        report.append(
            f"6. If audit fails, give `{repair_prompt}` to the agent for repair."
        )
        report.append(
            f"7. When all checks pass: `python scripts/update_manifest.py {chunk_id}`"
        )

        write_report(chunk_id, report)
        return

    # ── Automated mode (gemini-cli) ─────────────────────────────────────
    # Add scripts/ to path so llm_command can be imported.
    sys.path.insert(0, str(ROOT / "scripts"))
    from llm_command import run_llm_prompt

    # Try running the writer.
    prompt_text = writer_prompt.read_text(encoding="utf-8")
    out_path = REPORTS / f"chunk_{chunk_id}_writer_output.md"
    ok, msg = run_llm_prompt(prompt_text, out_path, label="writer")
    report.append(msg)

    if not ok:
        report.append(
            "Writer did not run automatically. Complete writer step manually."
        )
        write_report(chunk_id, report)
        return

    # ── 2. Deterministic validation ─────────────────────────────────────
    validation_rc = run(
        [sys.executable, "scripts/validate_chunk.py", chunk_id],
        allow_fail=True
    )
    canon_rc = run(
        [sys.executable, "scripts/canon_cross_check.py", chunk_id],
        allow_fail=True
    )

    # ── 3. Build and run audit ──────────────────────────────────────────
    run([sys.executable, "scripts/build_audit_prompt.py", chunk_id])
    audit_prompt = TMP / f"chunk_{chunk_id}_audit_prompt.md"
    report.append(f"Audit prompt: `{audit_prompt}`")

    audit_out = REPORTS / f"chunk_{chunk_id}_brutal_audit.md"
    ok, msg = run_llm_prompt(
        audit_prompt.read_text(encoding="utf-8"), audit_out, label="auditor"
    )
    report.append(msg)

    audit_rc = 1
    if ok:
        audit_rc = run(
            [sys.executable, "scripts/parse_audit_report.py", chunk_id],
            allow_fail=True
        )

    # ── 4. Repair loop ──────────────────────────────────────────────────
    repair_attempt = 0
    while (
        (validation_rc != 0 or canon_rc != 0 or audit_rc != 0)
        and repair_attempt < args.max_repairs
    ):
        repair_attempt += 1
        report.append(f"Repair attempt {repair_attempt} started.")

        run([sys.executable, "scripts/build_repair_prompt.py", chunk_id])
        repair_prompt = TMP / f"chunk_{chunk_id}_repair_prompt.md"

        ok, msg = run_llm_prompt(
            repair_prompt.read_text(encoding="utf-8"),
            REPORTS / f"chunk_{chunk_id}_repair_{repair_attempt}_output.md",
            label="repair"
        )
        report.append(msg)

        if not ok:
            report.append(
                "Repair did not run automatically. Complete repair manually."
            )
            write_report(chunk_id, report)
            return

        validation_rc = run(
            [sys.executable, "scripts/validate_chunk.py", chunk_id],
            allow_fail=True
        )
        canon_rc = run(
            [sys.executable, "scripts/canon_cross_check.py", chunk_id],
            allow_fail=True
        )
        run([sys.executable, "scripts/build_audit_prompt.py", chunk_id])

        ok, msg = run_llm_prompt(
            audit_prompt.read_text(encoding="utf-8"),
            audit_out,
            label="auditor"
        )
        report.append(msg)

        audit_rc = (
            run(
                [sys.executable, "scripts/parse_audit_report.py", chunk_id],
                allow_fail=True
            )
            if ok
            else 1
        )

    passed = validation_rc == 0 and canon_rc == 0 and audit_rc == 0

    report.append("")
    report.append(f"Final passed: {passed}")

    if passed and args.auto_update_manifest:
        run([sys.executable, "scripts/update_manifest.py", chunk_id])
        report.append("Manifest updated.")

    if not passed:
        report.append(
            "Pipeline stopped with failures. Review reports and repair "
            "manually or increase --max-repairs."
        )

    write_report(chunk_id, report)

    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
