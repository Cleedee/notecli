"""Tests for Door and DoorState entities."""

import unittest
from unittest.mock import patch

from notecli.entities.door import Door, DoorState
from notecli.entities.dungeon import roll_door
from notecli.entities.segment import Segment, SegmentType, create_doors_for_segment


class TestDoorState(unittest.TestCase):
    """Tests for DoorState enum."""

    def test_has_four_values(self):
        self.assertEqual(len(DoorState), 4)

    def test_door_state_values(self):
        expected = {"fechada", "armadilha", "trancada", "destrancada"}
        actual = {ds.value for ds in DoorState}
        self.assertEqual(actual, expected)


class TestDoor(unittest.TestCase):
    """Tests for Door entity."""

    def test_door_creation(self):
        door = Door(index=0, state=DoorState.FECHADA, target_segment_id=1)
        self.assertEqual(door.index, 0)
        self.assertEqual(door.state, DoorState.FECHADA)
        self.assertEqual(door.target_segment_id, 1)
        self.assertIsNone(door.trap_result)

    def test_is_opened(self):
        door = Door(index=0, state=DoorState.FECHADA, target_segment_id=1)
        self.assertFalse(door.is_opened())
        door.state = DoorState.DESTRANCADA
        self.assertTrue(door.is_opened())

    def test_is_locked(self):
        door = Door(index=0, state=DoorState.TRANCADA, target_segment_id=1)
        self.assertTrue(door.is_locked())
        door.state = DoorState.DESTRANCADA
        self.assertFalse(door.is_locked())

    def test_to_dict(self):
        door = Door(index=0, state=DoorState.FECHADA, target_segment_id=5)
        data = door.to_dict()
        self.assertEqual(data["index"], 0)
        self.assertEqual(data["state"], "fechada")
        self.assertEqual(data["target_segment_id"], 5)
        self.assertIsNone(data["trap_result"])

    def test_from_dict(self):
        data = {
            "index": 2,
            "state": "trancada",
            "target_segment_id": 10,
            "trap_result": "spike trap",
        }
        door = Door.from_dict(data)
        self.assertEqual(door.index, 2)
        self.assertEqual(door.state, DoorState.TRANCADA)
        self.assertEqual(door.target_segment_id, 10)
        self.assertEqual(door.trap_result, "spike trap")


class TestRollDoor(unittest.TestCase):
    """Tests for roll_door function."""

    @patch("notecli.entities.dungeon.random.randint")
    def test_roll_1_returns_armadilha(self, mock_rand):
        mock_rand.return_value = 1
        self.assertEqual(roll_door(), DoorState.ARMADILHA)

    @patch("notecli.entities.dungeon.random.randint")
    def test_roll_2_returns_trancada(self, mock_rand):
        mock_rand.return_value = 2
        self.assertEqual(roll_door(), DoorState.TRANCADA)

    @patch("notecli.entities.dungeon.random.randint")
    def test_roll_3_returns_trancada(self, mock_rand):
        mock_rand.return_value = 3
        self.assertEqual(roll_door(), DoorState.TRANCADA)

    @patch("notecli.entities.dungeon.random.randint")
    def test_roll_4_returns_destrancada(self, mock_rand):
        mock_rand.return_value = 4
        self.assertEqual(roll_door(), DoorState.DESTRANCADA)

    @patch("notecli.entities.dungeon.random.randint")
    def test_roll_5_returns_destrancada(self, mock_rand):
        mock_rand.return_value = 5
        self.assertEqual(roll_door(), DoorState.DESTRANCADA)

    @patch("notecli.entities.dungeon.random.randint")
    def test_roll_6_returns_destrancada(self, mock_rand):
        mock_rand.return_value = 6
        self.assertEqual(roll_door(), DoorState.DESTRANCADA)


class TestSegmentWithDoors(unittest.TestCase):
    """Tests for Segment with doors list."""

    def test_create_doors_for_segment(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1)
        create_doors_for_segment(seg, [1, 2])
        self.assertEqual(len(seg.doors), 2)
        self.assertEqual(seg.doors[0].target_segment_id, 1)
        self.assertEqual(seg.doors[0].state, DoorState.FECHADA)
        self.assertEqual(seg.doors_count, 2)

    def test_remaining_doors_count(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1)
        create_doors_for_segment(seg, [1, 2])
        self.assertEqual(seg.remaining_doors_count(), 2)
        seg.doors[0].state = DoorState.DESTRANCADA
        self.assertEqual(seg.remaining_doors_count(), 1)

    def test_locked_doors_count(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1)
        create_doors_for_segment(seg, [1, 2, 3])
        seg.doors[0].state = DoorState.TRANCADA
        seg.doors[1].state = DoorState.TRANCADA
        self.assertEqual(seg.locked_doors_count(), 2)

    def test_get_door(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1)
        create_doors_for_segment(seg, [1])
        self.assertIsNotNone(seg.get_door(0))
        self.assertIsNone(seg.get_door(5))

    def test_to_dict_and_from_dict(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1)
        create_doors_for_segment(seg, [1, 2])
        seg.doors[0].state = DoorState.TRANCADA

        data = seg.to_dict()
        restored = Segment.from_dict(data)

        self.assertEqual(restored.id, 0)
        self.assertEqual(len(restored.doors), 2)
        self.assertEqual(restored.doors[0].state, DoorState.TRANCADA)


if __name__ == "__main__":
    unittest.main()
