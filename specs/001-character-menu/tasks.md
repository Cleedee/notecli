# Tasks: Character Menu

**Input**: Design documents from `/specs/001-character-menu/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED per the project constitution (Principle II: Test-Driven, NON-NEGOTIABLE).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the new `cli/` subpackage structure

- [ ] T001 [P] Create `src/notecli/cli/` directory and `__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T002 [P] Implement character storage service in `src/notecli/cli/storage.py` (load/save JSON to `~/.notecli/characters.json`, create directory if missing, handle corrupted file errors)
- [ ] T003 Implement `PlayerCharacter` serialization helpers (`to_dict` / `from_dict`) in `src/notecli/entities/player.py` (serialize name, ancestry, occupation, HP, torches, light_on, magics by name+uses, starting_weapon, alive; reconstruct magics via `factory_magic()` on load)
- [ ] T004 Add 2d6 roll helper in `src/notecli/dice.py` — `Roller.roll_2d6()` that returns `int(Roller.roll("2d6"))`

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel

---

## Phase 3: User Story 3 — Navigate Character Menu (Priority: P2) 🎯 Entry Point

> **Why US3 first?** The menu is the entry point for all character functionality. Building it first provides the shell into which US1 and US2 plug. It can be tested independently with stub handlers.

**Goal**: `notecli character` launches an interactive menu with options 1) personagens, 2) novo personagem, 0/q to exit. Invalid input shows error and re-displays.

**Independent Test**: Launch menu, verify options display, select each option (stub), exit cleanly. Invalid input produces stderr message.

### Tests for User Story 3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T005 [P] [US3] Test menu displays correct options in `tests/test_character_menu.py`
- [ ] T006 [P] [US3] Test invalid input produces error and re-display in `tests/test_character_menu.py`
- [ ] T007 [US3] Test exit via `0` and `q` in `tests/test_character_menu.py`
- [ ] T008 [US3] Test Ctrl+C (`KeyboardInterrupt`) handled gracefully in `tests/test_character_menu.py`

### Implementation for User Story 3

- [ ] T009 [P] [US3] Implement `show_menu()` function in `src/notecli/cli/character_menu.py` (display numbered options, accept input, validate, loop)
- [ ] T010 [P] [US3] Implement `handle_invalid_input()` in `src/notecli/cli/character_menu.py` (write error to stderr, return to loop)
- [ ] T011 [US3] Implement `handle_exit()` in `src/notecli/cli/character_menu.py` (clean exit message, `sys.exit(0)`)
- [ ] T012 [US3] Wire `notecli character` subcommand in `src/notecli/main.py` (route "character" arg to `character_menu.main()`)
- [ ] T013 [US3] Add stub handlers for "personagens" and "novo personagem" in `src/notecli/cli/character_menu.py` (placeholder print statements)

**Checkpoint**: Menu launches, displays options, validates input, exits cleanly. Stub handlers print placeholders.

---

## Phase 4: User Story 1 — View Character List (Priority: P1) 🎯 MVP

**Goal**: Selecting "personagens" loads saved characters from storage and displays them as a numbered list. Selecting a character shows full details.

**Independent Test**: Pre-populate storage with test characters, run menu option 1, verify list output matches saved data. Empty storage shows "no characters" message.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T014 [P] [US1] Test storage `load_characters()` with valid JSON in `tests/test_storage.py`
- [ ] T015 [P] [US1] Test storage `load_characters()` with missing file returns empty list in `tests/test_storage.py`
- [ ] T016 [P] [US1] Test storage `load_characters()` with corrupted JSON returns error in `tests/test_storage.py`
- [ ] T017 [P] [US1] Test storage `save_characters()` writes valid JSON in `tests/test_storage.py`
- [ ] T018 [US1] Test character list display with saved characters in `tests/test_character_menu.py`
- [ ] T019 [US1] Test "no characters" message when storage is empty in `tests/test_character_menu.py`
- [ ] T020 [US1] Test character detail view shows all fields in `tests/test_character_menu.py`

### Implementation for User Story 1

- [ ] T021 [US1] Implement `list_characters(characters)` in `src/notecli/cli/character_menu.py` (numbered list with name, ancestry, profession, HP, status; "no characters" message if empty)
- [ ] T022 [US1] Implement `show_character_detail(character, index)` in `src/notecli/cli/character_menu.py` (full details: HP, current HP, magics with uses, torches, weapon, status)
- [ ] T023 [US1] Wire option 1 handler in `src/notecli/cli/character_menu.py` to call `storage.load_characters()` then `list_characters()`
- [ ] T024 [US1] Add character selection sub-menu (after list, prompt for number to view details, or back/exit)

**Checkpoint**: User can view character list and inspect individual character details. Works with pre-existing data.

---

## Phase 5: User Story 2 — Create New Character (Priority: P1) 🎯 Core Feature

**Goal**: Selecting "novo personagem" rolls 2d6 for ancestry, 2d6 for profession, applies both to a new `PlayerCharacter`, saves to storage, and displays a summary. Prompts to create another or return.

