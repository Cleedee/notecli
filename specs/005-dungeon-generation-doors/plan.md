# Implementation Plan: Dungeon Pre-Generation and Door Mechanics

**Branch**: `005-dungeon-generation-doors` | **Date**: 2026-04-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-dungeon-generation-doors/spec.md`

## Summary

Substituir geração incremental de segmentos por pré-geração completa da masmorra. Adicionar entidade `Door` com 4 estados (Fechada, Armadilha, Trancada, Destrancada) e rolagem d6 ao abrir. Portas trancadas exigem "Abrir Fechadura" que consome 1 tocha. Criar 6 tabelas de armadilhas (1 por tipo de masmorra). Remover consumo de tocha ao entrar em segmento.

## Technical Context

**Language/Version**: Python 3.14+
**Primary Dependencies**: Standard library (`random`, `enum`), `notecli.entities.segment` (modificado para Door), `notecli.entities.dungeon` (pré-geração), `notecli.tables` (novas tabelas de armadilhas)
**Storage**: `~/.notecli/exploration.json` (estendido para persistir estado de portas)
**Testing**: pytest/unittest (TDD)
**Target Platform**: Linux/macOS terminal (CLI interativo)
**Project Type**: CLI tool (comando subcommand `explore`)
**Performance Goals**: Pré-geração completa < 100ms
**Constraints**: Sem novas dependências; modificar entidades existentes (Segment, DungeonGraph); retrocompatibilidade com dados salvos
**Scale/Scope**: Masmorras geradas proceduralmente com profundidade limitada (até Sala Final no nível 3)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | Interação via `notecli explore` com ações `abrir`, `destrancar`, `voltar`, `sair` |
| **II. Test-Driven** | ✅ Pass | TDD para Door, DoorState, trap tables, pré-geração, CLI |
| **III. Entity-Driven** | ✅ Pass | Nova entidade `Door`, `DoorState` em `entities/`. `Segment` modificado. |
| **IV. Observability** | ✅ Pass | Output: estado da porta, armadilha acionada, tocha consumida |
| **V. Simplicity** | ✅ Pass | Reutiliza estrutura existente. Door substitui `connected_segments`. Sem libs novas. |
| **No new dependencies** | ✅ Pass | Zero novas dependências |
| **Package structure** | ✅ Pass | `entities/door.py`, `entities/segment.py` modificado, `tables.py` estendido |

**Result**: All gates passed. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/005-dungeon-generation-doors/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/notecli/
├── tables.py                        # Adicionar: 6 trap tables
├── cli/
│   └── explore_menu.py              # Modificar: remover torch consumption on enter, add door mechanics
└── entities/
    ├── door.py                      # NOVO: Door, DoorState
    ├── segment.py                   # Modificar: replace connected_segments with list[Door]
    └── dungeon.py                   # Modificar: pre-generate full dungeon, place Final Room
```

**Structure Decision**: Nova entidade `Door` em `entities/door.py`. `Segment` substitui `connected_segments` por `doors: list[Door]`. `DungeonGraph` ganha método `generate_full_dungeon()` que pré-gera todos os segmentos. `explore_menu.py` remove `pc.consume_torch()` on segment entry, adiciona door roll e lockpick action.

## Research

**Decision 1: Pré-geração vs geração incremental**

**Context**: A feature anterior gerava segmentos sob demanda ao abrir portas. Agora a masmorra inteira deve existir antes da exploração.

**Decision**: Implementar `generate_full_dungeon(graph)` que expande recursivamente a partir do segmento inicial até encontrar a Sala Final (nível 3 ou leaf node). Usa BFS com limite de profundidade para evitar loops infinitos.

**Rationale**: Garante que Sala Final sempre exista e que todas as portas possam ser abertas. Facilita persistência e debug.

**Alternatives considered**: Manter geração incremental + scan para Final Room — rejeitado por complexidade e risco de masmorras sem saída.

**Decision 2: Door substitui connected_segments**

**Context**: `Segment` atualmente tem `connected_segments: list[(door_idx, target_id)]`.

**Decision**: `Door` dataclass com `index`, `state`, `target_segment_id`, `trap_result`. `Segment.doors: list[Door]`.

**Rationale**: Door encapsula estado + destino. Compatível com serialização JSON.

**Decision 3: Rolagem de porta (d6)**

**Context**: 1 = Armadilha, 2-3 = Trancada, 4-6 = Destrancada.

**Decision**: Função `roll_door()` retorna `DoorState`. Rolagem única por porta — estado persistido após primeira abertura.

**Rationale**: Simples, determinístico, testável.

**Decision 4: Tabelas de armadilhas**

**Context**: 6 tabelas × 6 entradas, uma por tipo de masmorra. Entradas serão placeholders nesta feature.

**Decision**: Definir `TRAP_TABLES: dict[str, list[str]]` em `tables.py` com chaves = nomes de tipos de masmorra. Valores = listas de 6 strings placeholder.

**Rationale**: Estrutura pronta para feature futura sem adicionar complexidade agora.

## Data Model

### Entity: DoorState (Enum)

- `FECHADA` — Porta ainda não aberta
- `ARMADILHA` — Rolagem = 1, armadilha acionada
- `TRANCADA` — Rolagem = 2-3, precisa de tocha para destrancar
- `DESTRANCADA` — Rolagem = 4-6, segmento revelado

### Entity: Door

- `index` (int): Índice da porta no segmento (0-based)
- `state` (DoorState): Estado atual
- `target_segment_id` (int | None): ID do segmento de destino
- `trap_result` (str | None): Resultado da armadilha (placeholder por enquanto)

### Entity: Segment (modificado)

- Remove: `connected_segments: list[(int, int)]`
- Add: `doors: list[Door]` — inicializado com `doors_count` portas no estado FECHADA

### Entity: DungeonGraph (modificado)

- Add: `generate_full_dungeon()` — gera todos os segmentos até Sala Final
- Remove: geração incremental em `open_door()`

## Quickstart

```bash
uv run notecli explore
# → Masmorra gerada: O Templo da Dor Nebulosa
# → 🪜 Escadaria — Nível 1
# → 1 porta (fechada)
# > abrir 1
# → 🎲 Rolagem: 4 — Porta Destrancada!
# → 🚶 Corredor — Nível 1
```

## Agent Context Update

Nenhuma nova tecnologia.

## Constitution Check (Post-Design)

*Re-evaluated after Phase 1 design completion.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | Ações: abrir, destrancar, voltar, sair |
| **II. Test-Driven** | ✅ Pass | Testes para Door, DoorState, roll_door, pre-generation, trap tables |
| **III. Entity-Driven** | ✅ Pass | `Door`, `DoorState` novas. `Segment` modificado. |
| **IV. Observability** | ✅ Pass | Rolagem exibida, estado da porta claro, aviso de tocha |
| **V. Simplicity** | ✅ Pass | Door substitui connected_segments. Sem libs novas. |
| **No new dependencies** | ✅ Pass | Zero |
| **Package structure** | ✅ Pass | `entities/door.py`, `segment.py`, `dungeon.py` |

**Result**: All gates passed. No violations.
