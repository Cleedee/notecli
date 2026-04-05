"""Tests for character creation flow (US2: Create New Character)."""

import unittest
from unittest.mock import patch, MagicMock

from notecli.cli import character_menu
from notecli.cli.character_menu import create_character
from notecli.cli.storage import load_characters, _STORAGE_PATH
from notecli.entities.player import PlayerCharacter


class TestCharacterCreation(unittest.TestCase):
    """T025-T028: Test character creation saves, displays summary, and integrates with list."""

    def setUp(self):
        """Clear storage before each test."""
        if _STORAGE_PATH.exists():
            _STORAGE_PATH.unlink()
        _STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if _STORAGE_PATH.exists():
            _STORAGE_PATH.unlink()

    @patch("notecli.dice.Roller.roll_2d6")
    def test_creation_saves_to_storage(self, mock_roll):
        """T025: Character creation saves to storage with correct HP."""
        mock_roll.side_effect = [7, 6]  # Human (20 HP), Blacksmith (+4 HP)

        pc = create_character()

        saved = load_characters()
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["name"], pc.name)
        self.assertEqual(saved[0]["health_points"], 24)  # 20 + 4
        self.assertEqual(saved[0]["ancestry"], "Humano")
        self.assertEqual(saved[0]["occupation"], "Ferreiro")

    @patch("notecli.dice.Roller.roll_2d6")
    def test_creation_with_mocked_rolls(self, mock_roll):
        """T026: Creation with deterministic rolls produces correct character."""
        mock_roll.side_effect = [3, 4]  # Vagalóide (16 HP + Light), Noble (+0 HP)

        pc = create_character()

        self.assertEqual(pc.ancestry, "Vagalóide")
        self.assertEqual(pc.occupation, "Nobre")
        self.assertEqual(pc.health_points, 16)  # 16 + 0
        self.assertEqual(pc.torches, 10)
        self.assertEqual(pc.starting_weapon, "rapieira")
        self.assertTrue(pc.is_alive())
        # Vagalóide gets Light magic with 3 uses
        self.assertEqual(len(pc.magics), 1)
        self.assertEqual(pc.magics[0]["name"], "Light")
        self.assertEqual(pc.magics[0]["uses"], 3)

    @patch("notecli.dice.Roller.roll_2d6")
    def test_new_character_appears_in_list(self, mock_roll):
        """T027: After creation, character appears in storage list."""
        mock_roll.side_effect = [7, 2]  # Human, Beggar

        pc = create_character()

        saved = load_characters()
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["name"], pc.name)
        self.assertEqual(saved[0]["occupation"], "Mendigo")

    def test_creation_summary_output(self):
        """T028: show_creation_summary displays correct fields."""
        from notecli.cli.character_menu import show_creation_summary
        pc = PlayerCharacter(
            name="Test", occupation="Ferreiro", torches=10,
            health_points=24, hp_current=24, ancestry="Humano",
            starting_weapon="martelo",
        )
        with patch("builtins.print") as mock_print:
            show_creation_summary(pc)
            all_output = " ".join(str(c) for c in mock_print.call_args_list)
            self.assertIn("Humano", all_output)
            self.assertIn("Ferreiro", all_output)
            self.assertIn("24", all_output)
            self.assertIn("martelo", all_output)

    @patch("notecli.dice.Roller.roll_2d6")
    def test_multiple_characters_accumulate(self, mock_roll):
        """Edge case: creating multiple characters adds to storage."""
        mock_roll.side_effect = [7, 6, 3, 4]  # Two characters

        pc1 = create_character()
        pc2 = create_character()

        saved = load_characters()
        self.assertEqual(len(saved), 2)
        self.assertEqual(saved[0]["name"], pc1.name)
        self.assertEqual(saved[1]["name"], pc2.name)


if __name__ == "__main__":
    unittest.main()