**Independent Test**: Run creation flow, verify character is saved to storage with correct attributes (HP = ancestry + occupation bonus, 10 torches, starting weapon, ancestry magics).

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T025 [P] [US2] Test character creation saves to storage with correct HP in `tests/test_create_character.py`
- [ ] T026 [P] [US2] Test character creation with mocked 2d6 rolls for deterministic ancestry/profession in `tests/test_create_character.py`
- [ ] T027 [P] [US2] Test new character appears in list after creation in `tests/test_create_character.py`
- [ ] T028 [US2] Test character summary output format in `tests/test_create_character.py`

### Implementation for User Story 2

- [ ] T029 [P] [US2] Implement `roll_ancestry()` in `src/notecli/cli/character_menu.py` (roll 2d6, lookup in `tables.ANCESTRIES`, display result)
- [ ] T030 [P] [US2] Implement `roll_profession()` in `src/notecli/cli/character_menu.py` (roll 2d6, lookup in `tables.OCCUPATIONS`, display result)
- [ ] T031 [US2] Implement `create_character()` in `src/notecli/cli/character_menu.py` (roll ancestry + profession, apply to PlayerCharacter, set torches=10, set starting_weapon, save via `storage.save_characters()`)
- [ ] T032 [US2] Implement `show_creation_summary(pc)` in `src/notecli/cli/character_menu.py` (display ancestry, profession, final HP, weapon, torches)
- [ ] T033 [US2] Wire option 2 handler in `src/notecli/cli/character_menu.py` to call `create_character()`
- [ ] T034 [US2] Implement "create another?" prompt (s/n loop back to menu or exit)

**Checkpoint**: User can create characters with randomized ancestry/profession, see summary, and characters persist across sessions.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T035 [P] Update `src/notecli/entities/__init__.py` to export any new entities or serialization helpers
- [ ] T036 Run all existing tests to ensure no regressions
- [ ] T037 [P] Add docstrings to all new public functions in `cli/` and storage modules
- [ ] T038 Run quickstart.md validation (manual end-to-end test per example session)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US3 (menu shell) can be built first as it provides the entry point
  - US1 (view list) and US2 (create) plug into the menu after US3
  - Suggested order: US3 → US1 → US2 (entry point → read → write)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US3 Navigate Menu (P2)**: Can start after Foundational — provides menu shell with stub handlers
- **US1 View List (P1)**: Can start after Foundational — depends on storage (T002-T003)
- **US2 Create Character (P1)**: Can start after Foundational — depends on storage (T002-T003) and entity application
- US1 and US2 are independently testable once storage foundation exists

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models/helpers before services
- Services before menu integration
- Core implementation before cross-cutting polish
- Story complete before moving to next priority

### Parallel Opportunities

- T001 (setup) is standalone
- T002 (storage) and T004 (dice helper) can run in parallel in Foundational phase
- T003 (serialization) depends on T002's storage format design
- T005-T007 (US3 tests) can run in parallel
- T009-T010 (US3 menu functions) can run in parallel
- T014-T017 (US1 storage tests) can run in parallel
- T025-T027 (US2 creation tests) can run in parallel
- T029-T030 (US2 roll functions) can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch independent foundational tasks together:
Task: "T002 [P] Implement character storage service in src/notecli/cli/storage.py"
Task: "T004 [P] Add 2d6 roll helper in src/notecli/dice.py"
```

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all storage tests together:
Task: "T014 [P] [US1] Test storage load_characters() with valid JSON in tests/test_storage.py"
Task: "T015 [P] [US1] Test storage load_characters() with missing file in tests/test_storage.py"
Task: "T016 [P] [US1] Test storage load_characters() with corrupted JSON in tests/test_storage.py"
Task: "T017 [P] [US1] Test storage save_characters() in tests/test_storage.py"
```

---

## Parallel Example: User Story 2 Creation Tests

```bash
# Launch all creation tests together:
Task: "T025 [P] [US2] Test character creation saves to storage in tests/test_create_character.py"
Task: "T026 [P] [US2] Test creation with mocked 2d6 rolls in tests/test_create_character.py"
Task: "T027 [P] [US2] Test new character appears in list after creation in tests/test_create_character.py"
```

---

## Implementation Strategy

### MVP First (US3 Menu + US1 View)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002-T004)
3. Complete Phase 3: US3 Navigate Menu (T005-T013)
4. Complete Phase 4: US1 View List (T014-T024) — **pre-populate storage manually for testing**
5. **STOP and VALIDATE**: Menu works, can view characters
6. Demo if ready

### Incremental Delivery

1. Setup + Foundational → Storage + dice ready
2. US3 (menu shell) → Test independently → Menu launches with stubs
3. US1 (view list) → Test independently → Can view pre-existing characters
4. US2 (create) → Test independently → Full creation flow with persistence
5. Polish → Docstrings, regression tests, quickstart validation

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: US3 (menu navigation)
   - Developer B: US1 (view list) — can start as soon as T002-T003 complete
   - Developer C: US2 (create character) — can start as soon as T002-T003 complete
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **Constitution Principle II (Test-Driven)**: All test tasks MUST be written and confirmed failing before their corresponding implementation tasks
