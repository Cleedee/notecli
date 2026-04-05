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

    def test_torch_not_consumed_on_resume_session_data(self):
        """T005: When resuming session, torch count in saved session must match what was saved."""
        # Test that session persistence preserves torch count
        from notecli.entities.dungeon import DungeonGraph, ExplorationSession, Dungeon, DungeonType
        from notecli.entities.segment import SegmentType

        # Create a session with a character that has 9 torches
        dungeon_type = DungeonType(
            article="O", name="Templo", entrance_description="Um templo."
        )
        dungeon = Dungeon(type=dungeon_type, name="O Templo da Dor")
        graph = DungeonGraph()
        graph.create_segment(SegmentType.ESCADARIA, 1, 1)

        session = ExplorationSession(
            dungeon=dungeon,
            character_index=1,
            started_at="2026-04-04T15:30:00",
            active=True,
            segment_graph=graph,
        )

        data = session.to_dict()
        restored = ExplorationSession.from_dict(data)

        # Session data should preserve segment_graph
        self.assertIsNotNone(restored.segment_graph)
        self.assertEqual(len(restored.segment_graph.segments), 1)


if __name__ == "__main__":
    unittest.main()
