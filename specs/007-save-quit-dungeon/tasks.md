# Tasks: Save and Quit Dungeon

**Input**: Design documents from `/specs/007-save-quit-dungeon/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Included — TDD (Constitution Principle II).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

No tasks needed — project already initialized.

---

## Phase 2: Foundational (Blocking Prerequisites)

No new foundational tasks needed. All dependencies (`load_exploration`, `save_exploration`, `clear_exploration`, `DungeonGraph`) already exist.

---

## Phase 3: User Story 1 — Salvar Posição e Sair do Jogo (Priority: P1) 🎯 MVP

**Goal**: Add "Salvar e Sair" option that pauses exploration, keeps session active, saves position + state.

**Independent Test**: Use "Salvar e Sair", then `notecli explore --resume` and verify exact segment + doors + torches preserved.

### Tests for User Story 1

- [x] T001 [P] [US1] Test save_quit keeps session active in `tests/test_save_quit.py`
- [x] T002 [P] [US1] Test save_quit preserves current segment in `tests/test_save_quit.py`
- [x] T003 [P] [US1] Test resume restores exact segment + doors + torches in `tests/test_save_quit.py`

### Implementation for User Story 1

- [x] T004 [US1] Implement `_handle_save_quit(pc, graph)` in `src/notecli/cli/explore_menu.py`
- [x] T005 [US1] Add "salvar_e_sair" option to exploration loop menu in `src/notecli/cli/explore_menu.py`

**Checkpoint**: "Salvar e Sair" saves session (active=True), resume restores exact state.

---

## Phase 4: User Story 2 — Diferença Clara entre "Sair da Masmorra" e "Salvar e Sair" (Priority: P2)

**Goal**: Distinct messages and behaviors for both exit options.

**Independent Test**: Use both options and verify distinct messages + session states.

### Tests for User Story 2

- [x] T006 [P] [US2] Test "Sair da Masmorra" deactivates session in `tests/test_save_quit.py`
- [x] T007 [P] [US2] Test "Salvar e Sair" shows save message in `tests/test_save_quit.py`
- [x] T008 [P] [US2] Test "Sair da Masmorra" shows exit message in `tests/test_save_quit.py`

### Implementation for User Story 2

- [x] T009 [US2] Add distinct exit message for "Salvar e Sair" in `src/notecli/cli/explore_menu.py`
- [x] T010 [US2] Verify existing "Sair da Masmorra" message remains distinct in `src/notecli/cli/explore_menu.py`

**Checkpoint**: Messages are clearly distinct, session states differ correctly.

---

## Phase 5: User Story 3 — Retomar com `notecli explore` após "Salvar e Sair" (Priority: P3)

**Goal**: `notecli explore` detects active session and prompts to resume or start new.

**Independent Test**: Save-quit, then run `notecli explore` and verify resume prompt.

### Tests for User Story 3

- [x] T011 [P] [US3] Test explore prompts when active session exists in `tests/test_save_quit.py`
- [x] T012 [P] [US3] Test choose resume continues exploration in `tests/test_save_quit.py`
- [x] T013 [US3] Test choose new exploration discards old session in `tests/test_save_quit.py`

### Implementation for User Story 3

- [x] T014 [US3] Add active session detection + prompt at start of `explore()` in `src/notecli/cli/explore_menu.py`
- [x] T015 [US3] Implement resume path on "r" response in `src/notecli/cli/explore_menu.py`
- [x] T016 [US3] Implement new exploration path on "n" response (clear + new dungeon) in `src/notecli/cli/explore_menu.py`

**Checkpoint**: `notecli explore` prompts when session active, resume/new both work.

---

## Phase N: Polish & Cross-Cutting Concerns

- [x] T017 [P] Run full test suite: `uv run python -m unittest discover -s tests` — all must pass
- [x] T018 Smoke test: save-quit then resume → verify segment preserved
- [x] T019 Smoke test: `notecli explore` with active session → verify prompt
- [x] T020 Update `QWEN.md` with new CLI option

---

## Dependencies & Execution Order

### Phase Dependencies

- **User Story 1 (Phase 3)**: No blocking tasks — can start immediately.
- **User Story 2 (Phase 4)**: Depends on US1 (messages reference save-quit behavior).
- **User Story 3 (Phase 5)**: Depends on US1 (session active state).
- **Polish (Final Phase)**: Depends on all user stories complete.

### Within Each User Story

- Tests (T001–T003, T006–T008, T011–T013) MUST be written and FAIL before implementation.
- Implementation tasks within each story are sequential.

### Parallel Opportunities

- T001–T003 (US1 tests) can run in parallel.
- T006–T008 (US2 tests) can run in parallel.
- T011–T012 (US3 tests) can run in parallel.
- T017–T020 (polish) can run in parallel.

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all tests for User Story 1 together:
Task: "Test save_quit keeps session active in tests/test_save_quit.py"
Task: "Test save_quit preserves current segment in tests/test_save_quit.py"
Task: "Test resume restores exact segment in tests/test_save_quit.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Write tests T001–T003 (TDD — must fail first).
2. Implement T004–T005 (`_handle_save_quit` + menu option).
3. **STOP and VALIDATE**: Use "salvar_e_sair" during exploration, then `notecli explore --resume`.
4. Run `uv run python -m unittest tests.test_save_quit -v`.

### Incremental Delivery

1. US1 → save-quit + resume.
2. US2 → distinct messages.
3. US3 → prompt on `notecli explore`.
4. Polish → full suite, smoke tests.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to specific user story for traceability.
- This is a simple feature — ~30 lines of new code + tests.
- Reuses existing `load_exploration`, `save_exploration`, `clear_exploration`, `DungeonGraph.from_dict`.
