# Quickstart: Character Menu

## Prerequisites

- Python 3.14+
- `uv` package manager
- Project dependencies installed (`uv sync`)

## Running

```bash
# Launch the character menu
uv run notecli character
```

## First Run

1. The menu displays two options:
   - **1) personagens** — Lists saved characters (empty on first run)
   - **2) novo personagem** — Creates a new character

2. Select **2** to create a character:
   - Ancestry is rolled (2d6) — e.g., "Humano" (20 HP)
   - Profession is rolled (2d6) — e.g., "Ferreiro" (+4 HP, martelo)
   - Character is saved with 10 torches, starting weapon, and any ancestry magics

3. Select **1** to view your characters:
   - Each character shows name, ancestry, profession, HP, and status
   - Select a character by number to see full details (magics, torches, weapon)

4. Press **0** or **q** to exit

## Character Storage

Characters are saved to `~/.notecli/characters.json`. You can inspect this file directly:

```bash
cat ~/.notecli/characters.json
```

## Example Session

```
$ uv run notecli character

=== Menu de Personagens ===
1) personagens
2) novo personagem
0) sair

> 2

🎲 Rolando ancestralidade... 2d6 = 7 → Humano (20 HP)
🎲 Rolando profissão... 2d6 = 6 → Ferreiro (+4 HP, martelo)

⚔️ Novo personagem criado!
  Nome: (auto)
  Ancestralidade: Humano
  Profissão: Ferreiro
  HP: 24
  Arma inicial: martelo
  Tochas: 10

Criar outro personagem? (s/n) > n

=== Menu de Personagens ===
1) personagens
2) novo personagem
0) sair

> 1

=== Personagens Salvos ===
1) Humano Ferreiro — HP: 24/24 — 🔥 vivo

> 0
Saindo...
```

## Testing

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run python -m unittest tests/test_character_menu.py
```
