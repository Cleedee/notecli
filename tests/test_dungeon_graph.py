"""Tests for DungeonGraph (updated for Door-based API)."""

import unittest
from unittest.mock import patch

from notecli.entities.segment import Segment, SegmentType, create_doors_for_segment
from notecli.entities.door import DoorState
from notecli.entities.dungeon import DungeonGraph


class TestDungeonGraph(unittest.TestCase):
    """Tests for DungeonGraph class."""

    def test_create_segment(self):
        graph = DungeonGraph()
        seg = graph.create_segment(SegmentType.CORREDOR, 1, [1, 2])
        self.assertEqual(seg.id, 0)
        self.assertEqual(seg.type, SegmentType.CORREDOR)
        self.assertEqual(len(graph.segments), 1)
        self.assertEqual(seg.doors_count, 2)

    def test_auto_increment_ids(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.CORREDOR, 1, [1])
        s2 = graph.create_segment(SegmentType.SALA, 1, [])
        self.assertEqual(s1.id, 0)
        self.assertEqual(s2.id, 1)

    def test_set_current_and_current_segment(self):
        graph = DungeonGraph()
        seg = graph.create_segment(SegmentType.ESCADARIA, 1, [1])
        graph.set_current(seg.id)
        self.assertEqual(graph.current_segment_id, seg.id)
        self.assertEqual(graph.current_segment(), seg)

    def test_visited_stack_push(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, [1])
        s2 = graph.create_segment(SegmentType.CORREDOR, 1, [2])
        graph.set_current(s1.id)
        graph.set_current(s2.id)
        self.assertEqual(graph.visited_stack, [s1.id, s2.id])

    def test_backtrack(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, [1])
        s2 = graph.create_segment(SegmentType.CORREDOR, 1, [2])
        graph.set_current(s1.id)
        graph.set_current(s2.id)

        result = graph.backtrack()
        self.assertEqual(result, s1)
        self.assertEqual(graph.current_segment_id, s1.id)
        self.assertEqual(graph.visited_stack, [s1.id])

    def test_backtrack_at_entrance_returns_none(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, [1])
        graph.set_current(s1.id)

        result = graph.backtrack()
        self.assertIsNone(result)

    def test_is_at_entrance(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, [1])
        graph.set_current(s1.id)
        self.assertTrue(graph.is_at_entrance())

        s2 = graph.create_segment(SegmentType.CORREDOR, 1, [2])
        graph.set_current(s2.id)
        self.assertFalse(graph.is_at_entrance())

    def test_max_level_tracking(self):
        graph = DungeonGraph()
        graph.create_segment(SegmentType.ESCADARIA, 1, [1])
        self.assertEqual(graph.max_level, 1)
        graph.create_segment(SegmentType.ESCADARIA, 2, [1])
        self.assertEqual(graph.max_level, 2)

    def test_to_dict_and_from_dict(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, [1])
        s2 = graph.create_segment(SegmentType.CORREDOR, 1, [2])
        graph.set_current(s1.id)
        graph.set_current(s2.id)

        data = graph.to_dict()
        restored = DungeonGraph.from_dict(data)

        self.assertEqual(len(restored.segments), 2)
        self.assertEqual(restored.current_segment_id, s2.id)
        self.assertEqual(restored.max_level, 1)
        self.assertEqual(restored.visited_stack, [s1.id, s2.id])


if __name__ == "__main__":
    unittest.main()
