# Implementation Plan: Enter Room After Opening Door

**Branch**: `008-enter-room-after-door` | **Date**: 2026-04-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/008-enter-room-after-door/spec.md`

## Summary

Modificar o modelo de `Door` para usar 3 atributos independentes (visibilidade, trava, armadilha). Adicionar opção "entrar" após abrir porta Destrancada. Fechar portas após qualquer ação subsequente. Portas já reveladas permitem entrar sem rolagem. Portas Trancadas não abrem sem destruir fechadura.

## Technical Context

**Language/Version**: Python 3.14+
**Primary Dependencies**: `notecli.entities.door` (modificar Door com 3 atributos), `notecli.entities.dungeon` (fechar portas após ação), `notecli.cli.explore_menu` (adicionar "entrar" ao menu)
**Storage**: `~/.notecli/exploration.json` (já persiste portas — adicionar campos `is_locked`, `has_trap`)
**Testing**: pytest/unittest (TDD)
**Target Platform**: Linux/macOS terminal (CLI interativo)
**Project Type**: CLI tool (comando subcommand `explore`)
**Performance Goals**: Operação instantânea
**Constraints**: Sem novas dependências; compatibilidade com sessões existentes (migração de dados)
**Scale/Scope**: Nenhuma mudança na escala — mesma masmorra, nova mecânica de portas

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | Nova opção "entrar" no menu de exploração |
| **II. Test-Driven** | ✅ Pass | TDD: testes antes para Door, enter, close doors |
| **III. Entity-Driven** | ✅ Pass | Door modificada com 3 atributos independentes |
| **IV. Observability** | ✅ Pass | Mensagens de porta fechando, estado resultante |
| **V. Simplicity** | ✅ Pass | 3 atributos booleanos na Door. Sem libs novas. |
| **No new dependencies** | ✅ Pass | Zero |
| **Package structure** | ✅ Pass | Door em `entities/`, lógica em `dungeon.py` e `explore_menu.py` |

**Result**: All gates passed. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/008-enter-room-after-door/
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
└── entities/
    ├── door.py                  # Modificar: adicionar is_locked, has_trap, state transitions
    ├── dungeon.py               # Modificar: close_doors_after_action, enter_room
    └── segment.py               # Sem alteração
```

**Structure Decision**: `Door` ganha novos campos booleanos. Funções `close_opened_doors()` e `enter_room()` em `dungeon.py`. `explore_menu.py` ganha opção "entrar" após abrir porta Destrancada.

## Research

**Decision 1: Door model with 3 independent attributes**

**Context**: Door state was a single enum. Now needs visibilidade (Fechada/Aberta), trava (Trancada/Destrancada), armadilha (Sim/Não).

**Decision**: Door gets `is_open: bool`, `is_locked: bool`, `has_trap: bool`. Display combines these into readable status.

**Rationale**: Clear, explicit, easy to serialize. Alternatives: composite enum with 8 values — rejected: hard to reason about, inflexible.

**Decision 2: Close doors after action**

**Context**: After entering or choosing another action, all opened doors close.

**Decision**: `close_opened_doors(segment)` function — iterates doors, sets `is_open = False` for doors that were open. Keeps `is_locked` and `has_trap` unchanged.

**Rationale**: Simple, one function call. Preserves lock/trap state.

**Decision 3: Already-revealed door allows entry without re-roll**

**Context**: Player knows where door leads after first opening.

**Decision**: If door has `target_segment_id` set and `is_locked = False` and `has_trap = False`, offer "entrar" directly. No re-roll.

**Rationale**: Respects player knowledge. No redundant randomness.

## Data Model

### Door (modified)

**Fields**:
- `is_open` (bool): Porta está fisicamente aberta?
- `is_locked` (bool): Porta está trancada?
- `has_trap` (bool): Porta tem armadilha ativa?
- `target_segment_id` (int | None): Destino da porta (set on first reveal)

**State transitions**:
- Tentar abrir (is_locked=True) → sem mudança, aviso "trancada"
- Abrir fechadura → `is_open=True, is_locked=False`
- Tentar abrir (has_trap=True) → trap triggered, `is_open=True, has_trap=False`
- Tentar abrir (Destrancada) → `is_open=True`
- After action → `is_open=False` (porta fecha, mantém is_locked e has_trap)

### Display Logic

| is_open | is_locked | has_trap | Display |
|---------|-----------|----------|---------|
| False | False | False | 🔒 Fechada |
| False | True | False | 🔐 Fechada + Trancada |
| False | False | True | ⚠️ Fechada + Armadilha |
| True | False | False | ✅ Aberta (entrar) |
| True | True | False | (impossible) |

## Quickstart

```bash
uv run notecli explore
# → Abrir porta → "Porta Destrancada! Entrar? (s/n)"
# → s → "Você entra. Porta fecha atrás."
# → n → "Porta fecha."
```

## Agent Context Update

Nenhuma nova tecnologia.

## Constitution Check (Post-Design)

*Re-evaluated after Phase 1 design completion.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | "entrar" no menu |
| **II. Test-Driven** | ✅ Pass | Testes para Door attributes, close, enter |
| **III. Entity-Driven** | ✅ Pass | Door modificada com 3 atributos |
| **IV. Observability** | ✅ Pass | Mensagens de fechar porta, estado |
| **V. Simplicity** | ✅ Pass | 3 bools + 1 função close |
| **No new dependencies** | ✅ Pass | Zero |
| **Package structure** | ✅ Pass | `entities/door.py`, `entities/dungeon.py` |

**Result**: All gates passed. No violations.
