"""Tests for DungeonGraph and segment generation functions."""

import unittest
from unittest.mock import patch

from notecli.entities.segment import Segment, SegmentType
from notecli.entities.dungeon import (
    DungeonGraph,
    generate_initial_segment,
    generate_next_segment,
)


class TestDungeonGraph(unittest.TestCase):
    """Tests for DungeonGraph class."""

    def test_create_segment(self):
        graph = DungeonGraph()
        seg = graph.create_segment(SegmentType.CORREDOR, 1, 2)
        self.assertEqual(seg.id, 0)
        self.assertEqual(seg.type, SegmentType.CORREDOR)
        self.assertEqual(len(graph.segments), 1)

    def test_auto_increment_ids(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.CORREDOR, 1, 1)
        s2 = graph.create_segment(SegmentType.SALA, 1, 0)
        self.assertEqual(s1.id, 0)
        self.assertEqual(s2.id, 1)

    def test_set_current_and_current_segment(self):
        graph = DungeonGraph()
        seg = graph.create_segment(SegmentType.ESCADARIA, 1, 1)
        graph.set_current(seg.id)
        self.assertEqual(graph.current_segment_id, seg.id)
        self.assertEqual(graph.current_segment(), seg)

    def test_visited_stack_push(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, 1)
        s2 = graph.create_segment(SegmentType.CORREDOR, 1, 2)
        graph.set_current(s1.id)
        graph.set_current(s2.id)
        self.assertEqual(graph.visited_stack, [s1.id, s2.id])

    def test_backtrack(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, 1)
        s2 = graph.create_segment(SegmentType.CORREDOR, 1, 2)
        graph.set_current(s1.id)
        graph.set_current(s2.id)

        result = graph.backtrack()
        self.assertEqual(result, s1)
        self.assertEqual(graph.current_segment_id, s1.id)
        self.assertEqual(graph.visited_stack, [s1.id])

    def test_backtrack_at_entrance_returns_none(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, 1)
        graph.set_current(s1.id)

        result = graph.backtrack()
        self.assertIsNone(result)

    def test_is_at_entrance(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, 1)
        graph.set_current(s1.id)
        self.assertTrue(graph.is_at_entrance())

        s2 = graph.create_segment(SegmentType.CORREDOR, 1, 2)
        graph.set_current(s2.id)
        self.assertFalse(graph.is_at_entrance())

    def test_max_level_tracking(self):
        graph = DungeonGraph()
        graph.create_segment(SegmentType.ESCADARIA, 1, 1)
        self.assertEqual(graph.max_level, 1)
        graph.create_segment(SegmentType.ESCADARIA, 2, 1)
        self.assertEqual(graph.max_level, 2)

    def test_to_dict_and_from_dict(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, 1)
        s2 = graph.create_segment(SegmentType.CORREDOR, 1, 2)
        s1.add_connection(0, s2.id)
        graph.set_current(s1.id)
        graph.set_current(s2.id)

        data = graph.to_dict()
        restored = DungeonGraph.from_dict(data)

        self.assertEqual(len(restored.segments), 2)
        self.assertEqual(restored.current_segment_id, s2.id)
        self.assertEqual(restored.max_level, 1)
        self.assertEqual(restored.visited_stack, [s1.id, s2.id])
        self.assertEqual(restored.segments[0].get_target(0), s2.id)


class TestGenerateInitialSegment(unittest.TestCase):
    """T008: Test initial segment generation."""

    def test_initial_segment_is_staircase_level_1_with_1_door(self):
        graph = DungeonGraph()
        seg = generate_initial_segment(graph)
        self.assertEqual(seg.type, SegmentType.ESCADARIA)
        self.assertEqual(seg.level, 1)
        self.assertEqual(seg.doors_count, 1)
        self.assertEqual(graph.current_segment_id, seg.id)
        self.assertEqual(graph.visited_stack, [seg.id])


class TestGenerateNextSegment(unittest.TestCase):
    """Tests for generate_next_segment function."""

    def _make_graph_with_segment(self, seg_type, level, doors):
        graph = DungeonGraph()
        seg = graph.create_segment(seg_type, level, doors)
        graph.set_current(seg.id)
        return graph, seg

    @patch("random.randint")
    def test_open_door_from_staircase_generates_corridor(self, mock_rand):
        """T013: Opening door from staircase generates corridor."""
        mock_rand.return_value = 1  # First entry = corridor 1 door
        graph, stair = self._make_graph_with_segment(SegmentType.ESCADARIA, 1, 1)

        new_seg = generate_next_segment(graph, 0)

        self.assertEqual(new_seg.type, SegmentType.CORREDOR)
        self.assertEqual(new_seg.level, 1)
        self.assertTrue(stair.is_connected(0))
        self.assertEqual(stair.get_target(0), new_seg.id)

    @patch("random.randint")
    def test_staircase_increases_level(self, mock_rand):
        """T016: Staircase destination increases level by 1."""
        # Corridor table entry 5 = staircase
        mock_rand.return_value = 6
        graph, corr = self._make_graph_with_segment(SegmentType.CORREDOR, 1, 1)

        new_seg = generate_next_segment(graph, 0)

        self.assertEqual(new_seg.type, SegmentType.ESCADARIA)
        self.assertEqual(new_seg.level, 2)

    @patch("random.randint")
    def test_already_opened_door_returns_existing(self, mock_rand):
        """T017: Opening already opened door returns existing segment."""
        graph, stair = self._make_graph_with_segment(SegmentType.ESCADARIA, 1, 1)
        # First open the door
        mock_rand.return_value = 1
        first_seg = generate_next_segment(graph, 0)

        # Reset graph to have corridor as current but stair still has connection
        graph.set_current(stair.id)

        # Open same door again
        second_seg = generate_next_segment(graph, 0)

        self.assertEqual(first_seg.id, second_seg.id)

    def test_invalid_door_index_raises(self):
        graph, _ = self._make_graph_with_segment(SegmentType.ESCADARIA, 1, 1)
        with self.assertRaises(ValueError):
            generate_next_segment(graph, 5)

    def test_no_current_segment_raises(self):
        graph = DungeonGraph()
        with self.assertRaises(ValueError):
            generate_next_segment(graph, 0)

    @patch("random.randint")
    def test_final_room_at_level_3(self, mock_rand):
        """T026: Entering level 3 generates Final Room."""
        # Create a level 2 corridor that opens to staircase
        # CORRIDOR_TRANSITIONS[5] = {"type": "escadaria", "doors": 1}
        mock_rand.return_value = 6
        graph, corr = self._make_graph_with_segment(SegmentType.CORREDOR, 2, 1)

        new_seg = generate_next_segment(graph, 0)

        self.assertEqual(new_seg.type, SegmentType.SALA_FINAL)
        self.assertTrue(new_seg.is_final_room)


if __name__ == "__main__":
    unittest.main()
