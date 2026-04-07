# Tasks: Enter Room After Opening Door

**Input**: Design documents from `/specs/008-enter-room-after-door/`
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

**Purpose**: Modify Door entity with 3 independent boolean attributes.

**⚠️ CRITICAL**: All user story work depends on this foundation.

- [ ] T001 [P] Modify `Door` dataclass: add `is_open`, `is_locked`, `has_trap` booleans in `src/notecli/entities/door.py`
- [ ] T002 [P] Add `close()` and `display_status()` methods to `Door` in `src/notecli/entities/door.py`
- [ ] T003 Update `to_dict()` and `from_dict()` for new Door fields in `src/notecli/entities/door.py`
- [ ] T004 Add migration logic for old `state` string → new booleans in `src/notecli/entities/door.py`
- [ ] T005 Write tests for Door attributes, close, display in `tests/test_door_states.py`

**Checkpoint**: Door model updated with 3 attributes, backward compatible serialization.

---

## Phase 3: User Story 1 — Entrar na Sala Após Abrir Porta (Priority: P1) 🎯 MVP

**Goal**: Add "entrar" option after opening unlocked door. Close doors after entering or choosing another action.

**Independent Test**: Open unlocked door, choose "enter", verify player moves to new segment and door closes.

### Tests for User Story 1

- [ ] T006 [P] [US1] Test enter moves player to new segment in `tests/test_enter_room.py`
- [ ] T007 [P] [US1] Test door closes after entering in `tests/test_enter_room.py`
- [ ] T008 [P] [US1] Test choosing another action closes doors in `tests/test_enter_room.py`

### Implementation for User Story 1

- [ ] T009 [US1] Implement `enter_room(graph, door_index)` in `src/notecli/entities/dungeon.py`
- [ ] T010 [US1] Implement `close_opened_doors(segment)` in `src/notecli/entities/dungeon.py`
- [ ] T011 [US1] Add "entrar" option to exploration loop after opening unlocked door in `src/notecli/cli/explore_menu.py`
- [ ] T012 [US1] Call `close_opened_doors()` when player chooses non-enter action in `src/notecli/cli/explore_menu.py`

**Checkpoint**: Player can enter opened doors, doors close after any subsequent action.

---

## Phase 4: User Story 2 — Portas Trancadas e com Armadilha (Priority: P2)

**Goal**: Locked doors don't open without picking. Trap doors trigger effect. After any action, doors close keeping their lock/trap state.

**Independent Test**: Try opening locked door — verify stays locked. Pick lock — verify opens. Choose another action — verify closes.

### Tests for User Story 2

- [ ] T013 [P] [US2] Test locked door stays locked on open attempt in `tests/test_door_states.py`
- [ ] T014 [P] [US2] Test trap triggers and reveals destination in `tests/test_door_states.py`
- [ ] T015 [US2] Test lock/trap state preserved after close in `tests/test_door_states.py`

### Implementation for User Story 2

- [ ] T016 [US2] Update `open_door()` to check `is_locked` before opening in `src/notecli/entities/dungeon.py`
- [ ] T017 [US2] Update `unlock_door()` to set `is_open=True, is_locked=False` in `src/notecli/entities/dungeon.py`
- [ ] T018 [US2] Update trap handling to set `is_open=True, has_trap=False` in `src/notecli/entities/dungeon.py`

**Checkpoint**: Locked and trap doors behave correctly, state preserved after close.

---

## Phase 5: User Story 3 — Feedback Visual de Porta Fechando (Priority: P3)

**Goal**: Display clear messages when doors close, showing resulting state and whether destination is revealed.

**Independent Test**: Enter through door — verify "door closes behind" message. Choose another action — verify "door closes" message.

### Tests for User Story 3

- [ ] T019 [P] [US3] Test door-closing message on enter in `tests/test_enter_room.py`
- [ ] T020 [P] [US3] Test door-closing message on other action in `tests/test_enter_room.py`

### Implementation for User Story 3

- [ ] T021 [US3] Add door-closing messages to `enter_room()` and exploration loop in `src/notecli/cli/explore_menu.py`

**Checkpoint**: All door closures have clear feedback messages.

---

## Phase N: Polish & Cross-Cutting Concerns

- [ ] T022 [P] Run full test suite: `uv run python -m unittest discover -s tests` — all must pass
- [ ] T023 Smoke test: open door, enter, verify segment change + door closes
- [ ] T024 Smoke test: open door, choose another action, verify door closes
- [ ] T025 Update `QWEN.md` with new Door attributes and CLI option

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 2)**: BLOCKS all user stories — Door model must be updated first.
- **User Story 1 (Phase 3)**: Depends on Phase 2.
- **User Story 2 (Phase 4)**: Depends on Phase 2 (Door attributes).
- **User Story 3 (Phase 5)**: Depends on Phase 3 (enter/close logic).
- **Polish (Final Phase)**: Depends on all user stories complete.

### Within Each User Story

- Tests (T006–T008, T013–T015, T019–T020) MUST be written and FAIL before implementation.
- Implementation tasks within each story are sequential.

### Parallel Opportunities

- T001–T002 (Door fields + methods) can run in parallel.
- T006–T008 (US1 tests) can run in parallel.
- T013–T014 (US2 tests) can run in parallel.
- T019–T020 (US3 tests) can run in parallel.
- T022–T025 (polish) can run in parallel.

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all tests for User Story 1 together:
Task: "Test enter moves player to new segment in tests/test_enter_room.py"
Task: "Test door closes after entering in tests/test_enter_room.py"
Task: "Test choosing another action closes doors in tests/test_enter_room.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (Door model with 3 attributes).
2. Complete Phase 3: User Story 1 (enter + close).
3. **STOP and VALIDATE**: Open door, enter, verify segment change + door closes.
4. Run `uv run python -m unittest discover -s tests`.

### Incremental Delivery

1. Foundational → Door model updated.
2. US1 → enter + close doors.
3. US2 → locked + trap door behavior.
4. US3 → feedback messages.
5. Polish → full suite, smoke tests.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to specific user story for traceability.
- Backward compatibility: old sessions with `state` string must migrate to new boolean fields.
- `close_opened_doors()` only affects doors that are currently open (`is_open=True`).
