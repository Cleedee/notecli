# Implementation Plan: Save and Quit Dungeon

**Branch**: `007-save-quit-dungeon` | **Date**: 2026-04-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-save-quit-dungeon/spec.md`

## Summary

Adicionar opção "Salvar e Sair" ao menu de exploração, separada de "Sair da Masmorra". "Salvar e Sair" pausa a sessão (mantém `active=True`), preserva posição exata. "Sair da Masmorra" desativa sessão (`active=False`). Ao executar `notecli explore` com sessão ativa, perguntar se retoma ou inicia nova exploração.

## Technical Context

**Language/Version**: Python 3.14+
**Primary Dependencies**: `notecli.cli.explore_menu` (modificar fluxo), `notecli.cli.storage` (load/save/clear exploration), `notecli.entities.dungeon` (DungeonGraph)
**Storage**: `~/.notecli/exploration.json` (já persiste grafo; `active` controla retomada)
**Testing**: pytest/unittest (TDD)
**Target Platform**: Linux/macOS terminal (CLI interativo)
**Project Type**: CLI tool (comando subcommand `explore`)
**Performance Goals**: Salvar < 50ms, retomar < 50ms
**Constraints**: Sem novas dependências; mensagens claras e distintas
**Scale/Scope**: 1 sessão ativa por vez

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | Novas opções no menu interativo de exploração |
| **II. Test-Driven** | ✅ Pass | Testes antes da implementação (TDD) |
| **III. Entity-Driven** | ✅ Pass | Nenhuma entidade nova — reutiliza ExplorationSession, DungeonGraph |
| **IV. Observability** | ✅ Pass | Mensagens distintas para cada opção de saída |
| **V. Simplicity** | ✅ Pass | ~30 linhas de nova lógica no explore_menu. Sem libs novas. |
| **No new dependencies** | ✅ Pass | Zero |
| **Package structure** | ✅ Pass | Apenas `cli/explore_menu.py` modificado |

**Result**: All gates passed. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/007-save-quit-dungeon/
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
└── cli/
    └── explore_menu.py  # Modificar: adicionar "Salvar e Sair", prompts, fluxo de retomada
```

**Structure Decision**: Única modificação é em `explore_menu.py` — nova opção no menu, `_handle_save_quit()`, prompt ao detectar sessão ativa no início de `explore()`.

## Research

**Decision 1: Diferença entre "Sair da Masmorra" e "Salvar e Sair"**

- "Sair da Masmorra" (existente): chama `_deactivate_session()` → `active=False`. Próximo `explore()` não retoma.
- "Salvar e Sair" (novo): salva sessão + personagem, **não** desativa (`active=True`). Próximo `explore()` detecta sessão ativa e pergunta.

**Rationale**: Reutiliza `active` flag existente. Sem mudanças no storage.

**Decision 2: Prompt ao iniciar `notecli explore` com sessão ativa**

- Se `load_exploration()` retorna sessão ativa:
  - Perguntar: "Sessão encontrada. Retomar ou nova exploração? (r/n)"
  - `r` → retoma
  - `n` → `clear_exploration()`, gera nova masmorra

**Rationale**: Simples, 1 pergunta. Não quebra `--resume` (que retoma direto).

**Decision 3: Mensagens distintas**

- "Salvar e Sair": "💾 Progresso salvo. Personagem permanece na masmorra. Execute 'notecli explore --resume' para continuar."
- "Sair da Masmorra" (existente): "🏁 Você sai da masmorra com vida. Personagem salvo."

**Rationale**: Emojis + texto claro.

## Data Model

Sem novas entidades. ExplorationSession já tem campo `active`. DungeonGraph já persiste segmento atual + portas.

## Quickstart

```bash
# Durante exploração:
> salvar_e_sair
# → 💾 Progresso salvo. Execute 'notecli explore --resume' para continuar.

# Retomar:
uv run notecli explore --resume
# → ou
uv run notecli explore
# → "Sessão encontrada. Retomar? (r/n) > r"

# Nova exploração (quando há sessão ativa):
uv run notecli explore
# → "Sessão encontrada. Retomar? (r/n) > n"
# → Nova masmorra gerada.
```

## Agent Context Update

Nenhuma nova tecnologia.

## Constitution Check (Post-Design)

*Re-evaluated after Phase 1 design completion.*

| Principle | Status | Justification |
|-----------|--------|---------------|
| **I. CLI-First** | ✅ Pass | Nova opção `salvar_e_sair` no menu |
| **II. Test-Driven** | ✅ Pass | Testes de save-quit, resume, prompt |
| **III. Entity-Driven** | ✅ Pass | Nenhuma entidade nova |
| **IV. Observability** | ✅ Pass | Mensagens distintas |
| **V. Simplicity** | ✅ Pass | ~30 linhas no explore_menu |
| **No new dependencies** | ✅ Pass | Zero |
| **Package structure** | ✅ Pass | Apenas explore_menu modificado |

**Result**: All gates passed. No violations.
