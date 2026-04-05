"""Tests for character storage (load/save JSON)."""

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from notecli.cli.storage import load_characters, save_characters, _STORAGE_PATH


class TestLoadCharacters(unittest.TestCase):
    """T014-T016: Test storage load with various conditions."""

    def setUp(self):
        """Remove storage file before each test for isolation."""
        if _STORAGE_PATH.exists():
            _STORAGE_PATH.unlink()
        _STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        """Clean up storage file after each test."""
        if _STORAGE_PATH.exists():
            _STORAGE_PATH.unlink()

    def test_load_missing_file_returns_empty(self):
        """T015: Missing file should return empty list."""
        self.assertFalse(_STORAGE_PATH.exists())
        result = load_characters()
        self.assertEqual(result, [])

    def test_load_valid_json(self):
        """T014: Valid JSON file should return characters list."""
        data = {
            "version": 1,
            "characters": [
                {"name": "TestChar", "ancestry": "Humano", "occupation": "Ferreiro",
                 "health_points": 24, "hp_current": 24, "torches": 10,
                 "light_on": False, "starting_weapon": "martelo",
                 "alive": True, "magics": []}
            ]
        }
        with open(_STORAGE_PATH, "w") as f:
            json.dump(data, f)

        result = load_characters()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "TestChar")
        self.assertEqual(result[0]["ancestry"], "Humano")

    def test_load_corrupted_json(self):
        """T016: Corrupted JSON should raise ValueError."""
        with open(_STORAGE_PATH, "w") as f:
            f.write("{not valid json!!!")

        with self.assertRaises(ValueError):
            load_characters()

    def test_load_empty_characters_array(self):
        """Edge case: file with empty characters array."""
        data = {"version": 1, "characters": []}
        with open(_STORAGE_PATH, "w") as f:
            json.dump(data, f)

        result = load_characters()
        self.assertEqual(result, [])


class TestSaveCharacters(unittest.TestCase):
    """T017: Test storage save writes valid JSON."""

    def setUp(self):
        if _STORAGE_PATH.exists():
            _STORAGE_PATH.unlink()
        _STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if _STORAGE_PATH.exists():
            _STORAGE_PATH.unlink()

    def test_save_writes_valid_json(self):
        """T017: Save should write valid JSON with correct structure."""
        characters = [
            {"name": "Jackie", "ancestry": "Humano", "occupation": "Vagabond",
             "health_points": 24, "hp_current": 24, "torches": 10,
             "light_on": False, "starting_weapon": "pedaço de pau",
             "alive": True, "magics": []}
        ]
        save_characters(characters)

        self.assertTrue(_STORAGE_PATH.exists())
        with open(_STORAGE_PATH, "r") as f:
            data = json.load(f)

        self.assertEqual(data["version"], 1)
        self.assertEqual(len(data["characters"]), 1)
        self.assertEqual(data["characters"][0]["name"], "Jackie")

    def test_save_overwrites_previous(self):
        """Save should replace previous content entirely."""
        # First save
        save_characters([{"name": "Old", "ancestry": "", "occupation": "",
                          "health_points": 0, "hp_current": 0, "torches": 0,
                          "light_on": False, "starting_weapon": "", "alive": True, "magics": []}])
        # Second save
        save_characters([{"name": "New", "ancestry": "", "occupation": "",
                          "health_points": 0, "hp_current": 0, "torches": 0,
                          "light_on": False, "starting_weapon": "", "alive": True, "magics": []}])

        result = load_characters()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "New")


if __name__ == "__main__":
    unittest.main()
