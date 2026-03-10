import unittest

from notecli.entities import PlayerCharacter

class TestCreatePC(unittest.TestCase):

    def test_create(self):
        pc = PlayerCharacter(
            health_points = 10,
            torches=3,
            ancestry="Dwarf",
            occupation="Blacksmith"
        )
        self.assertEqual(pc.health_points, 10)

if __name__ == "__main__":
    unittest.main()
