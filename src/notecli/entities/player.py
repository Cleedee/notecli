from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class PlayerCharacter:
    """Representa o herói controlado pelo jogador."""
    name: str
    occupation: str
    torches: int # número de tochas. Máximo 10.
    magics: List[dict] = field(default_factory=list)
    light_on: bool = field(default=False)
    health_points: int = field(default=0)
    hp_current: int = field(default=0)
    ancestry: Optional[str] = ''

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
