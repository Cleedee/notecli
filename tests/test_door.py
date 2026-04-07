"""Tests for Door entity with 3 independent attributes."""

import unittest
from unittest.mock import patch

from notecli.entities.door import Door
from notecli.entities.dungeon import roll_door, close_opened_doors, enter_room
from notecli.entities.dungeon import DungeonGraph
from notecli.entities.segment import Segment, SegmentType, create_doors_for_segment


class TestDoor(unittest.TestCase):
    """Tests for the new Door entity."""

    def test_door_creation_closed(self):
        """New doors should be closed, unlocked, no trap."""
        door = Door(index=0, is_open=False, is_locked=False, has_trap=False, target_segment_id=1)
        self.assertFalse(door.is_open)
        self.assertFalse(door.is_locked)
        self.assertFalse(door.has_trap)
        self.assertEqual(door.target_segment_id, 1)

    def test_door_display_closed(self):
        self.assertEqual(Door(0).display_status(), "🔒 Fechada")

    def test_door_display_open(self):
        door = Door(0, is_open=True)
        self.assertEqual(door.display_status(), "✅ Aberta")

    def test_door_display_locked(self):
        door = Door(0, is_locked=True)
        self.assertIn("Trancada", door.display_status())

    def test_door_display_trap(self):
        door = Door(0, has_trap=True)
        self.assertIn("Armadilha", door.display_status())

    def test_close_door(self):
        door = Door(0, is_open=True, target_segment_id=1)
        door.close()
        self.assertFalse(door.is_open)

    def test_can_enter(self):
        door = Door(0, is_open=True, target_segment_id=1)
        self.assertTrue(door.can_enter())

    def test_cannot_enter_locked(self):
        door = Door(0, is_open=True, is_locked=True, target_segment_id=1)
        self.assertFalse(door.can_enter())

    def test_cannot_enter_trap(self):
        door = Door(0, is_open=True, has_trap=True, target_segment_id=1)
        self.assertFalse(door.can_enter())

    def test_is_revealed(self):
        door = Door(0, target_segment_id=1)
        self.assertTrue(door.is_revealed())

    def test_to_dict_and_from_dict(self):
        door = Door(index=0, is_open=True, is_locked=False, has_trap=True, target_segment_id=5)
        data = door.to_dict()
        restored = Door.from_dict(data)
        self.assertEqual(restored.index, 0)
        self.assertTrue(restored.is_open)
        self.assertFalse(restored.is_locked)
        self.assertTrue(restored.has_trap)
        self.assertEqual(restored.target_segment_id, 5)

    def test_from_dict_migration_old_state(self):
        """Test backward compatibility with old state string format."""
        data = {"index": 0, "state": "destrancada", "target_segment_id": 1}
        door = Door.from_dict(data)
        self.assertTrue(door.is_open)

        data = {"index": 0, "state": "trancada", "target_segment_id": 1}
        door = Door.from_dict(data)
        self.assertTrue(door.is_locked)

        data = {"index": 0, "state": "armadilha", "target_segment_id": 1}
        door = Door.from_dict(data)
        self.assertTrue(door.has_trap)


class TestRollDoor(unittest.TestCase):
    """Tests for the roll_door function."""

    @patch("notecli.entities.dungeon.random.randint")
    def test_roll_1_armadilha(self, mock_rand):
        mock_rand.return_value = 1
        name, msg = roll_door()
        self.assertEqual(name, "armadilha")

    @patch("notecli.entities.dungeon.random.randint")
    def test_roll_2_trancada(self, mock_rand):
        mock_rand.return_value = 2
        name, msg = roll_door()
        self.assertEqual(name, "trancada")

    @patch("notecli.entities.dungeon.random.randint")
    def test_roll_3_trancada(self, mock_rand):
        mock_rand.return_value = 3
        name, msg = roll_door()
        self.assertEqual(name, "trancada")

    @patch("notecli.entities.dungeon.random.randint")
    def test_roll_4_destrancada(self, mock_rand):
        mock_rand.return_value = 4
        name, msg = roll_door()
        self.assertEqual(name, "destrancada")

    @patch("notecli.entities.dungeon.random.randint")
    def test_roll_6_destrancada(self, mock_rand):
        mock_rand.return_value = 6
        name, msg = roll_door()
        self.assertEqual(name, "destrancada")


class TestCloseOpenedDoors(unittest.TestCase):
    """Tests for close_opened_doors function."""

    def test_close_opened_doors(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1)
        create_doors_for_segment(seg, [1, 2, 3])
        seg.doors[0].is_open = True
        seg.doors[1].is_open = True

        count = close_opened_doors(seg)
        self.assertEqual(count, 2)
        self.assertFalse(seg.doors[0].is_open)
        self.assertFalse(seg.doors[1].is_open)
        self.assertFalse(seg.doors[2].is_open)  # Was already closed

    def test_close_preserves_lock_and_trap(self):
        seg = Segment(id=0, type=SegmentType.CORREDOR, level=1)
        create_doors_for_segment(seg, [1])
        seg.doors[0].is_open = True
        seg.doors[0].is_locked = True
        seg.doors[0].has_trap = True

        close_opened_doors(seg)
        self.assertFalse(seg.doors[0].is_open)
        self.assertTrue(seg.doors[0].is_locked)
        self.assertTrue(seg.doors[0].has_trap)


class TestEnterRoom(unittest.TestCase):
    """Tests for enter_room function."""

    def _make_graph_with_door_open(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.ESCADARIA, 1, [1])
        s2 = graph.create_segment(SegmentType.CORREDOR, 1, [])
        s1.doors[0].target_segment_id = s2.id
        s1.doors[0].is_open = True
        graph.set_current(s1.id)
        return graph

    def test_enter_moves_player(self):
        graph = self._make_graph_with_door_open()
        self.assertEqual(graph.current_segment_id, 0)

        success, msg = enter_room(graph, 0, "Templo")
        self.assertTrue(success)
        self.assertEqual(graph.current_segment_id, 1)

    def test_enter_closes_door(self):
        graph = self._make_graph_with_door_open()
        enter_room(graph, 0, "Templo")
        self.assertFalse(graph.segments[0].doors[0].is_open)

    def test_enter_closes_other_open_doors(self):
        graph = DungeonGraph()
        s1 = graph.create_segment(SegmentType.CORREDOR, 1, [1, 2])
        s2 = graph.create_segment(SegmentType.SALA, 1, [])
        s1.doors[0].target_segment_id = s2.id
        s1.doors[0].is_open = True
        s1.doors[1].is_open = True  # Another open door
        graph.set_current(s1.id)

        enter_room(graph, 0, "Templo")
        self.assertFalse(s1.doors[0].is_open)
        self.assertFalse(s1.doors[1].is_open)


if __name__ == "__main__":
    unittest.main()
