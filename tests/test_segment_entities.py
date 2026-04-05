"""Tests for Segment and SegmentType entities."""

import unittest

from notecli.entities.segment import Segment, SegmentType


class TestSegmentType(unittest.TestCase):
    """Tests for SegmentType enum."""

    def test_has_four_values(self):
        self.assertEqual(len(SegmentType), 4)

    def test_segment_type_values(self):
        expected = {"escadaria", "corredor", "sala", "sala_final"}
        actual = {st.value for st in SegmentType}
        self.assertEqual(actual, expected)


class TestSegment(unittest.TestCase):
    """Tests for Segment entity."""

    def test_segment_creation(self):
        seg = Segment(
            id=0,
            type=SegmentType.ESCADARIA,
            level=1,
            doors_count=1,
        )
        self.assertEqual(seg.id, 0)
        self.assertEqual(seg.type, SegmentType.ESCADARIA)
        self.assertEqual(seg.level, 1)
        self.assertEqual(seg.doors_count, 1)
        self.assertFalse(seg.is_final_room)
        self.assertFalse(seg.has_monsters)

    def test_final_room_segment(self):
        seg = Segment(
            id=5,
            type=SegmentType.SALA_FINAL,
            level=3,
            doors_count=0,
            is_final_room=True,
        )
        self.assertTrue(seg.is_final_room)
        self.assertEqual(seg.type, SegmentType.SALA_FINAL)

    def test_opened_doors_count(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1, doors_count=2)
        self.assertEqual(seg.opened_doors_count(), 0)
        seg.add_connection(0, 1)
        self.assertEqual(seg.opened_doors_count(), 1)

    def test_remaining_doors_count(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1, doors_count=3)
        self.assertEqual(seg.remaining_doors_count(), 3)
        seg.add_connection(0, 1)
        self.assertEqual(seg.remaining_doors_count(), 2)

    def test_is_connected(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1, doors_count=2)
        self.assertFalse(seg.is_connected(0))
        seg.add_connection(0, 1)
        self.assertTrue(seg.is_connected(0))
        self.assertFalse(seg.is_connected(1))

    def test_get_target(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1, doors_count=2)
        self.assertIsNone(seg.get_target(0))
        seg.add_connection(0, 5)
        self.assertEqual(seg.get_target(0), 5)
        self.assertIsNone(seg.get_target(1))

    def test_to_dict(self):
        seg = Segment(
            id=0,
            type=SegmentType.ESCADARIA,
            level=1,
            doors_count=1,
            is_final_room=False,
            has_monsters=False,
        )
        data = seg.to_dict()
        self.assertEqual(data["id"], 0)
        self.assertEqual(data["type"], "escadaria")
        self.assertEqual(data["level"], 1)
        self.assertEqual(data["doors_count"], 1)
        self.assertEqual(data["connected_segments"], [])

    def test_from_dict(self):
        data = {
            "id": 3,
            "type": "corredor",
            "level": 2,
            "doors_count": 2,
            "connected_segments": [[0, 4]],
            "is_final_room": False,
            "has_monsters": True,
        }
        seg = Segment.from_dict(data)
        self.assertEqual(seg.id, 3)
        self.assertEqual(seg.type, SegmentType.CORREDOR)
        self.assertEqual(seg.level, 2)
        self.assertEqual(seg.doors_count, 2)
        self.assertTrue(seg.has_monsters)
        self.assertEqual(seg.get_target(0), 4)


if __name__ == "__main__":
    unittest.main()
