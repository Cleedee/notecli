# NoteCLI — Project Context

## Overview

**NoteCLI** is a Python CLI tool that automates gameplay for **NoteQuest**, a minimalist dungeon exploration game. Players create characters with randomly determined ancestry and profession, then explore procedurally generated dungeons based on tables of dungeon types and room types. Dungeons contain traps, monsters, treasures, and more.

Future plans include AI-assisted gameplay strategies using the `agno` library.

## Tech Stack

| Area | Technology |
|------|------------|
| **Language** | Python 3.14+ |
| **Package Manager** | uv (uv_build backend) |
| **AI Dependency** | agno>=2.5.8 |
| **Entry Point** | notecli → notecli.main:main |

## Project Structure

```
notecli/
├── main.py                      # Legacy entry point (use `uv run notecli` instead)
├── pyproject.toml               # Project config, dependencies, scripts
├── uv.lock                      # Locked dependency versions
├── README.md                    # Project description
├── .specify/                    # Feature spec templates and constitution
│   └── memory/constitution.md   # Development principles (5 core principles)
├── src/notecli/
│   ├── __init__.py              # Package init (empty, exports only)
│   ├── main.py                  # CLI entry point (sys.argv-based routing)
│   ├── dice.py                  # Dice roller (supports NdX+N notation)
│   ├── tables.py                # Ancestry lookup table (d6 roll → Ancestry)
│   └── entities/
│       ├── __init__.py          # Package init (empty)
│       ├── ancestry.py          # Ancestry dataclass + apply functions (7 ancestries)
│       ├── player.py            # PlayerCharacter dataclass (HP, magics, torches)
│       └── magic.py             # Magic system factory (Light, Heal, Freeze)
└── tests/                       # Test directory (pytest/unittest)
    ├── test_pc_basic.py         # Tests for Human, Gnome, Dwarf ancestry application
    ├── test_create_pc.py        # Tests for character creation (Slimeman, Vagaloide)
    ├── test_pc_elf.py           # Tests for Elf ancestry (magic use, mocked dice rolls)
    ├── test_pc_faerie.py        # Tests for Faerie ancestry (5 magic uses)
    └── test_use_magic.py        # Tests for magic usage, torch consumption, factory
```

## Key Commands

```bash
# Run the CLI
uv run notecli              # Shows welcome message
uv run notecli explore      # Enters dungeon exploration mode

# Install/update dependencies
uv sync

# Run tests
uv run pytest
# Or directly with unittest:
uv run python -m unittest discover -s tests
```

## Testing

The project uses **unittest** (compatible with pytest). Tests are organized by ancestry/feature:

| File | What it tests |
|------|--------------|
| `test_create_pc.py` | Character creation: Slimeman (HP=10), Vagaloide (HP=16 + Light magic with 3 uses) |
| `test_pc_basic.py` | Human (HP=20), Gnome (HP=14 + 3 magic uses), Dwarf ancestry application |
| `test_pc_elf.py` | Elf ancestry with mocked dice roll for magic randomization |
| `test_pc_faerie.py` | Faerie ancestry: 5 random magic uses total |
| `test_use_magic.py` | Light magic usage, torch consumption, factory_magic, multiple use depletion |

**Test patterns**:
- Uses `unittest.TestCase` with `setUp` for PlayerCharacter fixtures
- `unittest.mock.patch` for dice roll determinism (e.g., `test_pc_elf.py`)
- Tests validate HP values, magic counts, ancestry names, and state changes

## Domain Model

### PlayerCharacter
- **name**, **occupation** (string)
- **ancestry** (one of 7 types)
- **health_points**, **hp_current** (int)
- **torches** (max 10), **light_on** (bool)
- **magics** (list of magic dicts with name, applier, uses)

### Ancestry System
Each ancestry has a name, base HP, and an apply function that modifies the character:

| d6 Roll | Ancestry | HP | Special |
|---------|----------|----|---------|
| 2 | Homem-Gosma | 10 | — |
| 3 | Vagalóide | 16 | Starts with Light magic (3 uses) |
| 4 | Fada | 8 | 5 random magics |
| 5 | Gnomo | 14 | 3 random magics |
| 6 | Elfo | 16 | 1 random magic |
| 7 | Humano | 20 | — |
| 8 | Anão | 18 | — |

### Magic System
- **Light**: Turns on light (`light_on = True`)
- **Heal**: Restores 5 HP (capped at max HP)
- **Freeze**: Placeholder (no effect yet)
- Magic distribution on d6: 1=Heal, 2-3=Light, 4=Freeze, 5-6=Light

### Dice Roller
- Supports standard notation: `NdX` or `NdX+N` / `NdX-N`
- `Roller.d6()` is a shortcut for the most common roll
- Minimum result is always 1

## Development Conventions

The project follows the principles defined in `.specify/memory/constitution.md`:

