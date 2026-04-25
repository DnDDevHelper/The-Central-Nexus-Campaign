# Gemini CLI Workflow

Gemini CLI can be used as a local automation agent.

## Setup

Install Gemini CLI according to the official docs.

Then from this repo:

```bash
python scripts/run_chunk_pipeline.py 001 --mode prompt-only
```

or, if your Gemini CLI supports stdin cleanly:

```powershell
$env:TCN_LLM_COMMAND="gemini"
python scripts/run_chunk_pipeline.py 001 --mode gemini-cli --max-repairs 2
```

## Manual Alternative

Run:

```bash
python scripts/build_prompt.py 001
```

Then open Gemini CLI and say:

> Read `.tmp/chunk_001_prompt.md` and perform the task exactly.
> Edit only the master manuscript.
> Run the validator.
> Repair failed checks.
> Stop after the chunk passes.

## Audit

After Gemini writes the chunk:

```bash
python scripts/validate_chunk.py 001
python scripts/canon_cross_check.py 001
python scripts/build_audit_prompt.py 001
```

Then run the audit prompt through a **separate** model or a separate Gemini CLI session.
