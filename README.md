# The Central Nexus: The Tower of Ascension — Campaign Book Automation Repo

This repository is a chunked production pipeline for a massive Dungeons & Dragons 5e campaign book.

The final manuscript lives at:

**manuscript/The_Central_Nexus_Tower_of_Ascension_Campaign_Book.md**

## Core Campaign Structure

- The Central Nexus is the hub.
- The portal worlds are the main early campaign content.
- The Spire/Tower is the lethal ascent challenge.
- The true Spire Floor 1 is **The Executioner**, a CR 10 extreme-threat boss that low-level characters are not expected to defeat.

## Recommended Workflow

1. Put source notes/PDF transcriptions into `/canon`.
2. Edit `manifest.json` to set the current chunk.
3. Run:
   ```
   python scripts/build_prompt.py 001
   ```
4. Give `.tmp/chunk_001_prompt.md` to Jules, Gemini CLI, Codex, or another agent.
5. Let the agent patch the master manuscript.
6. Run:
   ```
   python scripts/validate_chunk.py 001
   ```
7. If validation fails, give the repair prompt to the agent.
8. When validation passes, run:
   ```
   python scripts/update_manifest.py 001
   ```

## Useful Commands

Show repo state:
```
python scripts/repo_status.py
```

Build current chunk prompt:
```
python scripts/build_prompt.py
```

Validate current chunk:
```
python scripts/validate_chunk.py
```

Extract latest handoff:
```
python scripts/extract_handoff.py
```

Update manifest after a passing chunk:
```
python scripts/update_manifest.py
```

## How to Use With Jules

Create a new Jules task using the prompt generated in `.tmp/`.

Jules should:
- modify only the master manuscript unless instructed otherwise
- run the validator
- patch only failed sections
- produce a report

## How to Use With Gemini CLI

From the repo root:
```
python scripts/build_prompt.py 001
gemini < .tmp/chunk_001_prompt.md
python scripts/validate_chunk.py 001
```

Or open Gemini CLI interactively and tell it:

> "Read .tmp/chunk_001_prompt.md and perform the task exactly. Edit only the master manuscript. Run the validator. Repair failed checks. Stop after the chunk passes."

## Current Priority

The immediate priority is **001_canon_repair**.

That chunk must repair the mistaken early-Tower progression and restore the portal-world campaign structure.

## Automated Pipeline

This repo now supports an orchestrated chunk pipeline.

**Prompt-only mode:**
```
python scripts/run_chunk_pipeline.py 001 --mode prompt-only
```

**Gemini CLI mode:**
```bash
set TCN_LLM_COMMAND=gemini
python scripts/run_chunk_pipeline.py 001 --mode gemini-cli --max-repairs 2
```

**PowerShell:**
```powershell
$env:TCN_LLM_COMMAND="gemini"
python scripts/run_chunk_pipeline.py 001 --mode gemini-cli --max-repairs 2
```

The pipeline performs:

1. writer prompt creation
2. deterministic validation
3. canon cross-check
4. brutal audit prompt creation
5. optional automated LLM audit
6. repair prompt creation
7. optional repair loop
8. final reports

**Do not advance the manifest until all checks pass.**

See `docs/AUTOMATION_WORKFLOW.md`, `docs/JULES_WORKFLOW.md`, and `docs/GEMINI_CLI_WORKFLOW.md` for detailed guides.
