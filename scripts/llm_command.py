#!/usr/bin/env python3
"""
Central utility for optionally running a local CLI LLM command.

Default command is read from env var TCN_LLM_COMMAND.
If no command is configured, writes prompt file and tells user to run manually.
Supports stdin piping.
"""

from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path
from typing import Optional


def run_llm_prompt(prompt: str, output_path: Path, label: str = "llm") -> tuple[bool, str]:
    """
    Runs an external LLM command if TCN_LLM_COMMAND is set.

    Example environment variable:
      TCN_LLM_COMMAND="gemini"

    This function pipes the prompt to stdin and captures stdout.

    If no command is configured, it writes the prompt to output_path.with_suffix(".prompt.md")
    and returns False with instructions.
    """
    command = os.environ.get("TCN_LLM_COMMAND", "").strip()

    prompt_path = output_path.with_suffix(".prompt.md")
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(prompt, encoding="utf-8")

    if not command:
        msg = (
            f"No TCN_LLM_COMMAND configured. Prompt written to {prompt_path}. "
            f"Run it manually with Jules/Gemini/Codex, then place output at {output_path} if needed."
        )
        return False, msg

    args = shlex.split(command)

    try:
        proc = subprocess.run(
            args,
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=60 * 60
        )
    except FileNotFoundError:
        return False, f"Command not found: {command}. Prompt written to {prompt_path}."
    except subprocess.TimeoutExpired:
        return False, f"Command timed out: {command}. Prompt written to {prompt_path}."

    combined = ""
    if proc.stdout:
        combined += proc.stdout
    if proc.stderr:
        combined += "\n\n--- STDERR ---\n\n" + proc.stderr

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(combined, encoding="utf-8")

    if proc.returncode != 0:
        return False, f"{label} command exited with {proc.returncode}. Output written to {output_path}."

    return True, f"{label} output written to {output_path}."
