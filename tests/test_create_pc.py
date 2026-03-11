import unittest

from notecli.entities import PlayerCharacter
from notecli import tables

class TestCreatePC(unittest.TestCase):

    def test_create(self):
        pc = PlayerCharacter(
            health_points = 10,
            torches=3,
            ancestry="Dwarf",
            occupation="Blacksmith"
        )
        ancestry = tables.ANCESTRIES[2]
        ancestry.apply(pc)
        self.assertEqual(pc.health_points, 10)
        self.assertEqual

if __name__ == "__main__":
    unittest.main()
