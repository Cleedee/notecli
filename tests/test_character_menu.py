"""Tests for character menu interaction (US3: Navigate Character Menu)."""

import unittest
from unittest.mock import patch

from notecli.cli.character_menu import show_menu


class TestMenuDisplay(unittest.TestCase):
    """T005: Test menu displays correct options."""

    @patch("sys.exit")
    @patch("builtins.input", side_effect=["0"])
    @patch("builtins.print")
    def test_menu_displays_options(self, mock_print, mock_input, mock_exit):
        """Menu must display options 1, 2, and 0/q."""
        show_menu()
        # Check that at least one print call contains the menu header
        all_output = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("personagens", all_output)
        self.assertIn("novo personagem", all_output)


class TestMenuInvalidInput(unittest.TestCase):
    """T006: Test invalid input produces error and re-display."""

    @patch("sys.exit")
    @patch("builtins.input", side_effect=["9", "abc", "0"])
    @patch("sys.stderr")
    def test_invalid_input_shows_error(self, mock_stderr, mock_input, mock_exit):
        """Invalid input should trigger error message and re-display."""
        show_menu()
        # Two invalid inputs should have produced errors
        self.assertEqual(mock_input.call_count, 3)


class TestMenuExit(unittest.TestCase):
    """T007: Test exit via '0' and 'q'."""

    @patch("builtins.input", side_effect=["0"])
    @patch("sys.exit")
    def test_exit_with_zero(self, mock_exit, mock_input):
        """Input '0' should exit with code 0."""
        show_menu()
        mock_exit.assert_called_once_with(0)

    @patch("builtins.input", side_effect=["q"])
    @patch("sys.exit")
    def test_exit_with_q(self, mock_exit, mock_input):
        """Input 'q' should exit with code 0."""
        show_menu()
        mock_exit.assert_called_once_with(0)


class TestMenuKeyboardInterrupt(unittest.TestCase):
    """T008: Test Ctrl+C (KeyboardInterrupt) handled gracefully."""

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    @patch("sys.exit")
    def test_ctrl_c_exits_cleanly(self, mock_exit, mock_input):
        """KeyboardInterrupt should result in clean exit."""
        show_menu()
        mock_exit.assert_called_once_with(0)


if __name__ == "__main__":
    unittest.main()


# ---------------------------------------------------------------------------
# US1: View Character List
# ---------------------------------------------------------------------------

from notecli.cli.character_menu import list_characters, show_character_detail
from notecli.cli.storage import save_characters
from notecli.entities.player import PlayerCharacter


class TestViewCharacterList(unittest.TestCase):
    """T018-T020: Test character list display, empty state, and detail view."""

    def test_list_with_characters(self):
        """T018: List display shows name, ancestry, profession, HP."""
        characters = [
            {"name": "Jackie", "ancestry": "Humano", "occupation": "Ferreiro",
             "health_points": 24, "hp_current": 24, "torches": 10,
             "light_on": False, "starting_weapon": "martelo",
             "alive": True, "magics": []}
        ]
        with patch("builtins.print") as mock_print:
            list_characters(characters)
            all_output = " ".join(str(c) for c in mock_print.call_args_list)
            self.assertIn("Jackie", all_output)
            self.assertIn("Humano", all_output)
            self.assertIn("Ferreiro", all_output)

    def test_list_empty(self):
        """T019: Empty list shows 'no characters' message."""
        with patch("builtins.print") as mock_print:
            list_characters([])
            all_output = " ".join(str(c) for c in mock_print.call_args_list)
            self.assertIn("nenhum personagem", all_output.lower())

    def test_detail_view(self):
        """T020: Detail view shows all fields."""
        pc = PlayerCharacter(
            name="Test",
            occupation="Ferreiro",
            torches=10,
            health_points=24,
            hp_current=24,
            ancestry="Humano",
            starting_weapon="martelo",
        )
        with patch("builtins.print") as mock_print:
            show_character_detail(pc, 1)
            all_output = " ".join(str(c) for c in mock_print.call_args_list)
            self.assertIn("Test", all_output)
            self.assertIn("24", all_output)
            self.assertIn("martelo", all_output)
