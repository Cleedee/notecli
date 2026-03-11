from dataclasses import dataclass

from notecli.entities import CharacterPlayer

@dataclass
class Ancestry:
    name: str
    health_point: int

    def apply(self, pc):
        ...


def apply_mendigo(pc: CharacterPlayer):
    pc.health_point += 4
