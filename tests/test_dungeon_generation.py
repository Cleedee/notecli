"""Tests for Dungeon, DungeonType, ExplorationSession entities and generation."""

import unittest
from datetime import datetime

from notecli.entities.dungeon import (
    DungeonType,
    Dungeon,
    ExplorationSession,
    generate_dungeon,
)
from notecli import tables


class TestDungeonType(unittest.TestCase):
    """Tests for the DungeonType entity."""

    def test_dungeon_type_creation(self):
        dt = DungeonType(name="Templo", entrance_description="Um templo antigo.")
        self.assertEqual(dt.name, "Templo")
        self.assertEqual(dt.entrance_description, "Um templo antigo.")

    def test_dungeon_type_in_tables(self):
        """All 6 dungeon types in DUNGEON_TYPES must be valid DungeonType instances."""
        for roll, dtype in tables.DUNGEON_TYPES.items():
            self.assertIsInstance(dtype, DungeonType)
            self.assertTrue(len(dtype.name) > 0)
            self.assertTrue(len(dtype.entrance_description) > 0)

    def test_dungeon_types_has_6_entries(self):
        self.assertEqual(len(tables.DUNGEON_TYPES), 6)


class TestDungeon(unittest.TestCase):
    """Tests for the Dungeon entity."""

    def setUp(self):
        self.dungeon_type = DungeonType(
            name="Cripta", entrance_description="Uma cripta escura."
        )

    def test_dungeon_creation(self):
        d = Dungeon(
            type=self.dungeon_type,
            name="A Cripta dos Ossos",
            entrance_shown=False,
            current_room=0,
            rooms_visited=0,
        )
        self.assertEqual(d.type.name, "Cripta")
        self.assertEqual(d.name, "A Cripta dos Ossos")
        self.assertFalse(d.entrance_shown)
        self.assertEqual(d.current_room, 0)
        self.assertEqual(d.rooms_visited, 0)

    def test_dungeon_entrance_marked_shown(self):
        d = Dungeon(
            type=self.dungeon_type,
            name="A Cripta",
            entrance_shown=False,
        )
        d.entrance_shown = True
        self.assertTrue(d.entrance_shown)


class TestExplorationSession(unittest.TestCase):
    """Tests for the ExplorationSession entity."""

    def setUp(self):
        dungeon_type = DungeonType(
            name="Templo", entrance_description="Um templo."
        )
        self.dungeon = Dungeon(
            type=dungeon_type,
            name="O Templo da Dor",
        )

    def test_session_creation(self):
        session = ExplorationSession(
            dungeon=self.dungeon,
            character_index=2,
            started_at="2026-04-04T15:30:00",
            active=True,
        )
        self.assertEqual(session.character_index, 2)
        self.assertTrue(session.active)
        self.assertEqual(session.dungeon.name, "O Templo da Dor")

    def test_session_to_dict(self):
        session = ExplorationSession(
            dungeon=self.dungeon,
            character_index=1,
            started_at="2026-04-04T15:30:00",
            active=True,
        )
        data = session.to_dict()
        self.assertEqual(data["character_index"], 1)
        self.assertEqual(data["dungeon"]["name"], "O Templo da Dor")
        self.assertEqual(data["dungeon"]["type_name"], "Templo")
        self.assertTrue(data["active"])

    def test_session_from_dict(self):
        data = {
            "dungeon": {
                "type_name": "Cripta",
                "name": "A Cripta Perdida",
                "entrance_shown": True,
                "current_room": 2,
                "rooms_visited": 2,
            },
            "character_index": 3,
            "started_at": "2026-04-04T16:00:00",
            "active": True,
        }
        session = ExplorationSession.from_dict(data)
        self.assertEqual(session.character_index, 3)
        self.assertTrue(session.active)
        self.assertEqual(session.dungeon.name, "A Cripta Perdida")
        self.assertEqual(session.dungeon.type.name, "Cripta")
        self.assertEqual(session.dungeon.current_room, 2)


class TestGenerateDungeon(unittest.TestCase):
    """Tests for the generate_dungeon function."""

    def test_generate_dungeon_valid_roll(self):
        """Rolls 1-6 must produce a valid dungeon."""
        for roll in range(1, 7):
            dungeon = generate_dungeon(roll)
            self.assertIsInstance(dungeon, Dungeon)
            self.assertIn(dungeon.type.name, [dt.name for dt in tables.DUNGEON_TYPES.values()])
            self.assertTrue(len(dungeon.name) > 0)
            self.assertFalse(dungeon.entrance_shown)

    def test_generate_dungeon_invalid_roll_raises(self):
        """Rolls outside 1-6 should raise ValueError."""
        for invalid in (0, 7, -1, 100):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    generate_dungeon(invalid)

    def test_generate_dungeon_name_pattern(self):
        """Generated name should match pattern: article + substantive + preposition + modifier."""
        dungeon = generate_dungeon(1)
        parts = dungeon.name.split()
        # At least 3 parts (e.g., "O Palácio da Dor" or "O Templo de Nebulosa")
        self.assertGreaterEqual(len(parts), 3)


if __name__ == "__main__":
    unittest.main()
