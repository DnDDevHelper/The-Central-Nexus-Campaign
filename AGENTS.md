# AGENTS.md — Central Nexus Campaign Book Automation

## Project Purpose

This repository exists to produce one massive, polished Dungeons & Dragons 5e campaign book:

**manuscript/The_Central_Nexus_Tower_of_Ascension_Campaign_Book.md**

The book must be written chunk by chunk, validated chunk by chunk, and repaired surgically when validation fails.

## Critical Canon

- The Central Nexus is an MMO-style hub, not merely a city before a normal dungeon.
- The portal worlds are the main early campaign focus.
- Each portal world is effectively its own D&D 5e campaign path, potentially levels 1–20.
- When a player enters a portal world, they create or activate a new D&D 5e character specifically for that portal world.
- That portal-world character can:
  - adventure in that portal world
  - return to the Central Nexus
  - eventually attempt the Spire/Tower
- Items and followers from one portal world cannot be used in another portal world.
- Items and followers from a portal world may be usable in the Central Nexus and Spire/Tower only under the world-specific export rules.
- Followers are earned through quest lines. Followers have full names, histories, motives, relationships, and current situations. Followers are the same level as the player character from that portal world.
- The true Spire Floor 1 is The Executioner.
- The Executioner is a lethal CR 10 extreme-threat boss and must not be softened into a level-2 tutorial.
- Low-level parties that attempt the true Floor 1 should be at extreme risk of death, retreat, extraction failure, or public consequence.
- The early campaign should direct players toward portal worlds, allies, followers, items, tactical intelligence, and preparation before serious Tower attempts.

## Work Rules for AI Agents

When assigned a chunk:

1. Read `manifest.json`.
2. Read relevant files in `/canon`.
3. Read the relevant `/specs/<chunk>.md`.
4. Read the existing master manuscript.
5. Update only `manuscript/The_Central_Nexus_Tower_of_Ascension_Campaign_Book.md` unless the task explicitly asks for other files.
6. Do not rewrite unrelated chunks.
7. Do not create separate manuscript files.
8. Do not claim the whole campaign book is complete.
9. At the end of each chunk, include a handoff summary.
10. Run `python scripts/validate_chunk.py <chunk_id>`.
11. If validation fails, patch only the failing material.
12. Write a report in `/reports`.

## Quality Standard

This is not a lore note project. This is a campaign-book production pipeline.

Every generated campaign-book chunk must be:

- playable
- specific
- internally consistent
- table-usable
- balanced for D&D 5e where mechanics are involved
- explicit about player-facing vs DM-facing information
- clear about canon vs optional material

Do not leave:

- placeholders
- TODOs
- "DM decides"
- "insert NPC here"
- "use an appropriate monster"
- "as needed"
- "as appropriate"
- unresolved canon gaps
- false claims of completion

## Important Safety / Table Design Rules

- Do not force player discomfort.
- Do not require real-life confession or trauma exposure.
- Character secrets must remain player-consented.
- PvP, betrayal, and binding deals between PCs require table consent.
- The campaign can include dangerous legal systems, debt, and death risk, but it must be designed as dramatic pressure, not gotcha punishment.

## Jules / Gemini CLI Notes

Jules should use this file to understand project conventions.

Gemini CLI should treat this repo like a local writing/build pipeline:

1. inspect files
2. edit the master manuscript
3. run validation scripts
4. patch failed validation
5. stop after the assigned chunk

## Automated Pipeline Rules

When using automation, agents must respect this sequence:

1. Write or repair one chunk only.
2. Run deterministic validation: `python scripts/validate_chunk.py <chunk_id>`
3. Run canon cross-check: `python scripts/canon_cross_check.py <chunk_id>`
4. Run brutal audit (separate model recommended).
5. Repair only failed sections.
6. Re-run validation.
7. Stop after pass or after max repair attempts.

The writer agent is not allowed to be the only judge of its own work.

The audit must be evidence-based and include quotes or references to the manuscript/canon where possible.

A chunk is not complete until:

- deterministic validation passes
- canon cross-check passes
- brutal audit passes
- required handoff exists
