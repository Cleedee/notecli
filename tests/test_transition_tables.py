"""Tests for dungeon transition tables."""

import unittest

from notecli import tables


class TestTransitionTables(unittest.TestCase):
    """Tests for STAIRCASE_TRANSITIONS, CORRIDOR_TRANSITIONS, ROOM_TRANSITIONS."""

    def test_staircase_table_has_6_entries(self):
        self.assertEqual(len(tables.STAIRCASE_TRANSITIONS), 6)

    def test_corridor_table_has_6_entries(self):
        self.assertEqual(len(tables.CORRIDOR_TRANSITIONS), 6)

    def test_room_table_has_6_entries(self):
        self.assertEqual(len(tables.ROOM_TRANSITIONS), 6)

    def test_staircase_only_generates_corridors(self):
        """FR-005: Staircase table must only generate corridors with 1-3 doors."""
        for entry in tables.STAIRCASE_TRANSITIONS:
            self.assertEqual(entry["type"], "corredor")
            self.assertIn(entry["doors"], (1, 2, 3))

    def test_corridor_generates_rooms_or_staircase(self):
        """FR-006: Corridor table generates rooms (1-2 doors) or staircase (1 door)."""
        staircase_count = 0
        for entry in tables.CORRIDOR_TRANSITIONS:
            if entry["type"] == "sala":
                self.assertIn(entry["doors"], (1, 2))
            elif entry["type"] == "escadaria":
                self.assertEqual(entry["doors"], 1)
                staircase_count += 1
        self.assertEqual(staircase_count, 1)

    def test_room_generates_dead_ends_or_staircase(self):
        """FR-007: Room table generates rooms with 0 doors or staircase (1 door)."""
        staircase_count = 0
        for entry in tables.ROOM_TRANSITIONS:
            if entry["type"] == "sala":
                self.assertEqual(entry["doors"], 0)
            elif entry["type"] == "escadaria":
                self.assertEqual(entry["doors"], 1)
                staircase_count += 1
        self.assertEqual(staircase_count, 1)

    def test_all_entries_have_type_and_doors(self):
        """All transition entries must have 'type' and 'doors' keys."""
        for table_name, table in [
            ("STAIRCASE", tables.STAIRCASE_TRANSITIONS),
            ("CORRIDOR", tables.CORRIDOR_TRANSITIONS),
            ("ROOM", tables.ROOM_TRANSITIONS),
        ]:
            for i, entry in enumerate(table):
                self.assertIn("type", entry, f"{table_name}[{i}] missing 'type'")
                self.assertIn("doors", entry, f"{table_name}[{i}] missing 'doors'")


if __name__ == "__main__":
    unittest.main()
