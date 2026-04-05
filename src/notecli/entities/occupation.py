from dataclasses import dataclass
from typing import Callable

from notecli.dice import Roller
from notecli.entities.player import PlayerCharacter
from notecli.entities.magic import BASIC_MAGICS

@dataclass
class Occupation:
    name: str
    additional_hit_points: int
    starting_weapon: str
    advantage_applier: Callable

def _randomize_magics(pc: PlayerCharacter, quantity):
    for _ in range(quantity):
        magic = BASIC_MAGICS.get(Roller.d6(), {})
        print(magic['name'])
        query_magic = pc.has_magic(magic['name'])
        if query_magic:
            query_magic['uses'] += 1
        else:
            pc.magics.append(magic)

def apply_generic(pc: PlayerCharacter):
    pass

def apply_noble(pc: PlayerCharacter):
    _randomize_magics(pc, 1)

def apply_student(pc: PlayerCharacter):
    _randomize_magics(pc, 3)

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
