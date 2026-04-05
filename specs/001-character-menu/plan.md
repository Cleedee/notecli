# Implementation Plan: Character Menu

**Branch**: `001-character-menu` | **Date**: 2026-04-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-character-menu/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Implement the `notecli character` subcommand that opens an interactive terminal menu with two options: (1) view a list of saved characters with details, and (2) create a new character with randomized ancestry (2d6) and profession (2d6). Characters are persisted to a local JSON file. The feature reuses existing domain entities (`PlayerCharacter`, `Ancestry`, `Occupation`), the dice roller, and the complete tables in `tables.py` (both `ANCESTRIES` and `OCCUPATIONS` fully mapped for 2d6 range 2-12).

## Technical Context

**Language/Version**: Python 3.14+
**Primary Dependencies**: Existing `notecli.entities` (PlayerCharacter, Ancestry, Occupation), `notecli.dice.Roller`, `notecli.tables` (ANCESTRIES + OCCUPATIONS fully mapped 2-12), standard library (`json`, `pathlib`, `sys`)
**Storage**: Local JSON file for character persistence (`~/.notecli/characters.json`)
**Testing**: unittest (existing pattern) + pytest compatible
**Target Platform**: Linux terminal (CLI)
**Project Type**: CLI tool
**Performance Goals**: Menu response under 1 second, character list loads under 2 seconds for up to 100 characters
**Constraints**: No external dependencies beyond stdlib for menu/storage; must follow existing entity patterns; no side effects in module imports
**Scale/Scope**: Single-user local tool; up to ~100 characters per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| I. CLI-First | Feature is entirely CLI-driven via `notecli character` | ✅ Pass |
| II. Test-Driven | Tests will be written before implementation for menu, storage, and creation flow | ✅ Pass |
| III. Entity-Driven Design | Reuses existing `PlayerCharacter`, `Ancestry`, `Occupation`; new storage service | ✅ Pass |
| IV. Observability | Menu errors to stderr; structured character summary on creation; clear prompts | ✅ Pass |
| V. Simplicity | No new dependencies; stdlib JSON for storage; no framework overhead | ✅ Pass |

## Project Structure

### Documentation (this feature)

```text
specs/001-character-menu/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (from /speckit.tasks)
```

### Source Code (repository root)

```text
src/notecli/
├── __init__.py
├── main.py                  # Extended: add 'character' subcommand routing
├── dice.py                  # Reused: Roller for 2d6 (ancestry + profession)
├── tables.py                # Reused: ANCESTRIES (2d6, keys 2-12) + OCCUPATIONS (2d6, keys 2-12)
├── cli/                     # NEW: CLI menu and subcommand modules
│   ├── __init__.py
│   ├── character_menu.py    # Interactive menu loop (personagens/novo personagem)
│   └── storage.py           # Character persistence (load/save JSON)
├── entities/
│   ├── __init__.py          # Updated: export new entities if added
│   ├── ancestry.py          # Reused: 11 ancestry instances (SLIMEMAN → HALF_DRAGON)
│   ├── player.py            # Reused: PlayerCharacter dataclass
│   ├── magic.py             # Reused: factory_magic, BASIC_MAGICS
│   └── occupation.py        # Reused: 11 profession instances (BEGGAR → GLADIATOR)

tests/
├── test_character_menu.py   # Menu interaction, input validation, exit flow
├── test_storage.py          # Load/save, empty file, corrupted data
├── test_create_character.py # End-to-end character creation flow
└── (existing tests unchanged)
```

**Structure Decision**: Single project (CLI tool). New `cli/` subpackage for menu logic and storage, keeping CLI routing separate from domain entities. Both `ANCESTRIES` and `OCCUPATIONS` tables in `tables.py` are fully mapped for the 2d6 range (2-12).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

_No violations. All constitution principles satisfied._
