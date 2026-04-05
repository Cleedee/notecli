# Quickstart: Dungeon Segment Generation

**Purpose**: Guide for testing dungeon segment exploration feature
**Created**: 2026-04-05

## Prerequisites

```bash
uv sync
```

## Basic Usage

```bash
uv run notecli explore
```

## Segment Exploration Flow

### Initial Segment

```
🏰 Gerando masmorra...
  Tipo: Templo
  Nome: O Templo da Dor Nebulosa

📖 Você chega à entrada do Templo da Dor Nebulosa.
   [description...]

🪜 Escadaria — Nível 1
   1 porta à frente.
```

### Opening a Door

```
> abrir 1

🚪 Você abre a porta 1...

🚶 Corredor — Nível 1
   2 portas à frente.
```

### Backtracking

```
> voltar

🔙 Você retorna ao segmento anterior...

🪜 Escadaria — Nível 1
   (porta 1 já aberta → Corredor)
   Nenhuma porta restante para abrir.
```

### Exiting the Dungeon

```
> sair

⚠️ Caminho até a entrada: livre de monstros.
Deseja realmente sair da masmorra? (s/n)
> s

🏁 Você sai da masmorra com vida.
   Personagem salvo.
```

## Inspecting State

```bash
cat ~/.notecli/exploration.json | python -m json.tool
```

Look for:
- `segments`: dict of all generated segments
- `current_segment_id`: where the player is
- `visited_stack`: backtrack history
- `max_level`: highest dungeon level reached

## Testing

```bash
uv run python -m unittest tests.test_segment_entities -v
uv run python -m unittest tests.test_transition_tables -v
uv run python -m unittest tests.test_dungeon_graph -v
uv run python -m unittest tests.test_segment_exploration -v
```

## Troubleshooting

### Corrupted exploration session

```bash
rm ~/.notecli/exploration.json
uv run notecli explore
```

### No segments generated

Check that `tables.py` has the 3 transition tables defined with 6 entries each.
