"""Tests for dungeon name generation."""

import unittest
from unittest.mock import patch

from notecli.entities.dungeon_name import generate_dungeon_name
from notecli.entities.dungeon import DungeonType


class TestDungeonNameGeneration(unittest.TestCase):
    """Tests for the generate_dungeon_name function."""

    def _make_dungeon_type(self, article="O", name="Palácio"):
        return DungeonType(
            article=article,
            name=name,
            entrance_description="Um dungeon de teste.",
        )

    def test_name_has_at_least_4_parts(self):
        """Generated name should have: article + substantive + adjectival_phrase + adjective."""
        dungeon_type = self._make_dungeon_type()
        name = generate_dungeon_name(dungeon_type)
        parts = name.split()
        self.assertGreaterEqual(len(parts), 4)

    def test_name_starts_with_article(self):
        """First word should match the dungeon type's article."""
        dungeon_type = self._make_dungeon_type(article="A", name="Cripta")
        name = generate_dungeon_name(dungeon_type)
        first_word = name.split()[0]
        self.assertEqual(first_word, "A")

    def test_name_contains_substantive(self):
        """Second word should be the dungeon type's name (substantive)."""
        dungeon_type = self._make_dungeon_type(article="O", name="Templo")
        name = generate_dungeon_name(dungeon_type)
        parts = name.split()
        self.assertEqual(parts[1], "Templo")

    def test_name_is_not_empty(self):
        """Generated name should never be empty."""
        dungeon_type = self._make_dungeon_type()
        name = generate_dungeon_name(dungeon_type)
        self.assertTrue(len(name) > 0)

    @patch("notecli.entities.dungeon_name.random.choice")
    def test_name_uses_tables_in_order(self, mock_choice):
        """Name should be composed from tables: article (from type) + substantive (from type) + adjectival + adjective."""
        mock_choice.side_effect = ["da", "Dor"]
        dungeon_type = self._make_dungeon_type(article="O", name="Palácio")
        name = generate_dungeon_name(dungeon_type)
        self.assertEqual(name, "O Palácio da Dor")

    def test_name_contains_adjective_from_third_part(self):
        """Name should contain an adjective from the third_part table."""
        from notecli.tables import third_part

        dungeon_type = self._make_dungeon_type()
        name = generate_dungeon_name(dungeon_type)
        parts = name.split()
        found = any(p in third_part for p in parts)
        self.assertTrue(found)


if __name__ == "__main__":
    unittest.main()
