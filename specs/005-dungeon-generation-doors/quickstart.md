# Quickstart: Dungeon Pre-Generation and Door Mechanics

**Purpose**: Guide for testing door mechanics and dungeon pre-generation
**Created**: 2026-04-05

## Prerequisites

```bash
uv sync
```

## Basic Usage

```bash
uv run notecli explore
```

## Door Mechanics

### Opening a Door

```
🪜 Escadaria — Nível 1
   1 porta (fechada)

> abrir 1

🎲 Rolagem: 4 — Porta Destrancada!
🚶 Corredor — Nível 1
   2 portas (fechadas)
```

### Locked Door + Lockpicking

```
> abrir 1

🎲 Rolagem: 2 — Porta Trancada!
   Use 'destrancar 1' para abrir (consome 1 tocha).

> destrancar 1

🔥 Você acende uma tocha para forçar a fechadura...
🚶 Corredor — Nível 1
   Tochas: 9
```

### Trap Triggered

```
> abrir 1

🎲 Rolagem: 1 — Armadilha!
   [trap description placeholder]
🚶 Corredor — Nível 1
```

## Inspecting State

```bash
cat ~/.notecli/exploration.json | python -m json.tool
```

Look for:
- `doors`: list of door objects with state
- `segments`: all pre-generated segments

## Testing

```bash
uv run python -m unittest tests.test_door -v
uv run python -m unittest tests.test_trap_tables -v
uv run python -m unittest tests.test_dungeon_pregen -v
```

## Troubleshooting

### Corrupted exploration session

```bash
rm ~/.notecli/exploration.json
uv run notecli explore
```
