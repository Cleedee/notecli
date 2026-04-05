# Data Model: Torch Consumption

**Purpose**: Document entities affected by torch consumption feature
**Created**: 2026-04-04

## Entity: PlayerCharacter (existing, fields affected)

**Fields modified**:
- `torches` (int): Decrementado em 1 ao iniciar exploração (mínimo 0)
- `light_on` (bool): Definido como `True` quando tocha é consumida com sucesso

**State transitions**:
- `torches: N, light_on: False` → `torches: N-1, light_on: True` (se N > 0)
- `torches: 0, light_on: False` → `torches: 0, light_on: False` (sem tochas, aviso exibido)

**Validation**:
- `torches` nunca pode ser negativo (mínimo 0)
- `torches` máximo é 10

## Method: PlayerCharacter.consume_torch() (existing)

**Behavior**:
- Se `torches > 0`: decrementa, ativa luz, imprime mensagem de sucesso
- Se `torches == 0`: imprime mensagem de aviso (escuro)

**Used by**: `explore_menu.py` ao iniciar nova sessão de exploração
