import unittest

from notecli.entities import PlayerCharacter
from notecli import tables


class TestFaerie(unittest.TestCase):

    def setUp(self):
        self.pc = PlayerCharacter(
            name="Alfilin",
            torches=10,
            occupation="Noble"
        )

    def test_five_magic_uses(self):
        ancestry = tables.ANCESTRIES[4] # Faerie
        ancestry.apply(self.pc)
        uses = 0
        for magic in self.pc.magics:
            uses += magic['uses']
        self.assertEqual(uses, 5, "Deve ter cinco usos")
        
if __name__ == '__main__':
    unittest.main()

