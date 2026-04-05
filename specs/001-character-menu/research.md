# Research: Character Menu

## Decision 1: Character Storage Format

**Decision**: JSON file (`~/.notecli/characters.json`)

**Rationale**: JSON is natively supported by Python's standard library (`json` module), requires no additional dependencies, and is human-readable for debugging. The existing codebase already uses JSON-serializable dataclasses. JSON supports arrays naturally for storing multiple character records.

**Alternatives considered**:
- **YAML**: More readable but requires `pyyaml` dependency (violates Simplicity principle)
- **SQLite**: Overkill for single-user local storage; adds `sqlite3` complexity
- **Pickle**: Not human-readable; security risks with arbitrary code execution
- **One file per character**: Simpler per-file but harder to list all characters atomically

## Decision 2: Interactive Menu Implementation

**Decision**: Simple `input()` loop with `match`/`case` (Python 3.10+)

**Rationale**: The menu is straightforward (2 options + exit). Python 3.14 supports `match`/`case` natively. No external library needed. Error handling via try/except for invalid input and `KeyboardInterrupt` for Ctrl+C.

**Alternatives considered**:
- **prompt_toolkit**: Rich features but adds external dependency (violates Simplicity)
- **curses**: Unix-only, complex setup, overkill for numbered menu
- **textual**: Modern TUI framework but heavy dependency for a 2-option menu
- **click/typer CLI frameworks**: Good for subcommands but not for interactive loops

## Decision 3: Ancestry and Profession Tables (2d6)

**Decision**: Both `ANCESTRIES` and `OCCUPATIONS` in `tables.py` are fully mapped for 2d6 range (2-12). Roll `2d6` via `Roller.roll("2d6")`, then direct dictionary lookup.

**Rationale**: The tables already cover all 2d6 outcomes (2-12). `ANCESTRIES` has 11 entries (SLIMEMAN through HALF_DRAGON). `OCCUPATIONS` has 11 entries (BEGGAR through GLADIATOR, with LUMBERJACK at both 10 and 11). No unmapped results — no re-roll logic needed.

**Alternatives considered**:
- **Re-roll on unmapped results**: Would be needed if tables were sparse, but they are complete
- **User choice**: Changes the NoteQuest game design which uses randomization

## Decision 4: Character Storage Path

**Decision**: `~/.notecli/characters.json` (user home directory)

**Rationale**: Follows Unix convention for application config/data in hidden home directories. Survives project directory changes. Easy to backup. Does not pollute the project tree with user data.

**Alternatives considered**:
- **`characters.json` in project root**: Breaks if user runs from different directory; mixes user data with source code
- **`~/.local/share/notecli/`** (XDG): More correct per freedesktop spec but adds complexity; `~/.notecli/` is simpler and sufficient for this scope
- **Environment variable configurable**: Good for future but YAGNI for v1

## Decision 5: Character Serialization Strategy

**Decision**: Manual `to_dict()` / `from_dict()` for `PlayerCharacter` with magic reconstruction via `factory_magic()`

**Rationale**: The `PlayerCharacter` contains `magics` (list of dicts with callables) which are NOT JSON-serializable. The serialization will store magic name and uses. On load, `factory_magic()` reconstructs the callable. `Occupation` has an `applier` callable — the stored `starting_weapon` string suffices for persistence; the callable is re-obtained from `OCCUPATIONS` table on load if needed.

**Alternatives considered**:
- **`dataclasses.asdict()`**: Simpler but produces same non-serializable issue with callables
- **Custom JSON encoder subclass**: Cleaner API but more complex; manual dict is simpler

## Decision 6: Menu Input Validation

**Decision**: Accept numeric input (1, 2, 0/q to exit); reject anything else with error message and re-display

**Rationale**: Matches the spec's edge case requirement. Simple and unambiguous. `0` and `q` both exit for convenience.

**Alternatives considered**:
- **Arrow key navigation**: Better UX but requires `curses` or external library
- **Any key as shortcut**: Ambiguous for menus with more options later
