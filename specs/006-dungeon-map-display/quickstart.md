# Quickstart: Dungeon Map Display

**Purpose**: Guide for testing dungeon map display
**Created**: 2026-04-05

## Prerequisites

```bash
uv sync
```

## Basic Usage

```bash
# After exploring a dungeon
uv run notecli map
```

## Expected Output

```
🏰 O Templo da Dor Nebulosa
════════════════════════════

  🪜 Escadaria — Nível 1
    ├── 🔒 Porta 1 → 🚶 Corredor (Nível 1)
  
  🚶 Corredor — Nível 1
    ├── 🔐 Porta 1 → 🏛️ Sala (Nível 1)
    └── 🔒 Porta 2 → 🪜 Escadaria (Nível 2)
  
  🏆 Sala Final — Nível 3
    (sem portas)

── Legenda ──
  Segmentos: 🪜 Escadaria  🚶 Corredor  🏛️ Sala  🏆 Sala Final
  Portas:    🔒 Fechada  ⚠️ Armadilha  🔐 Trancada  ✅ Destrancada
```

## No Session

```bash
uv run notecli map
# → Nenhuma masmorra foi explorada ainda. Execute 'notecli explore' para começar.
```

## Testing

```bash
uv run python -m unittest tests.test_map_display -v
```
