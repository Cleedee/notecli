# Tasks: Torch Consumption on Exploration Start

**Input**: Design documents from `/specs/003-torch-consumption/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Included — project uses TDD (Constitution Principle II).

**Organization**: Single user story (P1). No foundational tasks needed.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization — already done. No tasks needed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No new foundational tasks needed. All dependencies (`PlayerCharacter.consume_torch()`, `explore_menu.py`) already exist.

---

## Phase 3: User Story 1 — Consumir Tocha ao Iniciar Exploração (Priority: P1) 🎯 MVP

**Goal**: Ao iniciar nova exploração, consumir 1 tocha, ativar luz e exibir mensagem com estoque restante. Se sem tochas, exibir aviso.

**Independent Test**: Executar `notecli explore` e verificar que tochas são reduzidas em 1 e luz é acesa. Testar cenário com 0 tochas para verificar aviso.

### Tests for User Story 1 (TDD) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T001 [P] [US1] Test torch consumed when exploration starts with torches in `tests/test_torch_consumption.py`
- [x] T002 [P] [US1] Test light_on is True after torch consumption in `tests/test_torch_consumption.py`
- [x] T003 [P] [US1] Test no torch consumed when character has 0 torches in `tests/test_torch_consumption.py`
- [x] T004 [P] [US1] Test warning message when no torches available in `tests/test_torch_consumption.py`
- [x] T005 [US1] Test torch NOT consumed on session resume (`--resume`) in `tests/test_torch_consumption.py`

### Implementation for User Story 1

- [x] T006 [US1] Call `pc.consume_torch()` after character selection in `src/notecli/cli/explore_menu.py` (function `explore()`, after `select_or_create_character()`)
- [x] T007 [US1] Update character status display to reflect new torch count after consumption in `src/notecli/cli/explore_menu.py` (function `show_character_status()`)

**Checkpoint**: At this point, `notecli explore` consumes 1 torch, activates light, and shows updated torch count.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect the feature.

- [x] T008 [P] Run full test suite: `uv run python -m unittest discover -s tests` — all must pass
- [x] T009 Smoke test: `echo "q" | uv run notecli explore` — verify torch message appears
- [x] T010 Smoke test resume: `uv run notecli explore --resume` — verify no torch consumed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — already complete.
- **Foundational (Phase 2)**: No tasks — all dependencies exist.
- **User Story 1 (Phase 3)**: Depends on `PlayerCharacter.consume_torch()` existing (já implementado).
- **Polish (Final Phase)**: Depends on US1 completion.

### User Story Dependencies

- **User Story 1 (P1)**: Can start immediately — no blocking tasks.

### Within Each User Story

- Tests (T001–T005) MUST be written and FAIL before implementation.
- T006 (call `consume_torch`) before T007 (update display).
- Story complete before moving to Polish phase.

### Parallel Opportunities

- T001–T004 (tests) can run in parallel — different test methods, same file.
- T008–T010 (polish) can run in parallel.

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all tests for User Story 1 together:
Task: "Test torch consumed when exploration starts in tests/test_torch_consumption.py"
Task: "Test light_on after consumption in tests/test_torch_consumption.py"
Task: "Test no torch consumed when 0 torches in tests/test_torch_consumption.py"
Task: "Test warning message in tests/test_torch_consumption.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Write tests T001–T005 (TDD — must fail first).
2. Implement T006–T007 (1-2 lines of code).
3. **STOP and VALIDATE**: Run `echo "q" | uv run notecli explore` — verify torch message.
4. Run `uv run python -m unittest tests.test_torch_consumption -v`.

### Incremental Delivery

1. Tests first (T001–T005) → confirm they fail.
2. Implementation (T006–T007) → tests pass.
3. Polish (T008–T010) → full suite passes.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to specific user story for traceability.
- This feature is minimal by design — reuses existing `consume_torch()` method.
- Implementation is approximately 2 lines of new code + tests.
