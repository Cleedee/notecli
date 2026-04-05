# Implementation Plan: Dungeon Map Display

**Branch**: `006-dungeon-map-display` | **Date**: 2026-04-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-dungeon-map-display/spec.md`

## Summary

Implementar o comando `notecli map` que lê a sessão de exploração persistida e exibe um mapa textual da masmorra, mostrando todos os segmentos, portas, estados e conexões, com legenda.

## Technical Context

**Language/Version**: Python 3.14+
**Primary Dependencies**: `notecli.cli.storage` (load_exploration), `notecli.entities.segment`, `notecli.entities.door`
**Storage**: `~/.notecli/exploration.json` (já persiste grafo de segmentos)
**Testing**: pytest/unittest (TDD)
**Target Platform**: Linux/macOS terminal (CLI interativo)
**Project Type**: CLI tool (comando subcommand `map`)
**Performance Goals**: Exibição < 100ms
**Constraints**: Sem novas dependências; mapa legível em 80 colunas
**Scale/Scope**: Masmorras geradas proceduralmente com profundidade limitada (até nível 3)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | Novo subcomando `notecli map` com output legível |
| **II. Test-Driven** | ✅ Pass | Testes antes da implementação (TDD) |
| **III. Entity-Driven** | ✅ Pass | Reutiliza `Segment` e `Door` existentes. Nova função `build_map()`. |
| **IV. Observability** | ✅ Pass | Mapa textual com legenda clara |
| **V. Simplicity** | ✅ Pass | Sem novas dependências. Função simples de leitura + formatação. |
| **No new dependencies** | ✅ Pass | Zero novas dependências |
| **Package structure** | ✅ Pass | CLI logic em `main.py` + `cli/map_display.py` |

**Result**: All gates passed. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/006-dungeon-map-display/
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
├── main.py                          # Adicionar roteamento para 'map'
└── cli/
    └── map_display.py               # NOVO: função display_map()
```

**Structure Decision**: Função pura `display_map()` em novo módulo `cli/map_display.py`. `main.py` ganha roteamento para subcomando `map`. Sem mudanças em entidades ou storage — apenas leitura e formatação.

## Research

**Decision 1: Formato do mapa**

**Context**: Precisa ser legível em 80 colunas, mostrar segmentos, portas e estados.

**Decision**: Formato de lista indentada com hierarquia visual:
```
🏰 O Templo da Dor Nebulosa
════════════════════════════

  🪜 Escadaria — Nível 1
    ├── 🔒 Porta 1 → 🚶 Corredor (Nível 1)
  
  🚶 Corredor — Nível 1
    ├── 🔐 Porta 1 → 🏛️ Sala (Nível 1)
    └── 🔒 Porta 2 → 🪜 Escadaria (Nível 2)
  
  ...
  
🏆 Sala Final — Nível 3
    (sem portas)

── Legenda ──
  Segmentos: 🪜 Escadaria  🚶 Corredor  🏛️ Sala  🏆 Sala Final
  Portas:    🔒 Fechada  ⚠️ Armadilha  🔐 Trancada  ✅ Destrancada
```

**Rationale**: Simples, hierárquico, cabe em 80 colunas.
**Alternatives considered**: ASCII art grid — rejeitado: complexo para grafos não-planos. Graphviz — rejeitado: dependência externa.

**Decision 2: Leitura de sessão**

**Context**: Dados já persistidos em `exploration.json`.

**Decision**: Usar `load_exploration()` existente. Se retornar None ou inativo, exibir mensagem "Nenhuma masmorra explorada."

**Rationale**: Reutiliza infraestrutura existente. Simples.

## Data Model

Sem novas entidades. `display_map()` lê `ExplorationSession` → itera `DungeonGraph.segments` → formata texto.

## Quickstart

```bash
uv run notecli map
# → Mapa completo da masmorra com legenda
# ou
# → Nenhuma masmorra foi explorada ainda.
```

## Agent Context Update

Nenhuma nova tecnologia.

## Constitution Check (Post-Design)

*Re-evaluated after Phase 1 design completion.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | `notecli map` subcommand |
| **II. Test-Driven** | ✅ Pass | Testes de mapa e legenda |
| **III. Entity-Driven** | ✅ Pass | Reutiliza entidades existentes |
| **IV. Observability** | ✅ Pass | Mapa legível com legenda |
| **V. Simplicity** | ✅ Pass | 1 novo módulo, ~50 linhas |
| **No new dependencies** | ✅ Pass | Zero |
| **Package structure** | ✅ Pass | `cli/map_display.py` |

**Result**: All gates passed. No violations.
