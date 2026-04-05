# Implementation Plan: Dungeon Segment Generation

**Branch**: `004-dungeon-segments` | **Date**: 2026-04-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-dungeon-segments/spec.md`

## Summary

Implementar geração procedural de segmentos de masmorra (escadaria, corredor, sala) conectados por portas, com 3 tabelas de transição de 6 opções cada. Sistema de níveis (cada escadaria +1 nível), Sala Final no nível 3 ou como último segmento. Retrocesso via pilha de visitados e opção de sair se caminho livre.

## Technical Context

**Language/Version**: Python 3.14+
**Primary Dependencies**: Standard library (`random`, `enum`), `notecli.entities.dungeon` (Dungeon, generate_dungeon reutilizados), `notecli.dice.Roller`, `notecli.cli.explore_menu`, `notecli.cli.storage`
**Storage**: `~/.notecli/exploration.json` (estendido para persistir grafo de segmentos, nível atual, pilha de visitados)
**Testing**: pytest/unittest (TDD)
**Target Platform**: Linux/macOS terminal (CLI interativo)
**Project Type**: CLI tool (comando subcommand `explore`)
**Performance Goals**: Geração de segmento < 10ms (lookup de tabela + random)
**Constraints**: Sem novas dependências externas; entidades em `entities/`; grafo em memória com persistência JSON
**Scale/Scope**: 3 tipos de segmentos, 3 tabelas × 6 opções, grafo de segmentos sem limite fixo (limitado pela sessão do jogador)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | Interação via `notecli explore` com menu interativo de portas e retrocesso |
| **II. Test-Driven** | ✅ Pass | TDD: testes antes da implementação para entidades, tabelas, geração e CLI |
| **III. Entity-Driven** | ✅ Pass | Novas entidades `Segment`, `SegmentType`, `TransitionTable` em `entities/` |
| **IV. Observability** | ✅ Pass | Output estruturado: tipo, nível, portas. Erros em stderr |
| **V. Simplicity** | ✅ Pass | Sem novas dependências. Grafo simples com dict de segmentos. Pilha para retrocesso. |
| **No new dependencies** | ✅ Pass | Apenas `enum` da standard library |
| **Package structure** | ✅ Pass | Entidades em `entities/`, CLI em `cli/`, tabelas em `tables.py` |

**Result**: All gates passed. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/004-dungeon-segments/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI interaction contract)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/notecli/
├── main.py                          # Sem alteração (já roteia para explore)
├── tables.py                        # Adicionar: 3 tabelas de transição
├── cli/
│   ├── explore_menu.py              # Modificar: fluxo de exploração de segmentos
│   └── storage.py                   # Estender: persistir grafo de segmentos
└── entities/
    ├── dungeon.py                   # Modificar: adicionar grafo de segmentos
    ├── segment.py                   # NOVO: Segment, SegmentType, TransitionTable
    └── dungeon_name.py              # Existente (não alterado)

tests/
├── test_segment_entities.py         # Testes de Segment, SegmentType
├── test_transition_tables.py        # Testes das 3 tabelas de transição
├── test_dungeon_graph.py            # Testes de geração de grafo de segmentos
└── test_segment_exploration.py      # Testes do CLI de exploração com segmentos
```

**Structure Decision**: Nova entidade `Segment` em `entities/segment.py`. `Dungeon` é estendido para conter um grafo de segmentos (dict de id→Segment) e rastrear segmento atual, nível e pilha de retrocesso. Tabelas de transição adicionadas a `tables.py`. `explore_menu.py` ganha loop de interação: ver segmento → escolher porta → gerar/visitar próximo segmento.

## Research

**Decision 1: Representação do grafo de segmentos**

**Context**: Segmentos são conectados por portas. Precisamos rastrear quais portas foram abertas e quais segmentos existem.

**Decision**: Usar um dict `{segment_id: Segment}` onde cada `Segment` tem uma lista `connected_segments` de `(door_index, target_segment_id)`. IDs são ints auto-incrementados.

**Rationale**: Simples, O(1) lookup, serializável para JSON. Alternativa com objetos aninhados seria complexa para persistência.

**Alternatives considered**: Lista plana com referências por índice — rejeitada por menos clara. Graph library externa — rejeitada (YAGNI).

**Decision 2: Tabelas de transição**

**Context**: 3 tabelas com 6 opções cada, com distribuição específica.

**Decision**: Definir como listas de dicts em `tables.py`:
```python
STAIRCASE_TRANSITIONS = [
    {"type": "corredor", "doors": 1},
    {"type": "corredor", "doors": 2},
    {"type": "corredor", "doors": 3},
    ...  # 6 entries total
]
```
Seleção via `random.choice(table)` ou `Roller.d6() - 1`.

**Rationale**: Consistente com `DUNGEON_TYPES` existente. Fácil de ajustar.

**Decision 3: Retrocesso (backtracking)**

**Context**: Jogador precisa voltar pelo caminho percorrido.

**Decision**: Pilha (stack) de `visited_segment_ids`. `push` ao avançar, `pop` ao retroceder. Último item = segmento de entrada.

**Rationale**: Pilha é a estrutura natural para "voltar pelo caminho percorrido". Simples e eficiente.

**Decision 4: Sala Final**

**Context**: Aparece no nível 3 OU como último segmento se não houve escadarias suficientes.

**Decision**: Verificar `current_level >= 3` ao gerar destino de escadaria → gerar `SegmentType.SALA_FINAL`. Para fallback: quando não há mais segmentos conectados e nível < 3, marcar último segmento como Sala Final.

**Rationale**: Lógica simples no ponto de geração. Sem estado extra.

## Data Model

Entidades detalhadas em `data-model.md`. Resumo:

- **SegmentType**: Enum `ESCADARIA`, `CORREDOR`, `SALA`, `SALA_FINAL`
- **Segment**: `id`, `type`, `level`, `doors_count`, `connected_segments: [(door_idx, target_id)]`, `is_final_room`, `has_monsters`
- **Dungeon**: `segments: dict[int, Segment]`, `current_segment_id`, `max_level`, `visited_stack: list[int]`
- **TransitionTable**: 3 listas de 6 dicts `{type, doors}`

## Quickstart

```bash
uv run notecli explore
# → Escadaria — Nível 1
# → 1 porta à frente
# > abrir 1
# → Corredor — Nível 1
# → 2 portas à frente
# > abrir 2
# → Sala — Nível 1 (sem portas — caminho sem saída)
# > voltar
# → Corredor — Nível 1
# → 1 porta restante
```

## Agent Context Update

Nenhuma nova tecnologia. Adicionar `enum.Enum` ao stack existente.

## Constitution Check (Post-Design)

*Re-evaluated after Phase 1 design completion.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | Menu interativo: abrir porta, voltar, sair |
| **II. Test-Driven** | ✅ Pass | 4 arquivos de teste planejados |
| **III. Entity-Driven** | ✅ Pass | `Segment`, `SegmentType`, `TransitionTable` em `entities/` |
| **IV. Observability** | ✅ Pass | Tipo + nível + portas em cada interação |
| **V. Simplicity** | ✅ Pass | Dict + pilha + enum. Zero dependências novas |
| **No new dependencies** | ✅ Pass | Apenas `enum` |
| **Package structure** | ✅ Pass | `entities/segment.py`, `cli/explore_menu.py` |

**Result**: All gates passed. No violations.
