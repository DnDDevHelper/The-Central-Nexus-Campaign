# Jules Workflow

Jules is best used as an asynchronous GitHub PR worker.

## Recommended Process

1. Make sure the repo is pushed to GitHub.

2. Run locally:
   ```bash
   python scripts/build_prompt.py 001
   ```

3. Give Jules `.tmp/chunk_001_prompt.md`.

4. Tell Jules:
   > Complete the assigned chunk.
   > Update only `manuscript/The_Central_Nexus_Tower_of_Ascension_Campaign_Book.md`.
   > Run `python scripts/validate_chunk.py 001`.
   > Run `python scripts/canon_cross_check.py 001`.
   > If validation fails, patch only failed sections.
   > Write `reports/chunk_001_jules_report.md`.
   > Open a PR.

5. After Jules opens the PR, run:
   ```bash
   python scripts/build_audit_prompt.py 001
   ```

6. Give the audit prompt to a **separate** LLM or run it with Gemini CLI.

7. Merge only after validation, canon check, and brutal audit pass.

## Why Separate Audit?

The writer should not be trusted to judge itself alone.
The audit should be adversarial, canon-aware, and evidence-based.
