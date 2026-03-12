import unittest

from notecli.entities import PlayerCharacter
from notecli.entities.magic import factory_magic
from notecli import tables

class TestUseMagic(unittest.TestCase):

    def setUp(self):
        self.pc = PlayerCharacter(
            name="Kharshak",
            torches=10,
            occupation="Blacksmith"
        )
        ancestry = tables.ANCESTRIES[3] # Vagalóide
        ancestry.apply(self.pc)

    def test_use_light(self):
        self.assertEqual(len(self.pc.magics), 1)
        self.assertEqual(self.pc.light_on, False)
        self.pc.use_magic(0)
        self.assertEqual(self.pc.light_on, True)
        self.assertEqual(self.pc.get_magic(0)["uses"], 2)

    def test_use_much_light(self):
        self.pc.use_magic(0)
        self.pc.use_magic(0)
        self.pc.use_magic(0)
        self.pc.use_magic(0)
        self.assertEqual(self.pc.get_magic(0)["uses"], 0)

    def test_light_on(self):
        self.assertEqual(self.pc.light_on, False)

    def test_factory_magic(self):
        magic = factory_magic('Light')
        self.assertEqual(magic['name'], 'Light')

    def test_use_torch(self):
        self.assertEqual(self.pc.torches, 10)
        self.pc.consume_torch()
        self.assertEqual(self.pc.torches, 9)
        self.assertEqual(self.pc.light_on, True)


if __name__ == "__main__":
    unittest.main()
