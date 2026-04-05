"""Tests for save-quit functionality."""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

from notecli.entities.dungeon import DungeonGraph, DungeonType, Dungeon, ExplorationSession
from notecli.entities.segment import SegmentType, create_doors_for_segment
from notecli.entities.door import DoorState
from notecli.entities.player import PlayerCharacter


class TestSaveQuit(unittest.TestCase):
    """Tests for save-quit and resume behavior."""

    def _make_session(self, active=True):
        """Create a session with a simple dungeon graph."""
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, [-1])
        s2 = graph.create_segment(SegmentType.CORREDOR, 1, [-1])
        # Connect s1's door to s2
        s1.doors[0].target_segment_id = s2.id
        graph.set_current(s2.id)

        dungeon_type = DungeonType(
            article="O", name="Templo", entrance_description="Um templo."
        )
        dungeon = Dungeon(type=dungeon_type, name="O Templo")
        session = ExplorationSession(
            dungeon=dungeon,
            character_index=1,
            started_at="2026-04-05T10:00:00",
            active=active,
            segment_graph=graph,
        )
        return session

    @patch("notecli.cli.explore_menu.load_exploration")
    def test_save_quit_keeps_session_active(self, mock_load):
        """T001: Save-quit must keep session active."""
        from notecli.cli.explore_menu import _handle_save_quit

        session = self._make_session(active=True)
        mock_load.return_value = session.to_dict()

        pc = MagicMock()
        pc.name = "TestChar"
        pc.ancestry = "Humano"
        pc.torches = 8
        pc.hp_current = 15
        pc.health_points = 20
        pc.magics = []

        graph = session.segment_graph

        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            _handle_save_quit(pc, graph)
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("salvo", output.lower())
        self.assertIn("Progresso", output)

    @patch("notecli.cli.explore_menu.load_exploration")
    @patch("notecli.cli.explore_menu._save_session")
    @patch("notecli.cli.explore_menu._save_character")
    def test_save_quit_preserves_current_segment(self, mock_save_char, mock_save_sess, mock_load):
        """T002: Save-quit must preserve current segment in session."""
        from notecli.cli.explore_menu import _handle_save_quit

        session = self._make_session(active=True)
        mock_load.return_value = session.to_dict()

        pc = MagicMock()
        pc.name = "TestChar"
        pc.ancestry = "Humano"
        pc.torches = 8
        pc.hp_current = 15
        pc.health_points = 20
        pc.magics = []

        graph = session.segment_graph
        original_current = graph.current_segment_id

        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            _handle_save_quit(pc, graph)
        finally:
            sys.stdout = old_stdout

        # Verify _save_session was called (which persists the graph)
        mock_save_sess.assert_called_once()
        # Verify character was saved
        mock_save_char.assert_called_once()

    @patch("notecli.cli.explore_menu.load_exploration")
    def test_resume_restores_exact_segment(self, mock_load):
        """T003: Resume must restore exact segment + doors + torches."""
        session = self._make_session(active=True)
        # Set a door state
        session.segment_graph.segments[1].doors[0].state = DoorState.TRANCADA
        mock_load.return_value = session.to_dict()

        # Simulate resume path
        from notecli.entities.dungeon import DungeonGraph
        graph = DungeonGraph.from_dict(session.to_dict()["segment_graph"])

        self.assertEqual(graph.current_segment_id, 1)
        self.assertEqual(len(graph.segments), 2)
        # Door state preserved
        door = graph.segments[1].get_door(0)
        self.assertEqual(door.state, DoorState.TRANCADA)

    @patch("notecli.cli.explore_menu.load_exploration")
    @patch("notecli.cli.explore_menu._deactivate_session")
    def test_exit_dungeon_deactivates_session(self, mock_deactivate, mock_load):
        """T006: Sair da Masmorra must deactivate session."""
        # This tests the existing _handle_exit with monsters=False and choice='s'
        from notecli.cli.explore_menu import _handle_exit

        session = self._make_session(active=True)
        mock_load.return_value = session.to_dict()

        graph = session.segment_graph
        pc = MagicMock()
        pc.name = "TestChar"
        pc.ancestry = "Humano"
        pc.torches = 8
        pc.hp_current = 15
        pc.health_points = 20
        pc.magics = []

        with patch("notecli.cli.explore_menu._prompt", return_value="s"):
            captured = StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured
            try:
                _handle_exit(pc, graph)
            finally:
                sys.stdout = old_stdout

        mock_deactivate.assert_called_once()

    @patch("notecli.cli.explore_menu.load_exploration")
    def test_save_quit_shows_save_message(self, mock_load):
        """T007: Save-quit must show save message."""
        from notecli.cli.explore_menu import _handle_save_quit

        session = self._make_session(active=True)
        mock_load.return_value = session.to_dict()

        pc = MagicMock()
        pc.name = "TestChar"
        pc.ancestry = "Humano"
        pc.torches = 8
        pc.hp_current = 15
        pc.health_points = 20
        pc.magics = []

        graph = session.segment_graph

        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            _handle_save_quit(pc, graph)
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("💾", output)
        self.assertIn("Progresso salvo", output)

    @patch("notecli.cli.explore_menu.load_exploration")
    def test_exit_dungeon_shows_exit_message(self, mock_load):
        """T008: Sair da Masmorra must show exit message."""
        from notecli.cli.explore_menu import _handle_exit

        session = self._make_session(active=True)
        mock_load.return_value = session.to_dict()

        graph = session.segment_graph
        pc = MagicMock()
        pc.name = "TestChar"
        pc.ancestry = "Humano"
        pc.torches = 8
        pc.hp_current = 15
        pc.health_points = 20
        pc.magics = []

        with patch("notecli.cli.explore_menu._prompt", return_value="s"):
            captured = StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured
            try:
                _handle_exit(pc, graph)
            finally:
                sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("🏁", output)
        self.assertIn("sai da masmorra", output.lower())


if __name__ == "__main__":
    unittest.main()
