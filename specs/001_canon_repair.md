# SPEC 001 — Canon Repair: Portal Worlds and the True Floor 1

## Purpose

Repair the master manuscript so it reflects the true campaign structure:

- Central Nexus = MMO-style hub.
- Portal worlds = main early campaign focus.
- Each portal world creates/activates its own D&D 5e character.
- Portal-world items/followers are world-bound.
- The true Spire Floor 1 is The Executioner.
- The Executioner is CR 10 and intentionally lethal.
- Existing survivable Floor 1–3 material must be reclassified as training/simulation material, not actual Tower floors.

## File to Edit

`manuscript/The_Central_Nexus_Tower_of_Ascension_Campaign_Book.md`

Do not create additional manuscript files.

## Required Source Files

Read:

- `canon/canon_summary.md`
- `canon/portal_worlds_canon.md`
- `canon/executioner_floor1_canon.md`
- `manifest.json`
- the current master manuscript

## Required Patch Sections

Add or update the manuscript with these sections:

1. `## Canon Repair Notice: Portal Worlds and the True Floor 1`
2. `## Repaired Campaign Structure`
3. `## How to Use This Book After Canon Repair`
4. `## Portal-World Campaign Architecture`
5. `## Account Identity and Nexus Identity`
6. `## Portal-World Character Slots`
7. `## Items, Followers, and Export Boundaries`
8. `## The True Spire Floor 1: The Executioner`
9. `## What If They Rush the Spire Anyway?`
10. `## Portal World Directory`
11. `## World-Specific Character Creation Procedure`
12. `## Reclassified Material: Spire Seeker Orientation Trials`
13. `## Chunk 001 Handoff Summary`

## Must Establish

The manuscript must clearly state:

- Portal worlds are the main early campaign path.
- The Tower/Spire is not the early leveling dungeon.
- Each portal world has its own character.
- Portal-world items/followers cannot enter other portal worlds.
- Followers are same level as the portal-world character.
- Followers are earned through quest lines.
- The Executioner is the true Floor 1.
- The Executioner is CR 10.
- Low-level Tower attempts are expected to fail or kill characters.
- Existing level-2 Floor 1–3 material is training/simulation material only.

## Must Not Do

Do not:

- write full portal-world campaigns yet
- write the full Executioner adventure yet
- delete useful old content without reclassification
- make The Executioner fair for level 2
- imply Floors 1–3 are safe early progression
- claim the full book is complete

## Required Validation

After editing, run:

```
python scripts/validate_chunk.py 001
```

Patch any failed canon checks.
