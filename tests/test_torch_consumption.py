"""Tests for torch consumption on exploration start."""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

from notecli.entities.player import PlayerCharacter


class TestTorchConsumptionOnExplore(unittest.TestCase):
    """T001-T005: Tests for torch consumption when exploration starts."""

    def test_torch_consumed_when_exploration_starts_with_torches(self):
        """T001: When character has torches, 1 torch must be consumed on start."""
        pc = PlayerCharacter(
            name="Test",
            occupation="Guarda",
            torches=10,
            health_points=20,
            hp_current=20,
        )
        self.assertEqual(pc.torches, 10)
        self.assertFalse(pc.light_on)

        pc.consume_torch()

        self.assertEqual(pc.torches, 9)
        self.assertTrue(pc.light_on)

    def test_light_on_after_torch_consumption(self):
        """T002: light_on must be True after torch consumption."""
        pc = PlayerCharacter(
            name="Test",
            occupation="Guarda",
            torches=5,
            health_points=20,
            hp_current=20,
        )
        pc.consume_torch()
        self.assertTrue(pc.light_on)

    def test_no_torch_consumed_when_zero_torches(self):
        """T003: When character has 0 torches, torches must stay at 0."""
        pc = PlayerCharacter(
            name="Test",
            occupation="Guarda",
            torches=0,
            health_points=20,
            hp_current=20,
        )
        self.assertEqual(pc.torches, 0)

        pc.consume_torch()

        self.assertEqual(pc.torches, 0)
        self.assertFalse(pc.light_on)

    def test_warning_message_when_no_torches(self):
        """T004: When character has 0 torches, a warning message must be displayed."""
        pc = PlayerCharacter(
            name="Test",
            occupation="Guarda",
            torches=0,
            health_points=20,
            hp_current=20,
        )

        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            pc.consume_torch()
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("tochas acabaram", output)

    @patch("notecli.cli.explore_menu.load_exploration")
    @patch("notecli.cli.explore_menu.load_characters")
    def test_torch_not_consumed_on_resume(self, mock_load_chars, mock_load_exp):
        """T005: When resuming session, torches must NOT be consumed again."""
        # Simulate an active session with a character that has 9 torches (1 already consumed)
        mock_load_exp.return_value = {
            "dungeon": {
                "type_name": "Templo",
                "name": "O Templo da Dor",
                "entrance_shown": True,
                "current_room": 2,
                "rooms_visited": 2,
            },
            "character_index": 1,
            "started_at": "2026-04-04T15:30:00",
            "active": True,
        }
        mock_load_chars.return_value = [
            {
                "name": "TestChar",
                "ancestry": "Humano",
                "occupation": "Guarda",
                "hp_current": 20,
                "health_points": 20,
                "alive": True,
                "torches": 9,
                "light_on": True,
                "starting_weapon": "Espada",
                "magics": [],
            },
        ]

        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            from notecli.cli.explore_menu import explore
            with patch("builtins.input", return_value="s"):
                explore(resume=True)
        except (KeyboardInterrupt, EOFError):
            pass
        finally:
            sys.stdout = old_stdout

        # Verify the character still has 9 torches (not consumed again on resume)
        self.assertIn("Tochas: 9", captured.getvalue())


if __name__ == "__main__":
    unittest.main()
