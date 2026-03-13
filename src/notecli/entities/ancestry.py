from dataclasses import dataclass
from typing import Callable

from notecli.entities.magic import factory_magic, BASIC_MAGICS
from notecli.dice import Roller

@dataclass
class Ancestry:
    name: str
    health_points: int
    applier: Callable

    def apply(self, pc):
        pc.health_points = self.health_points
        pc.ancestry = self.name
        self.applier(pc)


def apply_generic(pc):
    pass

def apply_vagaloide(pc):
    magic = factory_magic('Light')
    magic['uses'] = 3
    pc.magics.append(magic)

def apply_elf(pc):
    magic = BASIC_MAGICS.get(Roller.d6())
    magic['uses'] = 1
    pc.magics.append(magic)

SLIMEMAN = Ancestry("Homem-Gosma", 10, apply_generic)
VAGALOIDE = Ancestry("Vagalóide", 16, apply_vagaloide)
ELF = Ancestry("Elfo", 16, apply_elf)
