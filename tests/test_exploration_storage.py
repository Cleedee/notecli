"""Tests for exploration session storage functions."""

import unittest
import json
import os
from pathlib import Path
from unittest.mock import patch, mock_open

from notecli.cli.storage import (
    load_exploration,
    save_exploration,
    clear_exploration,
)


class TestExplorationStorage(unittest.TestCase):
    """Tests for load_exploration, save_exploration, clear_exploration."""

    def setUp(self):
        self.sample_session = {
            "dungeon": {
                "type_name": "Templo",
                "name": "O Templo da Dor Nebulosa",
                "entrance_shown": True,
                "current_room": 2,
                "rooms_visited": 2,
            },
            "character_index": 1,
            "started_at": "2026-04-04T15:30:00",
            "active": True,
        }

    @patch("notecli.cli.storage._EXPLORATION_PATH")
    def test_load_exploration_no_file(self, mock_path):
        """Should return None when exploration file doesn't exist."""
        mock_path.exists.return_value = False
        result = load_exploration()
        self.assertIsNone(result)

    @patch("notecli.cli.storage._EXPLORATION_PATH")
    def test_load_exploration_active_session(self, mock_path):
        """Should return session data when file exists and session is active."""
        mock_path.exists.return_value = True
        file_data = {"version": 1, "session": self.sample_session}

        with patch("builtins.open", mock_open(read_data=json.dumps(file_data))):
            result = load_exploration()

        self.assertIsNotNone(result)
        self.assertEqual(result["dungeon"]["name"], "O Templo da Dor Nebulosa")
        self.assertTrue(result["active"])

    @patch("notecli.cli.storage._EXPLORATION_PATH")
    def test_load_exploration_inactive_session(self, mock_path):
        """Should return None when session is not active."""
        mock_path.exists.return_value = True
        inactive = dict(self.sample_session)
        inactive["active"] = False
        file_data = {"version": 1, "session": inactive}

        with patch("builtins.open", mock_open(read_data=json.dumps(file_data))):
            result = load_exploration()

        self.assertIsNone(result)

    @patch("notecli.cli.storage._EXPLORATION_PATH")
    def test_load_exploration_corrupted_json(self, mock_path):
        """Should raise ValueError when JSON is corrupted."""
        mock_path.exists.return_value = True

        with patch("builtins.open", mock_open(read_data="{invalid json")):
            with self.assertRaises(ValueError):
                load_exploration()

    @patch("notecli.cli.storage._get_exploration_path")
    def test_save_exploration_writes_file(self, mock_path):
        """Should write session data to exploration file."""
        mock_path.return_value = Path("/tmp/test_exploration.json")
        mock_path.parent.mkdir.return_value = None

        with patch("builtins.open", mock_open()) as mock_file:
            save_exploration(self.sample_session)

        mock_file.assert_called_once()
        # Verify the written data contains the session
        call_args = mock_file()
        self.assertTrue(call_args.write.called)

    @patch("notecli.cli.storage._EXPLORATION_PATH")
    def test_clear_exploration_removes_file(self, mock_path):
        """Should remove exploration file when it exists."""
        mock_path.exists.return_value = True
        mock_path.unlink = unittest.mock.MagicMock()

        clear_exploration()
        mock_path.unlink.assert_called_once()

    @patch("notecli.cli.storage._EXPLORATION_PATH")
    def test_clear_exploration_no_file(self, mock_path):
        """Should do nothing when file doesn't exist."""
        mock_path.exists.return_value = False
        mock_path.unlink = unittest.mock.MagicMock()

        clear_exploration()
        mock_path.unlink.assert_not_called()


if __name__ == "__main__":
    unittest.main()
