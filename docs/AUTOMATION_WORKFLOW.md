# Automation Workflow

This repo supports a chunk-by-chunk automated campaign-book production pipeline.

## Recommended Local Workflow

### Prompt-only mode:

```bash
python scripts/run_chunk_pipeline.py 001 --mode prompt-only
```

This builds:

- `.tmp/chunk_001_prompt.md`
- `.tmp/chunk_001_audit_prompt.md` when ready
- validation reports

Give the generated prompt files to Jules, Gemini CLI, Codex, or another agent.

### Gemini CLI Mode

Set:

```bash
set TCN_LLM_COMMAND=gemini
```

On PowerShell:

```powershell
$env:TCN_LLM_COMMAND="gemini"
```

Then run:

```bash
python scripts/run_chunk_pipeline.py 001 --mode gemini-cli --max-repairs 2
```

If Gemini CLI accepts stdin on your install, the script will try to run the prompt automatically.

If it does not, use prompt-only mode and paste prompts manually.

## Reports

Reports are written to `/reports`.

Important reports:

- `chunk_001_validation.json`
- `chunk_001_canon_cross_check.json`
- `chunk_001_brutal_audit.md`
- `chunk_001_brutal_audit.json`
- `chunk_001_pipeline_report.md`

## Passing Criteria

A chunk passes only when:

- deterministic validation passes
- canon cross-check passes
- brutal audit JSON says `passed: true`
- no fatal or major issues remain
- the chunk handoff exists

## Important

Do not update `manifest.json` until a chunk passes.
