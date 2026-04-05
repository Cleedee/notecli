# Quickstart: Dungeon Exploration

**Purpose**: Guide for testing and using the dungeon exploration feature
**Created**: 2026-04-04

## Prerequisites

```bash
# Ensure project is set up
uv sync
```

## Basic Usage

### Start a new exploration

```bash
uv run notecli explore
```

This will:
1. Generate a random dungeon (type, name, entrance description)
2. Prompt you to select an existing character or create a new one
3. Begin the exploration session

### Resume an existing session

```bash
uv run notecli explore --resume
```

If an active session exists, you'll be prompted to continue from where you left off.

## Exploring Dungeons

Once inside a dungeon, you'll see:

```
🗡️ Humano Nobre entra no Templo da Dor Nebulosa...
   Tochas: 10 | Magias: 0 | HP: 22/22

Digite 'ajuda' para ver as ações disponíveis.
> _
```

### Available Actions (future implementation)

| Command | Description |
|---------|-------------|
| `ajuda` | Show available commands |
| `explorar` | Move to the next room |
| `tocha` | Light a torch (if dark) |
| `usar <magia>` | Cast a magic spell |
| `status` | Show character and dungeon status |
| `sair` | Save and exit the dungeon |

## Character Management

If you need to create characters before exploring:

```bash
uv run notecli character
```

This opens the character menu where you can:
- View saved characters
- Create new characters with randomized ancestry and profession

## Storage Locations

| Data | Location |
|------|----------|
| Characters | `~/.notecli/characters.json` |
| Exploration session | `~/.notecli/exploration.json` |

### Inspecting session state

```bash
cat ~/.notecli/exploration.json | python -m json.tool
```

## Troubleshooting

### "Nenhum personagem encontrado"

The system will automatically create a new character. If you want more control, run `notecli character` first to create characters manually.

### Corrupted exploration session

If the exploration file is corrupted or missing, the system will start a fresh session:

```bash
# Remove corrupted session
rm ~/.notecli/exploration.json
uv run notecli explore
```

### Character storage issues

```bash
# View raw character data
cat ~/.notecli/characters.json | python -m json.tool
```

## Testing

Run the test suite:

```bash
uv run pytest
# or
uv run python -m unittest discover -s tests
```

Run specific dungeon exploration tests:

```bash
uv run pytest tests/test_dungeon_generation.py
uv run pytest tests/test_dungeon_name.py
uv run pytest tests/test_explore_menu.py
uv run pytest tests/test_exploration_storage.py
```
