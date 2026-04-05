# Tasks: Dungeon Pre-Generation and Door Mechanics

**Input**: Design documents from `/specs/005-dungeon-generation-doors/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Included — TDD (Constitution Principle II).

## Phase 1: Setup

No tasks needed — project already initialized.

---

## Phase 2: Foundational (Blocking Prerequisites)

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T001 [P] Define `DoorState` enum (FECHADA, ARMADILHA, TRANCADA, DESTRANCADA) in `src/notecli/entities/door.py`
- [ ] T002 [P] Define `Door` dataclass in `src/notecli/entities/door.py`
- [ ] T003 Define 6 trap tables (placeholder) in `src/notecli/tables.py`
- [ ] T004 Write tests for `DoorState` and `Door` in `tests/test_door.py`
- [ ] T005 Write tests for trap tables in `tests/test_trap_tables.py`
- [ ] T006 Modify `Segment` to use `doors: list[Door]` instead of `connected_segments` in `src/notecli/entities/segment.py`
- [ ] T007 Write tests for `roll_door()` in `tests/test_door.py`

**Checkpoint**: Foundation ready.

---

## Phase 3: User Story 1 — Gerar Masmorra Completa (Priority: P1) 🎯 MVP

**Goal**: Pre-generate entire dungeon before exploration, including Final Room.

**Independent Test**: Execute `notecli explore` and verify full dungeon generated with Final Room.

### Tests

- [ ] T008 [P] [US1] Test full dungeon generation produces Final Room in `tests/test_dungeon_pregen.py`
- [ ] T009 [P] [US1] Test all doors have FECHADA state initially in `tests/test_dungeon_pregen.py`

### Implementation

- [ ] T010 [US1] Implement `generate_full_dungeon(graph)` in `src/notecli/entities/dungeon.py`
- [ ] T011 [US1] Integrate pre-generation into `explore()` in `src/notecli/cli/explore_menu.py`
- [ ] T012 [US1] Display initial segment with door states in `src/notecli/cli/explore_menu.py`

**Checkpoint**: `notecli explore` generates full dungeon + displays initial segment.

---

## Phase 4: User Story 2 — Abrir Porta com Rolagem (Priority: P2)

**Goal**: Door roll d6: 1=Trap, 2-3=Locked, 4-6=Unlocked. Reveals connected segment.

**Independent Test**: Open door and verify correct state based on roll.

### Tests

- [ ] T013 [P] [US2] Test roll=1 produces ARMADILHA in `tests/test_door.py`
- [ ] T014 [P] [US2] Test roll=2-3 produces TRANCADA in `tests/test_door.py`
- [ ] T015 [P] [US2] Test roll=4-6 produces DESTRANCADA in `tests/test_door.py`
- [ ] T016 [US2] Test already-opened door shows existing segment without re-roll in `tests/test_door.py`

### Implementation

- [ ] T017 [US2] Implement `roll_door()` and `open_door()` in `src/notecli/entities/dungeon.py`
- [ ] T018 [US2] Implement CLI interaction for "abrir <N>" in `src/notecli/cli/explore_menu.py`

**Checkpoint**: Player can open doors with randomized results.

---

## Phase 5: User Story 3 — Abrir Fechadura Consome Tocha (Priority: P3)

**Goal**: Locked doors require "destrancar" action consuming 1 torch.

**Independent Test**: With locked door and torches, unlock and verify 1 torch consumed.

### Tests

- [ ] T019 [P] [US3] Test unlock consumes 1 torch in `tests/test_door.py`
- [ ] T020 [P] [US3] Test unlock with 0 torches shows warning in `tests/test_door.py`
- [ ] T021 [US3] Test unlock on already unlocked door shows message in `tests/test_door.py`

### Implementation

- [ ] T022 [US3] Implement `unlock_door(door_index, pc)` in `src/notecli/entities/dungeon.py`
- [ ] T023 [US3] Implement CLI interaction for "destrancar <N>" in `src/notecli/cli/explore_menu.py`
- [ ] T024 [US3] Remove torch consumption on segment entry in `src/notecli/cli/explore_menu.py`

**Checkpoint**: Lockpicking works, torch only consumed on unlock.

---

## Phase 6: User Story 4 — Tabelas de Armadilhas (Priority: P4)

**Goal**: 6 trap tables, one per dungeon type. Placeholder entries.

**Independent Test**: Trigger trap on each dungeon type and verify correct table consulted.

### Tests

- [ ] T025 [P] [US4] Test correct trap table selected per dungeon type in `tests/test_trap_tables.py`
- [ ] T026 [US4] Test trap trigger shows placeholder message in `tests/test_trap_tables.py`

### Implementation

- [ ] T027 [US4] Implement `trigger_trap(dungeon_type)` in `src/notecli/entities/dungeon.py`
- [ ] T028 [US4] Display trap result in `src/notecli/cli/explore_menu.py`

**Checkpoint**: Trap table structure in place with placeholder messages.

---

## Phase N: Polish & Cross-Cutting Concerns

- [ ] T029 [P] Run full test suite: `uv run python -m unittest discover -s tests` — all must pass
- [ ] T030 Smoke test: `echo "abrir 1" | uv run notecli explore` — verify door roll
- [ ] T031 Update `QWEN.md` with new entities and CLI commands
- [ ] T032 Verify error messages go to stderr

---

## Dependencies

- **Foundational (Phase 2)**: BLOCKS all user stories
- **User Stories (Phase 3+)**: Sequential P1 → P2 → P3 → P4
- **Polish (Final)**: Depends on all user stories complete

### Parallel Opportunities

- T001–T002, T004–T005, T008–T009, T013–T015, T019–T020, T025, T029–T032
