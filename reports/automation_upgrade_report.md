# Automation Upgrade Report

**Date:** 2026-04-25
**Repo:** `The-Central-Nexus-Campaign`
**URL:** https://github.com/DnDDevHelper/The-Central-Nexus-Campaign

## Files Added

### schemas/
- `audit_report_schema.json` — JSON schema for structured LLM audit reports
- `canon_audit_schema.json` — JSON schema for canon cross-reference audits

### prompts/
- `brutal_auditor_prompt.md` — Adversarial audit prompt with structured JSON output
- `canon_cross_examiner_prompt.md` — Canon cross-examination prompt
- `automated_repair_prompt.md` — Surgical repair prompt
- `orchestrator_system_prompt.md` — Pipeline orchestrator system prompt

### scripts/
- `run_chunk_pipeline.py` — Main orchestrator (prompt-only and gemini-cli modes)
- `canon_cross_check.py` — Deterministic canon scanner
- `build_audit_prompt.py` — Builds brutal audit prompts
- `build_repair_prompt.py` — Builds targeted repair prompts
- `llm_command.py` — Central LLM command utility (graceful fallback)
- `parse_audit_report.py` — Extracts JSON from LLM audit markdown

### .github/workflows/
- `validate-chunk.yml` — GitHub Actions CI for PR validation

### docs/
- `AUTOMATION_WORKFLOW.md` — Full automation workflow guide
- `JULES_WORKFLOW.md` — Jules-specific workflow
- `GEMINI_CLI_WORKFLOW.md` — Gemini CLI workflow

## Files Updated

- `README.md` — Added Automated Pipeline section
- `AGENTS.md` — Added Automated Pipeline Rules section
- `manifest.json` — Added `automation` config block (chunk status unchanged)

## Commands Run

| Command | Result |
|---------|--------|
| `python scripts/repo_status.py` | ✅ Success — 115,556-word manuscript, chunk 001 |
| `python scripts/run_chunk_pipeline.py 001 --mode prompt-only` | ✅ Success — All prompts generated |

## Pipeline Output

The pipeline generated:

| File | Status |
|------|--------|
| `.tmp/chunk_001_prompt.md` | ✅ Built |
| `.tmp/chunk_001_audit_prompt.md` | ✅ Built |
| `.tmp/chunk_001_repair_prompt.md` | ✅ Built |
| `reports/chunk_001_validation.json` | ✅ Written — FAIL (expected) |
| `reports/chunk_001_canon_cross_check.json` | ✅ Written — FAIL (expected) |
| `reports/chunk_001_pipeline_report.md` | ✅ Written |

## Validation Status

Chunk 001 validation **correctly fails** — the canon repair pass has not been executed yet.

- **Missing headings:** 7 required sections not yet written
- **Missing canon phrases:** 4 required canon statements not yet in manuscript
- **Canon contradictions found:** 0 ✅
- **Banned phrases found:** 0 ✅

## Next Steps

### Exact next command:
```powershell
cd "c:\Users\Grimn\Downloads\TCN Campaign\central-nexus-campaign-book"
python scripts/run_chunk_pipeline.py 001 --mode prompt-only
```

### Then:
Give `.tmp/chunk_001_prompt.md` to Jules or Gemini CLI to perform the canon repair pass.

### After Jules finishes:
```powershell
python scripts/run_chunk_pipeline.py 001 --mode prompt-only
```

That second run builds the brutal audit prompt and reports. Use a **separate** model/session for the audit so the writer is not grading itself.
