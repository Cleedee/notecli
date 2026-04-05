"""Tests for trap tables."""

import unittest

from notecli import tables


class TestTrapTables(unittest.TestCase):
    """Tests for TRAP_TABLES."""

    def test_has_six_tables(self):
        """Must have exactly 6 trap tables."""
        self.assertEqual(len(tables.TRAP_TABLES), 6)

    def test_each_table_has_6_entries(self):
        """Each trap table must have exactly 6 entries."""
        for name, table in tables.TRAP_TABLES.items():
            self.assertEqual(len(table), 6, f"{name} trap table must have 6 entries")

    def test_all_entries_are_strings(self):
        """All trap table entries must be strings."""
        for name, table in tables.TRAP_TABLES.items():
            for i, entry in enumerate(table):
                self.assertIsInstance(entry, str, f"{name}[{i}] is not a string")

    def test_known_dungeon_type_keys(self):
        """Trap tables must have keys for all 6 dungeon types."""
        expected_keys = {"Palácio", "Cripta", "Tumba", "Santuário", "Templo", "Calabouço"}
        self.assertEqual(set(tables.TRAP_TABLES.keys()), expected_keys)


if __name__ == "__main__":
    unittest.main()
