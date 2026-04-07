"""Tests for dungeon pre-generation (updated for new Door model)."""

import unittest
from unittest.mock import patch

from notecli.entities.dungeon import DungeonGraph, generate_full_dungeon
from notecli.entities.segment import SegmentType



class TestDungeonPregen(unittest.TestCase):
    def test_all_doors_start_closed(self):
        """All doors must start closed after generation."""
        graph = DungeonGraph()
        generate_full_dungeon(graph, "Templo")
        for seg in graph.segments.values():
            for door in seg.doors:
                self.assertFalse(door.is_open)

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


if __name__ == "__main__":
    unittest.main()
