import unittest

from notecli.entities import PlayerCharacter
from notecli.entities.magic import factory_magic
from notecli import tables

class TestElf(unittest.TestCase):

    def setUp(self):
        self.pc = PlayerCharacter(
            name="Naliash",
            torches=10,
            occupation="Noble"
        )
        ancestry = tables.ANCESTRIES[6] # Elf
        ancestry.apply(self.pc)

    def test_use_heal(self):
        self.pc.use_magic(0)
        self.assertEqual(self.pc.health_points, 16, "Está no máximo de seus pontos de vida")

if __name__ == '__main__':
    unittest.main()
