# Feature Specification: Character Menu

**Feature Branch**: `001-character-menu`
**Created**: 2026-04-04
**Status**: Draft
**Input**: User description: "Ao executar o comando notecli character, um ambiente de terminal é aberto com duas opções disponíveis: 1) personagens; 2) novo personagem. A primeira opção acessa uma lista de personagens. A segunda opção abre para criar um personagem."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Character List (Priority: P1)

O usuário executa `notecli character` e seleciona a opção "personagens" para visualizar todos os personagens criados anteriormente, com informações básicas de cada um (nome, ancestralidade, profissão e estado atual).

**Why this priority**: Without existing characters to view, the player has no persistent progress. This is the entry point for returning players who want to continue or review their characters.

**Independent Test**: Can be fully tested by creating characters via the CLI and verifying they appear in the list with correct information.

**Acceptance Scenarios**:

1. **Given** the user has created characters previously, **When** they run `notecli character` and select "personagens", **Then** they see a numbered list of all characters with name, ancestry, and profession displayed.
2. **Given** the user has no saved characters, **When** they run `notecli character` and select "personagens", **Then** they see a message indicating no characters exist yet and are prompted to create one.
3. **Given** the character list is displayed, **When** the user selects a character by number, **Then** they see detailed information about that character (HP, magics, torches, status).

---

### User Story 2 - Create New Character (Priority: P1)

O usuário executa `notecli character` e seleciona a opção "novo personagem" para iniciar o fluxo de criação de personagem, onde ancestralidade e profissão são determinadas aleatoriamente, e o personagem é salvo automaticamente.

**Why this priority**: Character creation is the fundamental prerequisite for all gameplay. Without it, no exploration or combat can occur.

**Independent Test**: Can be fully tested by running the creation flow and verifying a new character appears in the character list with valid randomized attributes.

**Acceptance Scenarios**:

1. **Given** the user is at the character menu, **When** they select "novo personagem", **Then** the system randomly determines ancestry and profession, displays the results, and saves the character.
2. **Given** a character has just been created, **When** the user returns to the character list, **Then** the new character appears in the list with all assigned attributes.
3. **Given** the character creation completes, **Then** the user is asked if they want to create another character or return to the main menu.

---

### User Story 3 - Navigate Character Menu (Priority: P2)

O usuário executa `notecli character`, vê um menu interativo com duas opções numeradas, pode navegar entre elas e selecionar uma opção, ou sair do menu.

**Why this priority**: The menu is the entry point that routes users to all character-related functionality. It must be intuitive and responsive.

**Independent Test**: Can be tested by launching the menu, verifying the two options are displayed, selecting each option, and exiting cleanly.

**Acceptance Scenarios**:

1. **Given** the user runs `notecli character`, **When** the menu loads, **Then** they see two numbered options: "1) personagens" and "2) novo personagem", plus an option to exit.
2. **Given** the user is viewing a submenu (character list or character creation), **When** they press the exit key (e.g., `q` or `0`), **Then** they return to the previous menu or exit the application cleanly.

---

### Edge Cases

- What happens when the user enters an invalid menu option (e.g., a number outside the range or a letter)?
- How does the system handle corrupted or incomplete saved character data?
- What happens if the user interrupts character creation mid-flow (e.g., Ctrl+C)?
- How does the system handle reaching a maximum character limit (if any)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display an interactive menu with two options ("personagens" and "novo personagem") when the user runs `notecli character`.
- **FR-002**: System MUST load and display all previously saved characters when the user selects "personagens", showing at minimum name, ancestry, and profession.
- **FR-003**: Users MUST be able to select a character from the list to view full details (HP, current HP, magics with uses, torches, ancestry, profession).
- **FR-004**: System MUST randomly determine ancestry and profession when creating a new character, using the existing ancestry table and a profession table.
- **FR-005**: System MUST persist newly created characters to a local storage file so they are available in future sessions.
- **FR-006**: System MUST validate menu input and display an error message for invalid selections, re-displaying the current menu.
- **FR-007**: Users MUST be able to exit any menu level cleanly (e.g., pressing `q` or `0`).
- **FR-008**: System MUST display a confirmation message after character creation showing the generated character summary.

### Key Entities

- **Character Record**: A persistent representation of a player character, including name, ancestry, profession, health points (max and current), magics (with uses), torches, and alive/dead status.
- **Profession**: A character attribute (like ancestry) that determines starting skills or bonuses. [NEEDS CLARIFICATION: profession list and effects not yet defined]
- **Character Storage**: A local file (e.g., JSON or YAML) that holds an array of character records, one per created character.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can launch the character menu, view existing characters, and select one to see details in under 5 seconds from command execution.
- **SC-002**: Users can create a new character and see it appear in the character list within a single session, with 100% data persistence across application restarts.
- **SC-003**: 100% of invalid menu inputs are handled gracefully with clear error messages and no application crashes.
- **SC-004**: Users can exit any menu state and return to the main menu or exit the application within 1 keypress.

## Assumptions

- Characters are stored locally on the user's filesystem (no cloud sync or remote database).
- A reasonable default character storage path exists (e.g., `~/.notecli/characters.json` or a `characters/` directory in the project).
- Profession randomization uses a similar d6-based table mechanism as ancestry (consistent with existing `tables.py` patterns).
- No character deletion is required for this feature — creation and viewing only.
- The existing `PlayerCharacter` dataclass and `Ancestry` system will be reused for character creation.
- Maximum number of characters is not capped for this initial version.
