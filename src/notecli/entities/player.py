from dataclasses import dataclass, field
from typing import Optional, List

from notecli.entities.magic import factory_magic


@dataclass
class PlayerCharacter:
    """Representa o herói controlado pelo jogador."""
    name: str
    occupation: str
    torches: int  # número de tochas. Máximo 10.
    magics: List[dict] = field(default_factory=list)
    light_on: bool = field(default=False)
    health_points: int = field(default=0)
    hp_current: int = field(default=0)
    ancestry: Optional[str] = ''
    starting_weapon: str = ''
    alive: bool = True

    def is_alive(self):
        return self.hp_current > 0

    def consume_torch(self):
        if self.torches > 0:
            self.torches -= 1
            self.light_on = True
            print("🔥 Você acende uma tocha. A escuridão recua.")
        else:
            print("🌑 Suas tochas acabaram! Você está no escuro...")

    def get_magic(self, position):
        return self.magics[position]

    def use_magic(self, position):
        magic = self.magics[position]
        print(magic)
        print(f"{self.name} usa {magic['name']}.")
        uses = magic['uses']
        if uses >= 1:
            uses -= 1
            magic['applier'](self)
            self.magics[position]['uses'] = uses
        else:
            print(f"{self.name} não tem mais usos de {magic['name']}.")

    def has_magic(self, name):
        for magic in self.magics:
            if name in magic['name']:
                return magic
        return None

    def to_dict(self) -> dict:
        """Serialize to a JSON-compatible dictionary."""
        return {
            "name": self.name,
            "ancestry": self.ancestry,
            "occupation": self.occupation,
            "health_points": self.health_points,
            "hp_current": self.hp_current,
            "torches": self.torches,
            "light_on": self.light_on,
            "starting_weapon": self.starting_weapon,
            "alive": self.alive,
            "magics": [
                {"name": m["name"], "uses": m["uses"]}
                for m in self.magics
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PlayerCharacter":
        """Reconstruct a PlayerCharacter from a stored dictionary."""
        pc = cls(
            name=data["name"],
            occupation=data["occupation"],
            torches=data["torches"],
            light_on=data.get("light_on", False),
            health_points=data["health_points"],
            hp_current=data["hp_current"],
            ancestry=data.get("ancestry", ""),
            starting_weapon=data.get("starting_weapon", ""),
            alive=data.get("alive", True),
        )
        # Reconstruct magic callables from stored name + uses
        for m in data.get("magics", []):
            magic = factory_magic(m["name"])
            if magic:
                magic["uses"] = m["uses"]
                pc.magics.append(magic)
        return pc
