from dataclasses import dataclass
from typing import Callable

from notecli.entities.player import PlayerCharacter
from notecli.entities.magic import factory_magic, BASIC_MAGICS
from notecli.dice import Roller

@dataclass
class Ancestry:
    name: str
    health_points: int
    applier: Callable
    hp_current: int = 0

    def apply(self, pc: PlayerCharacter):
        pc.health_points = self.health_points
        pc.hp_current = self.health_points
        pc.ancestry = self.name
        self.applier(pc)

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

def apply_vagaloide(pc: PlayerCharacter):
    magic = factory_magic('Light')
    magic['uses'] = 3
    pc.magics.append(magic)

def apply_faerie(pc: PlayerCharacter):
    _randomize_magics(pc, 5)

def apply_elf(pc: PlayerCharacter):
    magic : dict = BASIC_MAGICS.get(Roller.d6(), {})
    magic['uses'] = 1
    pc.magics.append(magic)

def apply_gnome(pc: PlayerCharacter):
    _randomize_magics(pc, 3)

def apply_halfdragon(pc: PlayerCharacter):
    magic = factory_magic('Fireball')
    magic['uses'] = 3
    pc.magics.append(magic)

SLIMEMAN = Ancestry("Homem-Gosma", 10, apply_generic)
VAGALOIDE = Ancestry("Vagalóide", 16, apply_vagaloide)
FAERIE = Ancestry("Fada", 8, apply_faerie)
GNOME = Ancestry("Gnomo", 14, apply_gnome)
ELF = Ancestry("Elfo", 16, apply_elf)
HUMAN = Ancestry("Humano", 20, apply_generic)
DWARF = Ancestry("Anão", 18, apply_generic)
HALFLING = Ancestry("Pequenino", 14, apply_generic)
CAT_PEOPLE = Ancestry("Povo Gato", 19, apply_generic)
RINOCEROID = Ancestry("Rinoceróide", 24, apply_generic)
HALF_DRAGON = Ancestry("Meio-Dragão", 30, apply_halfdragon)
