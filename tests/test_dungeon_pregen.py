"""Tests for dungeon pre-generation."""

import unittest
from unittest.mock import patch

from notecli.entities.dungeon import DungeonGraph, generate_full_dungeon, generate_initial_segment
from notecli.entities.segment import SegmentType
from notecli.entities.door import DoorState


class TestDungeonPregen(unittest.TestCase):
    """Tests for full dungeon pre-generation."""

    def test_initial_segment_is_staircase_level_1(self):
        """Initial segment must be staircase at level 1."""
        graph = DungeonGraph()
        seg = generate_initial_segment(graph)
        self.assertEqual(seg.type, SegmentType.ESCADARIA)
        self.assertEqual(seg.level, 1)
        self.assertEqual(seg.doors_count, 1)
        self.assertEqual(graph.current_segment_id, 0)

    @patch("notecli.entities.dungeon.random.randint")
    def test_full_dungeon_generates_segments(self, mock_rand):
        """Full dungeon generation must create multiple segments."""
        # Make transitions produce corridors and eventually a staircase
        # Staircase transitions always produce corridor
        # Corridor transition roll 6 = staircase
        mock_rand.side_effect = [
            1,  # staircase -> corridor 1 door
            6,  # corridor -> staircase (level 2)
            1,  # staircase -> corridor 1 door
            6,  # corridor -> staircase → Final Room (level 3)
        ]

        graph = DungeonGraph()
        generate_full_dungeon(graph, "Templo")

        self.assertGreater(len(graph.segments), 1)
        self.assertGreaterEqual(graph.max_level, 1)

    def test_all_doors_start_fechada(self):
        """All doors must start in FECHADA state after generation."""
        graph = DungeonGraph()
        generate_full_dungeon(graph, "Templo")

        for seg in graph.segments.values():
            for door in seg.doors:
                self.assertEqual(door.state, DoorState.FECHADA)

    def test_final_room_exists(self):
        """At least one segment must be the Final Room."""
        graph = DungeonGraph()
        generate_full_dungeon(graph, "Templo")

        final_rooms = [s for s in graph.segments.values() if s.is_final_room]
        self.assertGreaterEqual(len(final_rooms), 1)

    def test_graph_serialization_roundtrip(self):
        """DungeonGraph must serialize and deserialize correctly."""
        graph = DungeonGraph()
        generate_full_dungeon(graph, "Templo")

        data = graph.to_dict()
        restored = DungeonGraph.from_dict(data)

        self.assertEqual(len(restored.segments), len(graph.segments))
        self.assertEqual(restored.current_segment_id, graph.current_segment_id)
        self.assertEqual(restored.max_level, graph.max_level)
        self.assertEqual(restored.visited_stack, graph.visited_stack)


if __name__ == "__main__":
    unittest.main()
