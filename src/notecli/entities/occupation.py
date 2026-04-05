from dataclasses import dataclass
from typing import Callable

from notecli.entities.player import PlayerCharacter

@dataclass
class Occupation:
    name: str
    additional_hit_points: int
    starting_weapon: str
    advantage_applier: Callable

def apply_generic(pc: PlayerCharacter):
    pass

BEGGAR = Occupation("Mendigo", 4, "pedaço de pau", apply_generic)
GRAVEDIGGER = Occupation("Coveiro", 2, "pá", apply_generic)
NOBLE = Occupation("Nobre", 0, "rapieira", apply_generic)
STUDENT = Occupation("Estudante", 0, "adaga", apply_generic)
BLACKSMITH = Occupation("Ferreiro", 4, "martelo", apply_generic)
GUARD = Occupation("Guarda", 4, "espada curta", apply_generic)
CHEF = Occupation("Cozinheiro", 2, "cutelo", apply_generic)
LOCKSMITH = Occupation("Chaveiro", 2, "adaga", apply_generic)
LUMBERJACK = Occupation("Lenhador", 4, "machado", apply_generic)
MINER = Occupation("Minerador", 4, "picareta", apply_generic)
GLADIATOR = Occupation("Gladiador", 6, "espada curta", apply_generic)
