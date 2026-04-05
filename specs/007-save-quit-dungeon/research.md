# Research: Save and Quit Dungeon

**Purpose**: Document design decisions for save-quit feature
**Created**: 2026-04-05

## Decision 1: Difference between "Sair da Masmorra" and "Salvar e Sair"

**Context**: Two exit options needed — one ends exploration, one pauses it.

**Decision**:
- "Sair da Masmorra" (existing): calls `_deactivate_session()` → `active=False`. Next `explore()` does not resume.
- "Salvar e Sair" (new): saves session + character, keeps `active=True`. Next `explore()` detects active session and prompts.

**Rationale**: Reuses existing `active` flag. No storage changes needed.

**Alternatives considered**:
- Separate "paused" state — rejected: adds complexity without benefit
- New save file — rejected: exploration.json already has all needed data

## Decision 2: Prompt on `notecli explore` with active session

**Context**: User shouldn't need to remember `--resume`.

**Decision**: If `load_exploration()` returns active session:
- Ask: "Sessão encontrada. Retomar ou nova exploração? (r/n)"
- `r` → resume
- `n` → `clear_exploration()`, generate new dungeon

**Rationale**: Simple, 1 question. Doesn't break `--resume` (which resumes directly).

## Decision 3: Distinct messages

**Context**: Users must understand which option they chose.

**Decision**:
- "Salvar e Sair": "💾 Progresso salvo. Personagem permanece na masmorra. Execute 'notecli explore --resume' para continuar."
- "Sair da Masmorra" (existing): "🏁 Você sai da masmorra com vida. Personagem salvo."

**Rationale**: Emojis + clear text differentiation.
