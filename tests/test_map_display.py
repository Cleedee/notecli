"""Tests for dungeon map display."""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import json

from notecli.cli.map_display import display_map
from notecli.entities.dungeon import DungeonGraph, DungeonType
from notecli.entities.segment import Segment, SegmentType, create_doors_for_segment
from notecli.entities.door import DoorState


class TestMapDisplay(unittest.TestCase):
    """Tests for the display_map function."""

    def _make_session_data(self):
        """Create sample session data with a simple dungeon."""
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, [1])
        s2 = graph.create_segment(SegmentType.CORREDOR, 1, [2, 3])
        s3 = graph.create_segment(SegmentType.SALA, 1, [])
        s4 = graph.create_segment(SegmentType.SALA_FINAL, 2, [])
        graph.set_current(s1.id)

        dungeon_type = DungeonType(
            article="O", name="Templo", entrance_description="Um templo antigo."
        )
        from notecli.entities.dungeon import Dungeon, ExplorationSession

        dungeon = Dungeon(type=dungeon_type, name="O Templo da Dor")
        session = ExplorationSession(
            dungeon=dungeon,
            character_index=1,
            started_at="2026-04-05T10:00:00",
            active=True,
            segment_graph=graph,
        )
        return session.to_dict()

    @patch("notecli.cli.map_display.load_exploration")
    def test_map_displays_all_segments(self, mock_load):
        """T001: Map must display all segments when session exists."""
        mock_load.return_value = self._make_session_data()

        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            display_map()
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("Escadaria", output)
        self.assertIn("Corredor", output)
        self.assertIn("Sala", output)
        self.assertIn("Sala Final", output)

    @patch("notecli.cli.map_display.load_exploration")
    def test_no_session_message(self, mock_load):
        """T002: When no session exists, show informative message."""
        mock_load.return_value = None

        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            display_map()
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("Nenhuma masmorra", output)

    @patch("notecli.cli.map_display.load_exploration")
    def test_map_shows_door_states(self, mock_load):
        """T003: Map must show door states (Fechada, Trancada, Destrancada)."""
        data = self._make_session_data()
        # Set some door states
        data["segment_graph"]["segments"]["0"]["doors"][0]["state"] = "trancada"
        mock_load.return_value = data

        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            display_map()
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("Trancada", output)

    @patch("notecli.cli.map_display.load_exploration")
    def test_legend_includes_segment_symbols(self, mock_load):
        """T006: Legend must include all segment type symbols."""
        mock_load.return_value = self._make_session_data()

        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            display_map()
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("Legenda", output)
        self.assertIn("Escadaria", output)
        self.assertIn("Corredor", output)
        self.assertIn("Sala", output)
        self.assertIn("Sala Final", output)

    @patch("notecli.cli.map_display.load_exploration")
    def test_legend_includes_door_symbols(self, mock_load):
        """T007: Legend must include all door state symbols."""
        mock_load.return_value = self._make_session_data()

        captured = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            display_map()
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        self.assertIn("Fechada", output)
        self.assertIn("Trancada", output)
        self.assertIn("Destrancada", output)


if __name__ == "__main__":
    unittest.main()
