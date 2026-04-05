# Research: Dungeon Exploration Flow

**Purpose**: Resolve technical unknowns and document design decisions for dungeon exploration feature
**Created**: 2026-04-04

## Decision 1: Dungeon Type Definition

**Context**: A spec requires 6 dungeon types, each with a unique entrance description.

**Decision**: Define `DUNGEON_TYPES` in `tables.py` as a dict mapping d6 rolls (1-6) to dataclass-like objects with `name` and `entrance_description` fields, following the same pattern as `ANCESTRIES` and `OCCUPATIONS`.

**Rationale**:
- Consistent with existing table structure (d6 roll → data)
- Reuses `Roller.d6()` for random selection
- Simple dict lookup is O(1) and requires no new dependencies

**Alternatives considered**:
- Enum + separate description table: More complex, requires two lookups
- JSON file with dungeon definitions: Overkill for 6 static entries
- Database/storage: Unnecessary for static game content

## Decision 2: Dungeon Name Generation Pattern

**Context**: Names follow pattern like "O Templo da Dor Nebulosa" — composed from multiple tables.

**Decision**: Implement `DUNGEON_NAME_TABLES` in `tables.py` as three separate lists: `articles`, `substantives`, `modifiers`. Name generation picks one from each table using `random.choice()` and concatenates with fixed prepositions ("de", "da", "do").

**Example structure**:
```python
DUNGEON_NAME_TABLES = {
    "articles": ["O", "A", "As", "Os"],
    "substantives": {
        "temple": ["Templo", "Santuário", "Catedral"],
        "dungeon": ["Masmorra", "Catacumba", "Cripta"],
        ...
    },
    "modifiers": ["da Dor", "da Névoa", "Nebulosa", ...]
}
```

**Rationale**:
- Flexible enough to generate varied, thematic names
- Simple random selection is sufficient for MVP
- Tables can be expanded later without code changes

**Alternatives considered**:
- Markov chain name generation: Overkill, unpredictable results
- Grammar-based generator: Too complex for 6 dungeon types
- Pre-defined name list: Limited variety, not procedural

## Decision 3: Exploration Session Storage

**Context**: FR-009 requires persisting exploration state for recovery.

**Decision**: Extend `cli/storage.py` with `load_exploration()` and `save_exploration()` functions, using `~/.notecli/exploration.json` as storage file. The exploration session stores:
```json
{
  "version": 1,
  "dungeon": {
    "type": "temple",
    "name": "O Templo da Dor Nebulosa",
    "entrance_shown": true,
    "current_room": 0
  },
  "character_index": 2
}
```

**Rationale**:
- Consistent with character storage pattern
- Single file per session (simple, no locking needed for single-user CLI)
- Easy to inspect/debug with `cat ~/.notecli/exploration.json`

**Alternatives considered**:
- In-memory only: Loses state on crash/interrupt
- SQLite: Overkill for single session state
- Pickle: Security risk, not human-readable

## Decision 4: Explore Menu Interaction Pattern

**Context**: Player must choose existing character or create new one.

**Decision**: Implement `explore_menu.py` with a function `select_or_create_character()` that:
1. Loads characters via existing `load_characters()`
2. If none exist, calls existing `create_character()` from `character_menu.py`
3. If exist, displays numbered menu: `1) <name> (<ancestry>)`, `2) ...`, `0) Criar novo`, `q) Sair`
4. Validates input in loop until valid choice

**Rationale**:
- Reuses existing `create_character()` logic (no duplication)
- Consistent with `character_menu.py` interaction patterns
- Simple input loop with error handling

**Alternatives considered**:
- Inline character creation in explore command: Duplicates logic, violates DRY
- Separate subcommand `notecli explore --character <name>`: Less discoverable

## Decision 5: Number of Dungeon Types

**Context**: Spec says "6 tipos" but doesn't define them.

**Decision**: Define 6 thematic dungeon types aligned with NoteQuest's minimalist dungeon exploration theme:
1. **Palácio** — Ancient royal residence, now ruined and treacherous
2. **Cripta** — Burial vault with undead and ancient relics
3. **Tumba** — Sealed tomb with traps and cursed treasures
4. **Santuário** — Sacred place corrupted by dark forces
5. **Templo** — Ancient religious structure with puzzles and divine wrath
6. **Calabouço** — Classic underground prison with desperate inmates

Each with a unique entrance description (2-3 sentences in Portuguese).

**Rationale**:
- Covers classic dungeon crawl archetypes
- Thematically distinct for varied gameplay
- Fits NoteQuest's minimalist aesthetic
