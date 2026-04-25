You are working locally in this repo.

Read `.tmp/chunk_{{CHUNK_ID}}_prompt.md` and complete the task exactly.

After editing:

1. Run `python scripts/validate_chunk.py {{CHUNK_ID}}`
2. If validation fails, repair only the failing sections.
3. Run validation again.
4. Stop when the chunk passes or when you have written a clear report explaining what failed.

- Do not create unrelated files.
- Do not modify unrelated chunks.
