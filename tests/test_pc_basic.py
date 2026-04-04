import unittest

from notecli.entities import PlayerCharacter
from notecli import tables


class TestBasic(unittest.TestCase):

    def setUp(self):
        self.pc = PlayerCharacter(
            name="Jackie",
            torches=10,
            occupation="Vagabond"
        )

    def test_human(self):
        ancestry = tables.ANCESTRIES[7] # Human
        ancestry.apply(self.pc)
        self.assertEqual(self.pc.hp_current, 20, "Essa deve ser os pontos de vida inicial")
        
    def test_gnome(self):
        ancestry = tables.ANCESTRIES[5] # Gnome
        ancestry.apply(self.pc)
        uses = 0
        for magic in self.pc.magics:
            uses += magic['uses']
        self.assertEqual(uses, 3, "Deve ter três usos")
        self.assertEqual(self.pc.hp_current, 14, "Essa deve ser os pontos de vida inicial")
        self.assertEqual(self.pc.ancestry, 'Gnomo')
        
    def test_dwarf(self):
        ancestry = tables.ANCESTRIES[8] # Dwarf
        ancestry.apply(self.pc)


if __name__ == '__main__':
    unittest.main()