1. **CLI-First**: Every feature must be usable from the command line
2. **Test-Driven (NON-NEGOTIABLE)**: TDD with Red-Green-Refactor cycle
3. **Entity-Driven Design**: Domain entities in `src/notecli/entities/`
4. **Observability & Debuggability**: Clear output, errors to stderr, structured logs
5. **Simplicity & YAGNI**: No premature abstractions or dependencies

### Code Style
- Python 3.14+ features available
- Dataclasses for domain entities
- Pure functions where possible
- No side effects in `__init__.py` files
- Portuguese language for domain names (ancestries, etc.), English for code

### File Organization
- Entities go in `src/notecli/entities/`
- CLI logic in `src/notecli/main.py` (or subcommand modules)
- Utility modules (dice, tables) at `src/notecli/` root

## Current State

The project is in early development. Core domain entities (ancestry, player, magic, dice) are implemented but the CLI currently has minimal functionality (`explore` command shows a placeholder message). Key features yet to implement:

- Character creation CLI flow
- Procedural dungeon generation
- Room exploration with traps/monsters/treasures
- Combat system
- AI-assisted strategies (future)

## Testing Status

The project has **5 test files** covering ancestry application, character creation, magic usage, and torch consumption. Tests use `unittest.TestCase` (pytest-compatible).

**Coverage**:
- ✅ Ancestry application (Human, Gnome, Dwarf, Slimeman, Vagaloide, Elf, Faerie)
- ✅ Magic system (Light, Heal, Freeze factory, use/depletion)
- ✅ Torch consumption
- ⚠️ Character creation CLI flow (no tests yet)
- ⚠️ Dungeon generation (not implemented yet)
- ⚠️ Room exploration (not implemented yet)
- ⚠️ Combat system (not implemented yet)

Per the constitution's Test-Driven principle, new features MUST have tests before implementation.

## Active Technologies
- Python 3.14+ + Existing `notecli.entities` (PlayerCharacter, Ancestry, Occupation), `notecli.dice.Roller`, `notecli.tables` (ANCESTRIES + OCCUPATIONS fully mapped 2-12), standard library (`json`, `pathlib`, `sys`) (001-character-menu)
- Local JSON file for character persistence (`~/.notecli/characters.json`) (001-character-menu)
- Python 3.14+ + Standard library (input, sys, random), `notecli.entities` (PlayerCharacter, Ancestry), `notecli.dice.Roller`, `notecli.tables`, `notecli.cli.storage` (reutilizado) (002-dungeon-explore)
- `~/.notecli/characters.json` (existente) + `~/.notecli/exploration.json` (novo, para sessão de exploração) (002-dungeon-explore)
- Python 3.14+ + `notecli.entities.player.PlayerCharacter` (já possui `consume_torch()`, `torches`, `light_on`), `notecli.cli.explore_menu` (ponto de integração) (003-torch-consumption)
- `~/.notecli/exploration.json` (já persiste `light_on` e `torches` indiretamente via `character_index`) (003-torch-consumption)
- Python 3.14+ + Standard library (`random`, `enum`), `notecli.entities.dungeon` (Dungeon, generate_dungeon reutilizados), `notecli.dice.Roller`, `notecli.cli.explore_menu`, `notecli.cli.storage` (004-dungeon-segments)
- `~/.notecli/exploration.json` (estendido para persistir grafo de segmentos, nível atual, pilha de visitados) (004-dungeon-segments)
- Python 3.14+ + Standard library (`random`, `enum`), `notecli.entities.segment` (modificado para Door), `notecli.entities.dungeon` (pré-geração), `notecli.tables` (novas tabelas de armadilhas) (005-dungeon-generation-doors)
- `~/.notecli/exploration.json` (estendido para persistir estado de portas) (005-dungeon-generation-doors)
- Python 3.14+ + `notecli.cli.storage` (load_exploration), `notecli.entities.segment`, `notecli.entities.door` (006-dungeon-map-display)
- `~/.notecli/exploration.json` (já persiste grafo de segmentos) (006-dungeon-map-display)
- Python 3.14+ + `notecli.cli.explore_menu` (modificar fluxo), `notecli.cli.storage` (load/save/clear exploration), `notecli.entities.dungeon` (DungeonGraph) (007-save-quit-dungeon)
- `~/.notecli/exploration.json` (já persiste grafo; `active` controla retomada) (007-save-quit-dungeon)
- Python 3.14+ + `notecli.entities.door` (modificar Door com 3 atributos), `notecli.entities.dungeon` (fechar portas após ação), `notecli.cli.explore_menu` (adicionar "entrar" ao menu) (008-enter-room-after-door)
- `~/.notecli/exploration.json` (já persiste portas — adicionar campos `is_locked`, `has_trap`) (008-enter-room-after-door)

## Recent Changes
- 001-character-menu: Added Python 3.14+ + Existing `notecli.entities` (PlayerCharacter, Ancestry, Occupation), `notecli.dice.Roller`, `notecli.tables` (ANCESTRIES + OCCUPATIONS fully mapped 2-12), standard library (`json`, `pathlib`, `sys`)
