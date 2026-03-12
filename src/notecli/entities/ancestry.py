from dataclasses import dataclass
from typing import Callable

from notecli.entities import factory_magic

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
    print(magic)
    magic['uses'] = 3
    pc.magics.append(magic)


MENDIGO = Ancestry("Mendigo", 10, apply_generic)
VAGALOIDE = Ancestry("Vagalóide", 16, apply_vagaloide)
