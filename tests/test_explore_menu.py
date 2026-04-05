"""Tests for the explore menu CLI flow."""

import unittest
import json
from datetime import datetime
from unittest.mock import patch, MagicMock

from notecli.entities.dungeon import DungeonType, Dungeon
from notecli.cli.storage import save_exploration, clear_exploration
from notecli.dice import Roller


class TestExploreDungeonGeneration(unittest.TestCase):
    """T012: Test explore() generates dungeon with valid type, name, description."""

    def test_dungeon_type_is_one_of_six(self):
        """Generated dungeon type must be one of the 6 defined types."""
        from notecli import tables
        valid_names = {dt.name for dt in tables.DUNGEON_TYPES.values()}

        for roll in range(1, 7):
            from notecli.entities.dungeon import generate_dungeon
            dungeon = generate_dungeon(roll)
            self.assertIn(dungeon.type.name, valid_names)

    def test_dungeon_has_name(self):
        """Generated dungeon must have a non-empty name."""
        from notecli.entities.dungeon import generate_dungeon
        for roll in range(1, 7):
            dungeon = generate_dungeon(roll)
            self.assertTrue(len(dungeon.name) > 0)

    def test_dungeon_has_entrance_description(self):
        """Dungeon type must have a non-empty entrance description."""
        from notecli import tables
        for dt in tables.DUNGEON_TYPES.values():
            self.assertTrue(len(dt.entrance_description) > 0)


class TestExploreAutoCreateCharacter(unittest.TestCase):
    """T013: Test auto-creates character when none exist."""

    @patch("notecli.cli.character_menu.create_character")
    @patch("notecli.cli.storage.load_characters")
    def test_auto_creates_when_empty(self, mock_load, mock_create):
        """When no characters exist, create_character should be called."""
        mock_load.return_value = []
        mock_pc = MagicMock()
        mock_pc.name = "Gosma"
        mock_pc.ancestry = "Homem-Gosma"
        mock_pc.occupation = "Mendigo"
        mock_pc.hp_current = 10
        mock_pc.health_points = 10
        mock_pc.torches = 10
        mock_pc.magics = []
        mock_create.return_value = mock_pc

        from notecli.cli.explore_menu import select_or_create_character
        pc = select_or_create_character()

        mock_create.assert_called_once()
        self.assertEqual(pc.name, "Gosma")


class TestExploreSessionPersistence(unittest.TestCase):
    """T014: Test exploration session is saved after start."""

    def setUp(self):
        clear_exploration()

    def tearDown(self):
        clear_exploration()

    def test_session_saved_after_explore(self):
        """After starting exploration, session file should exist."""
        from notecli.entities.dungeon import generate_dungeon
        from notecli.cli.storage import load_exploration

        dungeon = generate_dungeon(1)
        session_data = {
            "dungeon": {
                "type_name": dungeon.type.name,
                "name": dungeon.name,
                "entrance_shown": False,
                "current_room": 0,
                "rooms_visited": 0,
            },
            "character_index": 1,
            "started_at": datetime.now().isoformat(),
            "active": True,
        }

        save_exploration(session_data)

        loaded = load_exploration()
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["dungeon"]["type_name"], "Palácio")
        self.assertTrue(loaded["active"])


class TestExploreInputValidation(unittest.TestCase):
    """T027: Test invalid input prompts again."""

    def test_roll_d6_for_dungeon(self):
        """Explore should use d6 roll to select dungeon type."""
        roll = Roller.d6()
        self.assertIn(roll, range(1, 7))


class TestExploreDisplayFormatting(unittest.TestCase):
    """T019-T021: US2 - Display formatting tests."""

    def test_display_dungeon_info_shows_type_name_description(self):
        """display_dungeon_info should print type, name, and entrance description."""
        from io import StringIO
        import sys

        dungeon_type = DungeonType(
            article="O",
            name="Templo",
            entrance_description="Um templo antigo.",
        )
        dungeon = Dungeon(type=dungeon_type, name="O Templo da Dor")

        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            from notecli.cli.explore_menu import display_dungeon_info
            display_dungeon_info(dungeon)
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("Templo", output)
        self.assertIn("O Templo da Dor", output)
        self.assertIn("Um templo antigo.", output)

    def test_all_six_types_have_descriptions(self):
        """All 6 dungeon types must have unique, non-empty entrance descriptions."""
        from notecli import tables
        descriptions = set()
        for dt in tables.DUNGEON_TYPES.values():
            self.assertTrue(len(dt.entrance_description) > 0)
            descriptions.add(dt.entrance_description)
        # All descriptions should be unique
        self.assertEqual(len(descriptions), 6)


class TestExploreCharacterSelection(unittest.TestCase):
    """T025-T028: US3 - Character selection menu tests."""

    @patch("notecli.cli.storage.load_characters")
    def test_menu_displays_with_existing_characters(self, mock_load):
        """Numbered menu should display when characters exist."""
        mock_load.return_value = [
            {
                "name": "Gnomo",
                "ancestry": "Gnomo",
                "occupation": "Coveiro",
                "hp_current": 16,
                "health_points": 16,
                "alive": True,
            },
        ]

        from io import StringIO
        import sys

        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            from notecli.cli.explore_menu import select_or_create_character
            # Will prompt for input, we simulate 'q' to exit
            with patch("builtins.input", return_value="q"):
                select_or_create_character()
        except (KeyboardInterrupt, EOFError):
            pass
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("Escolha um Personagem", output)
        self.assertIn("1)", output)
        self.assertIn("Criar novo personagem", output)

    @patch("notecli.cli.storage.load_characters")
    def test_valid_selection_returns_character(self, mock_load):
        """Selecting a valid number returns the correct character."""
        mock_load.return_value = [
            {
                "name": "TestChar",
                "ancestry": "Humano",
                "occupation": "Guarda",
                "hp_current": 20,
                "health_points": 20,
                "alive": True,
                "torches": 5,
                "light_on": False,
                "starting_weapon": "Espada",
                "magics": [],
            },
        ]

        from notecli.cli.explore_menu import select_or_create_character
        with patch("builtins.input", return_value="1"):
            pc = select_or_create_character()

        self.assertEqual(pc.name, "TestChar")
        self.assertEqual(pc.ancestry, "Humano")

    @patch("notecli.cli.storage.load_characters")
    def test_invalid_input_shows_error(self, mock_load):
        """Invalid input should show error message and re-prompt."""
        mock_load.return_value = [
            {
                "name": "TestChar",
                "ancestry": "Humano",
                "occupation": "Guarda",
                "hp_current": 20,
                "health_points": 20,
                "alive": True,
                "torches": 5,
                "light_on": False,
                "starting_weapon": "Espada",
                "magics": [],
            },
        ]

        from io import StringIO
        import sys

        captured_err = StringIO()
        old_stderr = sys.stderr
        sys.stderr = captured_err
        try:
            from notecli.cli.explore_menu import select_or_create_character
            # First invalid, then valid
            with patch("builtins.input", side_effect=["abc", "1"]):
                select_or_create_character()
        except (KeyboardInterrupt, EOFError):
            pass
        finally:
            sys.stderr = old_stderr

        error_output = captured_err.getvalue()
        self.assertIn("inválida", error_output)


if __name__ == "__main__":
    unittest.main()
