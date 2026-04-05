# Tasks: Dungeon Map Display

**Input**: Design documents from `/specs/006-dungeon-map-display/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Included — TDD (Constitution Principle II).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization — already done. No tasks needed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No new foundational tasks needed. All dependencies (`load_exploration`, `DungeonGraph`, `Segment`, `Door`) already exist.

---

## Phase 3: User Story 1 — Exibir Mapa da Última Masmorra (Priority: P1) 🎯 MVP

**Goal**: `notecli map` displays full dungeon map with all segments, doors, and connections.

**Independent Test**: Execute `notecli map` after exploration and verify all segments, doors, and connections are displayed.

### Tests for User Story 1

- [x] T001 [P] [US1] Test map displays all segments when session exists in `tests/test_map_display.py`
- [x] T002 [P] [US1] Test "no session" message when exploration.json missing in `tests/test_map_display.py`
- [x] T003 [P] [US1] Test map shows door states (Fechada, Trancada, Destrancada) in `tests/test_map_display.py`

### Implementation for User Story 1

- [x] T004 [US1] Implement `display_map()` function in `src/notecli/cli/map_display.py`
- [x] T005 [US1] Wire `notecli map` subcommand in `src/notecli/main.py`

**Checkpoint**: `notecli map` displays full map with segments and door states.

---

## Phase 4: User Story 2 — Legenda do Mapa (Priority: P2)

**Goal**: Map includes legend explaining segment type and door state symbols.

**Independent Test**: Execute `notecli map` and verify legend is present with all symbols explained.

### Tests for User Story 2

- [x] T006 [P] [US2] Test legend includes all segment type symbols in `tests/test_map_display.py`
- [x] T007 [P] [US2] Test legend includes all door state symbols in `tests/test_map_display.py`

### Implementation for User Story 2

- [x] T008 [US2] Add legend section to `display_map()` in `src/notecli/cli/map_display.py`

**Checkpoint**: Map displays with complete legend.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect the feature.

- [x] T009 [P] Run full test suite: `uv run python -m unittest discover -s tests` — all must pass
- [x] T010 Smoke test: `uv run notecli map` (no session) — verify friendly message
- [x] T011 Smoke test: `uv run notecli explore` then `uv run notecli map` — verify map displays
- [x] T012 Update `QWEN.md` with new CLI command

---

## Dependencies & Execution Order

### Phase Dependencies

- **User Story 1 (Phase 3)**: No blocking tasks — can start immediately.
- **User Story 2 (Phase 4)**: Depends on US1 (legend added to existing map output).
- **Polish (Final Phase)**: Depends on US1 and US2 complete.

### Within Each User Story

- Tests (T001–T003, T006–T007) MUST be written and FAIL before implementation.
- T004 before T005 (function before wiring).

### Parallel Opportunities

- T001–T003 (US1 tests) can run in parallel.
- T006–T007 (US2 tests) can run in parallel.
- T009–T012 (polish) can run in parallel.

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all tests for User Story 1 together:
Task: "Test map displays all segments in tests/test_map_display.py"
Task: "Test no session message in tests/test_map_display.py"
Task: "Test map shows door states in tests/test_map_display.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Write tests T001–T003 (TDD — must fail first).
2. Implement T004 (`display_map()` function).
3. Implement T005 (wire in `main.py`).
4. **STOP and VALIDATE**: Run `uv run notecli map` — verify map displays.
5. Run `uv run python -m unittest tests.test_map_display -v`.

### Incremental Delivery

1. US1 → map with segments and door states.
2. US2 → add legend.
3. Polish → full suite, smoke tests.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to specific user story for traceability.
- This is a simple feature — ~50 lines of new code + tests.
- Reuses `load_exploration()` and existing entity serialization.
