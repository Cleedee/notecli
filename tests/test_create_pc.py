import unittest

from notecli.entities import PlayerCharacter
from notecli import tables

class TestCreatePC(unittest.TestCase):

    def setUp(self):
        self.pc = PlayerCharacter(
            name="Walter",
            torches=10,
            occupation="Blacksmith"
        )
        

    def test_ancestry_mendigo(self):
        ancestry = tables.ANCESTRIES[2]
        ancestry.apply(self.pc)
        self.assertEqual(self.pc.health_points, 10)
        self.assertEqual(self.pc.ancestry, "Homem-Gosma")

    def test_ancestry_vagaloide_magia_inicial(self):
        ancestry = tables.ANCESTRIES[3]
        ancestry.apply(self.pc)
        self.assertEqual(self.pc.health_points, 16)
        self.assertEqual(self.pc.ancestry, "Vagalóide")
        self.assertEqual(len(self.pc.magics), 1)
        self.assertEqual(self.pc.get_magic(0)['uses'], 3)

if __name__ == "__main__":
    unittest.main()
