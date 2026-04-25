# Chunk 001 Pipeline Report

Mode: prompt-only
Max repairs: 2

Writer prompt: `C:\Users\Grimn\Downloads\TCN Campaign\central-nexus-campaign-book\.tmp\chunk_001_prompt.md`

Prompt-only mode selected.
Give the writer prompt to Jules/Gemini/Codex manually, then run this pipeline again after the manuscript is patched.

## Current Validation State
Deterministic validation: FAIL
Canon cross-check: FAIL
Audit prompt: `C:\Users\Grimn\Downloads\TCN Campaign\central-nexus-campaign-book\.tmp\chunk_001_audit_prompt.md`
Repair prompt: `C:\Users\Grimn\Downloads\TCN Campaign\central-nexus-campaign-book\.tmp\chunk_001_repair_prompt.md`

## Next Steps (Manual Mode)
1. Give `C:\Users\Grimn\Downloads\TCN Campaign\central-nexus-campaign-book\.tmp\chunk_001_prompt.md` to Jules/Gemini/Codex to write the chunk.
2. After the manuscript is patched, run this pipeline again.
3. Give `C:\Users\Grimn\Downloads\TCN Campaign\central-nexus-campaign-book\.tmp\chunk_001_audit_prompt.md` to a SEPARATE model for brutal review.
4. Save audit output to `reports/chunk_001_brutal_audit.md`.
5. Run `python scripts/parse_audit_report.py 001` to extract JSON.
6. If audit fails, give `C:\Users\Grimn\Downloads\TCN Campaign\central-nexus-campaign-book\.tmp\chunk_001_repair_prompt.md` to the agent for repair.
7. When all checks pass: `python scripts/update_manifest.py 001`
