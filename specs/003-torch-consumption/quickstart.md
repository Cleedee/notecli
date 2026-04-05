# Quickstart: Torch Consumption

**Purpose**: Guide for testing torch consumption feature
**Created**: 2026-04-04

## Prerequisites

```bash
uv sync
```

## Test Scenarios

### Scenario 1: Character with torches (normal case)

```bash
uv run notecli explore
```

Expected output includes:
```
🔥 Você acende uma tocha. A escuridão recua.
🗡️ Gnomo Lenhador começa a exploração...
   Tochas: 9 | Magias: 2 (Heal (2), Fireball (1)) | HP: 18/18
```

### Scenario 2: Character with 0 torches

Create a character with 0 torches (manually edit `~/.notecli/characters.json`), then:

```bash
uv run notecli explore
```

Expected output includes:
```
🌑 Suas tochas acabaram! Você está no escuro...
🗡️ Gnomo Mendigo começa a exploração...
   Tochas: 0 | Magias: 0 | HP: 14/14
```

### Scenario 3: Resume session (no torch consumed)

```bash
uv run notecli explore --resume
```

Expected: No torch consumed, session state preserved.

## Run Tests

```bash
uv run python -m unittest tests.test_torch_consumption -v
```
