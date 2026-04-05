import random
import re

class Roller:

    @staticmethod
    def roll(notation: str) -> int:
        """
        Resolve uma string de dados (ex: '1d6', '2d10+2').
        Retorna o resultado total da rolagem.
        """
        # Regex para capturar: [quantidade]d[lados][+ou-][bônus]
        match = re.match(r"(\d+)d(\d+)(?:([+-])(\d+))?", notation.lower())
        if not match:
            raise ValueError(f"Formato de dado inválido: {notation}")

        quantity = int(match.group(1))
        sides = int(match.group(2))
        operator = match.group(3)
        bonus = int(match.group(4)) if match.group(4) else 0

        # Realiza a soma das rolagens individuais
        total = sum(random.randint(1, sides) for _ in range(quantity))

        # Aplica o modificador, se existir
        if operator == "+":
            total += bonus
        elif operator == "-":
            total -= bonus

        return max(1, total)  # Garante que o resultado nunca seja menor que 1

    @staticmethod
    def d6() -> int:
        """Atalho para a rolagem mais comum do NoteQuest."""
        return random.randint(1, 6)

    @staticmethod
    def roll_2d6() -> int:
        """Rolagem 2d6 para ancestralidade e profissão (resultado 2-12)."""
        return Roller.roll("2d6")
