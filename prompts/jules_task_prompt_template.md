Use this repository to complete one campaign-book chunk.

Read:

- `AGENTS.md`
- `manifest.json`
- `canon/canon_summary.md`
- `canon/portal_worlds_canon.md`
- `canon/executioner_floor1_canon.md`
- `specs/{{CHUNK_ID}}_*.md`
- `manuscript/The_Central_Nexus_Tower_of_Ascension_Campaign_Book.md`

## Task:

Complete chunk **{{CHUNK_ID}}** according to its spec.

## Rules:

- Update only `manuscript/The_Central_Nexus_Tower_of_Ascension_Campaign_Book.md` unless required by the spec.
- Do not create separate campaign-book files.
- Do not write later chunks.
- Do not claim the entire book is complete.
- Preserve canon.
- Run `python scripts/validate_chunk.py {{CHUNK_ID}}`.
- If validation fails, patch only failed sections.
- Write a report in `reports/`.

## Open a PR with:

- summary of changes
- validation status
- remaining issues, if any
