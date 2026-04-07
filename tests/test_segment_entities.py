"""Tests for Segment entity (updated for new Door model)."""

import unittest

from notecli.entities.segment import Segment, SegmentType, create_doors_for_segment
from notecli.entities.door import Door


class TestSegmentType(unittest.TestCase):
    def test_has_four_values(self):
        self.assertEqual(len(SegmentType), 4)

    def test_segment_type_values(self):
        expected = {"escadaria", "corredor", "sala", "sala_final"}
        actual = {st.value for st in SegmentType}
        self.assertEqual(actual, expected)


class TestSegment(unittest.TestCase):
    def test_segment_creation(self):
        seg = Segment(id=0, type=SegmentType.ESCADARIA, level=1)
        self.assertEqual(seg.id, 0)
        self.assertEqual(seg.type, SegmentType.ESCADARIA)
        self.assertEqual(seg.level, 1)
        self.assertEqual(seg.doors_count, 0)

    def test_final_room_segment(self):
        seg = Segment(id=5, type=SegmentType.SALA_FINAL, level=3, is_final_room=True)
        self.assertTrue(seg.is_final_room)

    def test_opened_doors_count(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1)
        create_doors_for_segment(seg, [1, 2])
        self.assertEqual(seg.opened_doors_count(), 0)
        seg.doors[0].is_open = True
        self.assertEqual(seg.opened_doors_count(), 1)

    def test_remaining_doors_count(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1)
        create_doors_for_segment(seg, [1, 2, 3])
        self.assertEqual(seg.remaining_doors_count(), 3)
        seg.doors[0].is_open = True
        self.assertEqual(seg.remaining_doors_count(), 2)

    def test_get_door(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1)
        create_doors_for_segment(seg, [1])
        self.assertIsNotNone(seg.get_door(0))
        self.assertIsNone(seg.get_door(5))

    def test_to_dict(self):
        seg = Segment(id=0, type=SegmentType.ESCADARIA, level=1)
        create_doors_for_segment(seg, [1])
        data = seg.to_dict()
        self.assertEqual(data["id"], 0)
        self.assertEqual(data["type"], "escadaria")
        self.assertEqual(len(data["doors"]), 1)

    def test_from_dict(self):
        data = {
            "id": 3,
            "type": "corredor",
            "level": 2,
            "doors": [{"index": 0, "is_open": False, "is_locked": False, "has_trap": False, "target_segment_id": 4}],
            "is_final_room": False,
            "has_monsters": True,
        }
        seg = Segment.from_dict(data)
        self.assertEqual(seg.id, 3)
        self.assertEqual(seg.type, SegmentType.CORREDOR)
        self.assertEqual(seg.level, 2)
        self.assertEqual(seg.doors_count, 1)
        self.assertTrue(seg.has_monsters)


if __name__ == "__main__":
    unittest.main()
