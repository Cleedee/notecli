# Tasks: Dungeon Segment Generation

**Input**: Design documents from `/specs/004-dungeon-segments/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/segment-exploration.md

**Tests**: Included — project uses TDD (Constitution Principle II).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization — already done. No tasks needed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core entities, tables, and dungeon graph extension that ALL user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T001 [P] Define `SegmentType` enum (ESCADARIA, CORREDOR, SALA, SALA_FINAL) in `src/notecli/entities/segment.py`
- [x] T002 [P] Define `Segment` dataclass in `src/notecli/entities/segment.py`
- [x] T003 Define `STAIRCASE_TRANSITIONS`, `CORRIDOR_TRANSITIONS`, `ROOM_TRANSITIONS` in `src/notecli/tables.py`
- [x] T004 Write tests for `SegmentType` and `Segment` in `tests/test_segment_entities.py`
- [x] T005 Write tests for transition tables in `tests/test_transition_tables.py`
- [x] T006 [P] Extend `Dungeon` entity with segment graph in `src/notecli/entities/dungeon.py`
- [x] T007 [P] Write tests for `Dungeon` graph extension in `tests/test_dungeon_graph.py`

**Checkpoint**: Foundation ready — user story implementation can now begin.

---

## Phase 3: User Story 1 — Gerar Segmento Inicial (Priority: P1) 🎯 MVP

**Goal**: Generate initial staircase segment (level 1, 1 door) at exploration start.

**Independent Test**: Execute `notecli explore` and verify first segment is staircase, level 1, 1 door.

### Tests for User Story 1

- [x] T008 [P] [US1] Test initial segment is staircase level 1 with 1 door in `tests/test_dungeon_graph.py`
- [x] T009 [P] [US1] Test segment display shows type, level, doors in `tests/test_segment_exploration.py`

### Implementation for User Story 1

- [x] T010 [US1] Implement `generate_initial_segment()` function in `src/notecli/entities/dungeon.py`
- [x] T011 [US1] Integrate initial segment generation into `explore()` in `src/notecli/cli/explore_menu.py`
- [x] T012 [US1] Display segment info after dungeon generation in `src/notecli/cli/explore_menu.py`

**Checkpoint**: At this point, `notecli explore` generates dungeon + initial staircase + displays it.

---

## Phase 4: User Story 2 — Gerar Segmento ao Abrir Porta (Priority: P2)

**Goal**: Open door → generate new segment using correct transition table. Level increases on staircase.

**Independent Test**: Open a door and verify correct segment type generated per transition table.

### Tests for User Story 2

- [x] T013 [P] [US2] Test open door from staircase generates corridor in `tests/test_dungeon_graph.py`
- [x] T014 [P] [US2] Test open door from corridor generates room or staircase in `tests/test_dungeon_graph.py`
- [x] T015 [P] [US2] Test open door from room generates room or staircase in `tests/test_dungeon_graph.py`
- [x] T016 [US2] Test staircase increases level by 1 in `tests/test_dungeon_graph.py`
- [x] T017 [US2] Test already-opened door shows existing segment in `tests/test_dungeon_graph.py`

### Implementation for User Story 2

- [x] T018 [US2] Implement `open_door(segment_id, door_index)` in `src/notecli/entities/dungeon.py`
- [x] T019 [US2] Implement CLI interaction loop for "abrir <N>" in `src/notecli/cli/explore_menu.py`
- [x] T020 [US2] Update exploration session save/load for segment graph in `src/notecli/cli/storage.py`

**Checkpoint**: Player can open doors and explore procedurally generated dungeon.

---

## Phase 5: User Story 3 — Retroceder Entre Segmentos (Priority: P3)

**Goal**: Player can backtrack through visited segments. Exit if path clear.

**Independent Test**: Advance 2+ segments, backtrack, verify state preserved.

### Tests for User Story 3

- [x] T021 [P] [US3] Test backtrack returns to previous segment in `tests/test_dungeon_graph.py`
- [x] T022 [P] [US3] Test backtrack at entrance triggers exit prompt in `tests/test_segment_exploration.py`
- [x] T023 [US3] Test exit dungeon when path is clear in `tests/test_segment_exploration.py`

### Implementation for User Story 3

- [x] T024 [US3] Implement `backtrack()` method in `src/notecli/entities/dungeon.py`
- [x] T025 [US3] Implement CLI interaction for "voltar" and "sair" in `src/notecli/cli/explore_menu.py`

**Checkpoint**: Player can backtrack and exit dungeon if path is clear.

---

## Phase 6: User Story 4 — Encontrar e Completar a Sala Final (Priority: P4)

**Goal**: Final Room generated at level 3 or as last segment.

**Independent Test**: Explore until 2 staircases reached, verify Final Room generated.

### Tests for User Story 4

- [x] T026 [P] [US4] Test Final Room generated at level 3 in `tests/test_dungeon_graph.py`
- [x] T027 [P] [US4] Test Final Room as last segment (no more staircases) in `tests/test_dungeon_graph.py`
- [x] T028 [US4] Test completion message when reaching Final Room in `tests/test_segment_exploration.py`

### Implementation for User Story 4

- [x] T029 [US4] Implement Final Room generation check in `open_door()` in `src/notecli/entities/dungeon.py`
- [x] T030 [US4] Display Final Room message in `src/notecli/cli/explore_menu.py`

**Checkpoint**: All user stories complete. Full dungeon exploration with Final Room.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [x] T031 [P] Run full test suite: `uv run python -m unittest discover -s tests` — all must pass
- [x] T032 Smoke test: `echo "abrir 1" | uv run notecli explore` — verify segment generation
- [x] T033 Update `QWEN.md` with new entities and CLI commands
- [x] T034 Verify error messages go to stderr per Constitution Principle IV

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 2)**: No external dependencies — BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - Can proceed sequentially: P1 → P2 → P3 → P4
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### Within Each User Story

- Tests MUST be written and FAIL before implementation.
- Entities before services.
- Core implementation before CLI integration.
- Story complete before moving to next priority.

### Parallel Opportunities

- T001–T002 (entities) can run in parallel.
- T004–T005 (tests) can run in parallel — different test files.
- T006–T007 (dungeon graph + tests) can run in parallel.
- T008–T009 (US1 tests) can run in parallel.
- T013–T015 (US2 tests) can run in parallel.
- T021–T022 (US3 tests) can run in parallel.
- T026–T027 (US4 tests) can run in parallel.
- T031–T034 (polish) can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (entities, tables, tests).
2. Complete Phase 3: User Story 1.
3. **STOP and VALIDATE**: Run `notecli explore` — staircase generated, displayed.
4. Run full test suite — all pass.

### Incremental Delivery

1. Foundational → entities and tables ready.
2. US1 → initial staircase generation.
3. US2 → door opening and segment exploration.
4. US3 → backtracking and exit.
5. US4 → Final Room and completion.
6. Polish → full suite, smoke tests.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to specific user story for traceability.
- Each user story should be independently completable and testable.
- Verify tests fail before implementing.
- Commit after each task or logical group.
