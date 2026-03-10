from dataclasses import dataclass

@dataclass
class PlayerCharacter:
    """Representa o herói controlado pelo jogador."""
    health_points: int
    torches: int # número de tochas. Máximo 10.
    ancestry: str
    occupation: str

    def is_alive(self):
        return self.health_points > 0

    def consume_torch(self):
        if self.torches > 0:
            self.torches -= 1
            print("🔥 Você acende uma tocha. A escuridão recua.")
        else:
            print("🌑 Suas tochas acabaram! Você está no escuro...")
