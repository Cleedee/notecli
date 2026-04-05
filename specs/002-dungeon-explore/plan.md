# Implementation Plan: Dungeon Exploration Flow

**Branch**: `002-dungeon-explore` | **Date**: 2026-04-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-dungeon-explore/spec.md`

## Summary

Implementar o fluxo de exploração de masmorras no comando `notecli explore`: geração aleatória de tipo, nome composto e descrição de entrada, seguida de seleção ou criação de personagem. A funcionalidade reutiliza o sistema de persistência de personagens existente e segue os padrões CLI já estabelecidos no `character_menu`.

## Technical Context

**Language/Version**: Python 3.14+
**Primary Dependencies**: Standard library (input, sys, random), `notecli.entities` (PlayerCharacter, Ancestry), `notecli.dice.Roller`, `notecli.tables`, `notecli.cli.storage` (reutilizado)
**Storage**: `~/.notecli/characters.json` (existente) + `~/.notecli/exploration.json` (novo, para sessão de exploração)
**Testing**: pytest/unittest (mesma base existente em `tests/`)
**Target Platform**: Linux/macOS terminal (CLI interativo)
**Project Type**: CLI tool (comando subcommand `explore`)
**Performance Goals**: Resposta inicial < 1s (geração instantânea de dados de tabela)
**Constraints**: Interação via stdin/stdout, sem interface gráfica, compatível com pipes/redirecionamento
**Scale/Scope**: 6 tipos de masmorra, 3 tabelas de nomes (~20-30 itens cada), persistência de 1 sessão ativa

## Constitution Check (Post-Design)

*Re-evaluated after Phase 1 design completion.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | `notecli explore` com `--resume` option, output estruturado, menu interativo |
| **II. Test-Driven** | ✅ Pass | 4 arquivos de teste planejados: `test_dungeon_generation.py`, `test_dungeon_name.py`, `test_explore_menu.py`, `test_exploration_storage.py` |
| **III. Entity-Driven** | ✅ Pass | Entidades `Dungeon`, `DungeonType`, `ExplorationSession` definidas em `entities/` |
| **IV. Observability** | ✅ Pass | Output em stdout/stderr, contrato de comandos documentado, session inspecionável via JSON |
| **V. Simplicity** | ✅ Pass | Sem novas dependências, reutiliza `storage.py` e `character_menu.py`, pattern consistente com código existente |
| **No new dependencies** | ✅ Pass | Apenas `random` da standard library adicionado |
| **Package structure** | ✅ Pass | Novos arquivos respeitam `entities/` e `cli/` directories |

**Result**: All gates passed. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/002-dungeon-explore/
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
├── main.py                          # Roteamento do comando 'explore'
├── tables.py                        # Adicionar: DUNGEON_TYPES, DUNGEON_NAME_TABLES
├── cli/
│   ├── __init__.py
│   ├── character_menu.py            # Existente (não alterado)
│   ├── storage.py                   # Adicionar: load_exploration, save_exploration
│   └── explore_menu.py              # NOVO: Menu de exploração de masmorras
└── entities/
    ├── __init__.py
    ├── player.py                    # Existente (não alterado)
    ├── ancestry.py                  # Existente (não alterado)
    ├── occupation.py                # Existente (não alterado)
    ├── magic.py                     # Existente (não alterado)
    ├── dungeon.py                   # NOVO: Dungeon dataclass + DungeonType enum
    └── dungeon_name.py              # NOVO: Geração de nomes compostos

tests/
├── test_dungeon_generation.py       # Testes de geração de masmorra
├── test_dungeon_name.py             # Testes de composição de nomes
├── test_explore_menu.py             # Testes do menu de exploração
└── test_exploration_storage.py      # Testes de persistência de sessão
```

**Structure Decision**: Estrutura single-project CLI, seguindo o padrão existente. Novos módulos de entidade em `entities/`, lógica de CLI em `cli/`, e persistência reutilizada em `cli/storage.py`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
