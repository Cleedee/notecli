import unittest
from unittest.mock import patch

from notecli.entities import PlayerCharacter
from notecli import tables

class TestElf(unittest.TestCase):

    def setUp(self):
        self.pc = PlayerCharacter(
            name="Naliash",
            torches=10,
            occupation="Noble"
        )

    def test_use_heal(self):
        with patch('notecli.dice.Roller.d6') as mock_d6:
            mock_d6.return_value = 1
            ancestry = tables.ANCESTRIES[6] # Elf
            ancestry.apply(self.pc)
            self.pc.use_magic(0)
            mock_d6.assert_called_once()
            self.assertEqual(self.pc.ancestry, "Elfo")
            self.assertEqual(self.pc.health_points, 16, "Está no máximo de seus pontos de vida")

if __name__ == '__main__':
    unittest.main()
