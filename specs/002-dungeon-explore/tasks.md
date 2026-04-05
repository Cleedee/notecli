# Tasks: Dungeon Exploration Flow

**Input**: Design documents from `/specs/002-dungeon-explore/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/explore-command.md

**Tests**: Included — project uses TDD (Constitution Principle II).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization — already done (uv, structure exists). No new tasks needed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core entities, tables, and storage that ALL user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T001 [P] Define `DungeonType` dataclass in `src/notecli/entities/dungeon.py`
- [ ] T002 [P] Define `Dungeon` dataclass in `src/notecli/entities/dungeon.py`
- [ ] T003 [P] Define `ExplorationSession` dataclass in `src/notecli/entities/dungeon.py`
- [ ] T004 Define `DUNGEON_TYPES` table (6 types: Palácio, Cripta, Tumba, Santuário, Templo, Calabouço) in `src/notecli/tables.py`
- [ ] T005 [P] Define `DUNGEON_NAME_TABLES` (articles, substantives, prepositions, modifiers) in `src/notecli/tables.py`
- [ ] T006 Implement `generate_dungeon_name()` function in `src/notecli/entities/dungeon_name.py`
- [ ] T007 Implement `generate_dungeon(roll)` function in `src/notecli/entities/dungeon.py`
- [ ] T008 Add `load_exploration()` and `save_exploration()` to `src/notecli/cli/storage.py`
- [ ] T009 Write tests for `DungeonType`, `Dungeon`, `ExplorationSession` in `tests/test_dungeon_generation.py`
- [ ] T010 Write tests for `generate_dungeon_name()` in `tests/test_dungeon_name.py`
- [ ] T011 Write tests for `load_exploration()` / `save_exploration()` in `tests/test_exploration_storage.py`

**Checkpoint**: Foundation ready — user story implementation can now begin.

---

## Phase 3: User Story 1 — Iniciar Exploração de Masmorra (Priority: P1) 🎯 MVP

**Goal**: Executar `notecli explore` gera uma masmorra (tipo, nome, descrição) e inicia sessão com personagem (criado automaticamente se não existir).

**Independent Test**: Executar `notecli explore` e verificar que masmorra é gerada, personagem é associado e sessão é persistida.

### Tests for User Story 1

- [ ] T012 [P] [US1] Test `explore()` generates dungeon with valid type, name, and description in `tests/test_explore_menu.py`
- [ ] T013 [P] [US1] Test auto-creates character when none exist in `tests/test_explore_menu.py`
- [ ] T014 [P] [US1] Test exploration session is saved after start in `tests/test_exploration_storage.py`

### Implementation for User Story 1

- [ ] T015 [US1] Implement `explore()` function in `src/notecli/cli/explore_menu.py` (generates dungeon, shows info, starts session)
- [ ] T016 [US1] Implement `start_new_session(dungeon, character_index)` in `src/notecli/cli/explore_menu.py`
- [ ] T017 [US1] Wire `notecli explore` subcommand in `src/notecli/main.py` to call `explore()`
- [ ] T018 [US1] Add error handling for storage failures (fallback to auto-create character)

**Checkpoint**: At this point, `notecli explore` generates a dungeon, creates/selects a character, saves the session, and prints a start message.

---

## Phase 4: User Story 2 — Visualizar Informações da Masmorra Gerada (Priority: P2)

**Goal**: Exibir no terminal o tipo, nome composto e descrição de entrada da masmorra gerada, com formatação clara.

**Independent Test**: Executar `notecli explore` e verificar que tipo, nome e descrição são exibidos corretamente.

### Tests for User Story 2

- [ ] T019 [P] [US2] Test dungeon type is one of 6 valid types in `tests/test_explore_menu.py`
- [ ] T020 [P] [US2] Test dungeon name matches pattern (article + substantive + preposition + modifier) in `tests/test_dungeon_name.py`
- [ ] T021 [P] [US2] Test entrance description matches the selected type in `tests/test_explore_menu.py`

### Implementation for User Story 2

- [ ] T022 [US2] Implement `display_dungeon_info(dungeon)` output formatting in `src/notecli/cli/explore_menu.py`
- [ ] T023 [US2] Ensure entrance description text is displayed with proper formatting in `src/notecli/cli/explore_menu.py`
- [ ] T024 [US2] Validate all 6 dungeon types have unique, non-empty entrance descriptions in `tests/test_dungeon_generation.py`

**Checkpoint**: At this point, `notecli explore` displays complete dungeon information (type, name, entrance description) before character selection.

---

## Phase 5: User Story 3 — Selecionar Personagem Existente (Priority: P3)

**Goal**: Quando existem personagens salvos, exibir menu numerado para escolha de personagem existente ou criação de novo.

**Independent Test**: Salvar 2+ personagens via `notecli character`, executar `notecli explore` e verificar menu de seleção.

### Tests for User Story 3

- [ ] T025 [P] [US3] Test numbered menu displays with existing characters in `tests/test_explore_menu.py`
- [ ] T026 [P] [US3] Test valid character selection returns correct character in `tests/test_explore_menu.py`
- [ ] T027 [P] [US3] Test invalid input prompts again with error message in `tests/test_explore_menu.py`
- [ ] T028 [US3] Test "Criar novo personagem" option triggers character creation in `tests/test_explore_menu.py`

### Implementation for User Story 3

- [ ] T029 [US3] Implement `select_or_create_character()` function in `src/notecli/cli/explore_menu.py`
- [ ] T030 [US3] Implement input validation loop (reject invalid, out-of-range, non-numeric) in `src/notecli/cli/explore_menu.py`
- [ ] T031 [US3] Integrate `create_character()` from `character_menu.py` for "Criar novo" option
- [ ] T032 [US3] Display character status line after selection (name, ancestry, HP, torches, magics) in `src/notecli/cli/explore_menu.py`

**Checkpoint**: All user stories are now independently functional — full exploration flow works with character selection.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [ ] T033 [P] Add `--resume` flag support to `notecli explore` in `src/notecli/main.py`
- [ ] T034 [P] Implement `resume_session()` function in `src/notecli/cli/explore_menu.py`
- [ ] T035 Verify all error messages go to stderr per Constitution Principle IV
- [ ] T036 Run full test suite: `uv run pytest` — all must pass
- [ ] T037 Run quickstart.md validation (manual smoke test)
- [ ] T038 Update `QWEN.md` with new entities and CLI commands

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — already complete.
- **Foundational (Phase 2)**: No external dependencies — BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - User stories can then proceed in parallel (if staffed) or sequentially (P1 → P2 → P3).
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — No dependencies on other stories.
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) — Builds on US1's dungeon generation display.
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) — Integrates with US1's session start.

### Within Each User Story

- Tests MUST be written and FAIL before implementation.
- Entities before services.
- Services before CLI menus.
- Core implementation before integration.
- Story complete before moving to next priority.

### Parallel Opportunities

- T001–T003 (entities) can run in parallel.
- T004–T005 (tables) can run in parallel.
- T009–T011 (foundational tests) can run in parallel.
- T012–T014 (US1 tests) can run in parallel.
- T019–T021 (US2 tests) can run in parallel.
- T025–T027 (US3 tests) can run in parallel.
- T033–T034 (resume feature) can run in parallel.

---

## Parallel Example: Foundational Phase

```bash
# Launch all entity definitions together:
Task: "Define DungeonType dataclass in src/notecli/entities/dungeon.py"
Task: "Define Dungeon dataclass in src/notecli/entities/dungeon.py"
Task: "Define ExplorationSession dataclass in src/notecli/entities/dungeon.py"

# Launch all table definitions together:
Task: "Define DUNGEON_TYPES table in src/notecli/tables.py"
Task: "Define DUNGEON_NAME_TABLES in src/notecli/tables.py"
```

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Test explore() generates dungeon in tests/test_explore_menu.py"
Task: "Test auto-creates character in tests/test_explore_menu.py"
Task: "Test exploration session saved in tests/test_exploration_storage.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (entities, tables, storage, tests).
2. Complete Phase 3: User Story 1.
3. **STOP and VALIDATE**: Run `uv run notecli explore` — dungeon generates, character created, session saved.
4. Run `uv run pytest` — all tests pass.

### Incremental Delivery

1. Complete Foundational → Foundation ready.
2. Add User Story 1 → Test independently → Demo (`notecli explore` works end-to-end).
3. Add User Story 2 → Test independently → Demo (dungeon info displays beautifully).
4. Add User Story 3 → Test independently → Demo (character selection menu works).
5. Add Polish (resume, stderr, full test suite).

### Parallel Team Strategy

With multiple developers:

1. Team completes Foundational together.
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to specific user story for traceability.
- Each user story should be independently completable and testable.
- Verify tests fail before implementing.
- Commit after each task or logical group.
- Stop at any checkpoint to validate story independently.
