"""Tests for dungeon name generation."""

import unittest
from unittest.mock import patch

from notecli.entities.dungeon_name import generate_dungeon_name


class TestDungeonNameGeneration(unittest.TestCase):
    """Tests for the generate_dungeon_name function."""

    def test_name_has_at_least_4_parts(self):
        """Generated name should have: article + substantive + preposition + modifier."""
        name = generate_dungeon_name()
        parts = name.split()
        self.assertGreaterEqual(len(parts), 4)

    def test_name_starts_with_article(self):
        """First word should be a valid article."""
        articles = {"O", "A", "As", "Os"}
        name = generate_dungeon_name()
        first_word = name.split()[0]
        self.assertIn(first_word, articles)

    def test_name_is_not_empty(self):
        """Generated name should never be empty."""
        name = generate_dungeon_name()
        self.assertTrue(len(name) > 0)

    @patch("notecli.entities.dungeon_name.random.choice")
    def test_name_uses_tables_in_order(self, mock_choice):
        """Name should be composed from tables in order: article, substantive, preposition, modifier."""
        mock_choice.side_effect = ["O", "Palácio", "da", "Dor"]
        name = generate_dungeon_name()
        self.assertEqual(name, "O Palácio da Dor")

    def test_name_contains_preposition(self):
        """Name should contain a preposition."""
        prepositions = {"de", "da", "do", "das", "dos"}
        name = generate_dungeon_name()
        parts = name.split()
        found = any(p in prepositions for p in parts)
        self.assertTrue(found)


if __name__ == "__main__":
    unittest.main()
