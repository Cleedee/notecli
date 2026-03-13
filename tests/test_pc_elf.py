import unittest
from unittest.mock import Mock

from notecli.entities import PlayerCharacter
from notecli.entities.magic import factory_magic
from notecli.dice import Roller
from notecli import tables

Roller = Mock()

class TestElf(unittest.TestCase):

    def setUp(self):
        self.pc = PlayerCharacter(
            name="Naliash",
            torches=10,
            occupation="Noble"
        )

    def test_use_heal(self):
        ancestry = tables.ANCESTRIES[6] # Elf
        Roller.d6.return_value = 1
        ancestry.apply(self.pc)
        self.pc.use_magic(0)
        self.assertEqual(self.pc.ancestry, "Elfo")
        self.assertEqual(self.pc.health_points, 16, "Está no máximo de seus pontos de vida")

if __name__ == '__main__':
    unittest.main()
