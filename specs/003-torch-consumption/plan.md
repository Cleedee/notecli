# Implementation Plan: Torch Consumption on Exploration Start

**Branch**: `003-torch-consumption` | **Date**: 2026-04-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-torch-consumption/spec.md`

## Summary

Ao iniciar uma nova sessão de exploração via `notecli explore`, consumir 1 tocha do estoque do personagem, ativar a luz e exibir mensagem com estoque restante. Se sem tochas, exibir aviso e iniciar no escuro. Não consumir ao retomar via `--resume`.

## Technical Context

**Language/Version**: Python 3.14+
**Primary Dependencies**: `notecli.entities.player.PlayerCharacter` (já possui `consume_torch()`, `torches`, `light_on`), `notecli.cli.explore_menu` (ponto de integração)
**Storage**: `~/.notecli/exploration.json` (já persiste `light_on` e `torches` indiretamente via `character_index`)
**Testing**: pytest/unittest (mesma base existente em `tests/`)
**Target Platform**: Linux/macOS terminal (CLI interativo)
**Project Type**: CLI tool (comando subcommand `explore`)
**Performance Goals**: N/A (operação instantânea)
**Constraints**: Reutilizar `PlayerCharacter.consume_torch()` existente; sem novas dependências
**Scale/Scope**: 1 operação por sessão de exploração

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | Funcionalidade acessível via `notecli explore`, output legível |
| **II. Test-Driven** | ✅ Pass | Testes escritos antes da implementação (TDD) |
| **III. Entity-Driven** | ✅ Pass | Reutiliza `PlayerCharacter` existente, sem novas entidades |
| **IV. Observability** | ✅ Pass | Mensagens claras em stdout, avisos em stderr quando aplicável |
| **V. Simplicity** | ✅ Pass | Reutiliza `consume_torch()` existente, 1 linha de código nova no explore_menu |
| **No new dependencies** | ✅ Pass | Zero novas dependências |
| **Package structure** | ✅ Pass | Modificação apenas em `cli/explore_menu.py` e testes |

**Result**: All gates passed. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/003-torch-consumption/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (minimal — CLI contract update)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/notecli/
├── cli/
│   └── explore_menu.py              # Modificar: chamar consume_torch() ao iniciar sessão
└── entities/
    └── player.py                    # Existente (consume_torch já implementado)

tests/
└── test_torch_consumption.py        # NOVO: Testes de consumo de tocha na exploração
```

**Structure Decision**: Modificação mínima em `explore_menu.py` — chamar `pc.consume_torch()` após selecionar/criar personagem e antes de salvar a sessão. Testes dedicados em `test_torch_consumption.py`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (nenhuma) | — | — |

## Research

**Decision 1: Reutilizar `PlayerCharacter.consume_torch()` existente**

O método `consume_torch()` já existe em `player.py` e faz exatamente o necessário: decrementa `torches` em 1, define `light_on = True` e imprime mensagem. Basta chamá-lo no momento certo.

**Rationale**: YAGNI — não há motivo reimplementar lógica existente.
**Alternatives considered**: Criar função dedicada no `explore_menu` — rejeitado por duplicar lógica.

## Data Model

Nenhuma nova entidade. O campo `torches` e `light_on` de `PlayerCharacter` são os únicos afetados.

**State transition**:
- `torches: N` → `torches: N-1` (se N > 0)
- `light_on: False` → `light_on: True` (se N > 0)
- Se N == 0: nenhum change, aviso exibido

## Quickstart

```bash
# Com tochas
uv run notecli explore
# → "🔥 Você acende uma tocha. A escuridão recua."
# → Status mostra Tochas: 9

# Sem tochas (crie personagem com 0 tochas manualmente para testar)
uv run notecli explore
# → "🌑 Suas tochas acabaram! Você está no escuro..."
```

## Agent Context Update

Nenhuma nova tecnologia. Reutiliza stack existente.

## Constitution Check (Post-Design)

*Re-evaluated after Phase 1 design completion.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | Sem alterações na interface CLI |
| **II. Test-Driven** | ✅ Pass | Testes dedicados em `test_torch_consumption.py` |
| **III. Entity-Driven** | ✅ Pass | Nenhuma entidade nova, reutiliza PlayerCharacter |
| **IV. Observability** | ✅ Pass | Mensagens de sucesso/aviso claras |
| **V. Simplicity** | ✅ Pass | 1 chamada de função adicionada ao explore_menu |
| **No new dependencies** | ✅ Pass | Zero novas dependências |
| **Package structure** | ✅ Pass | Apenas `explore_menu.py` modificado |

**Result**: All gates passed. No violations.
