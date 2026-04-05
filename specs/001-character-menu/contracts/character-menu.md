# Contract: Character Menu CLI

## Command: `notecli character`

### Description
Opens an interactive character management menu with two options:
1. **personagens** — View list of saved characters
2. **novo personagem** — Create a new character with randomized ancestry and profession

### Usage

```
notecli character
```

No additional arguments or flags required for initial version.

### Menu Interaction Protocol

**Input**: User enters a number via stdin:
- `1` → View character list
- `2` → Create new character
- `0` or `q` → Exit
- Any other input → Error message to stderr, menu re-displayed

**Output** (stdout):
- Menu header with numbered options
- For option 1: numbered list of characters with name, ancestry, profession; or "no characters" message
- For option 2: character creation sequence showing rolled ancestry, profession, final HP, and starting weapon
- For detail view: full character sheet (HP, current HP, magics, torches, weapon, status)

### Error Output (stderr)

| Scenario | Message |
|----------|---------|
| Invalid menu option | "Opção inválida. Escolha 1, 2 ou 0/q para sair." |
| No characters saved | "Nenhum personagem encontrado. Crie um novo personagem." |
| Storage file corrupted | "Erro ao carregar personagens. O arquivo pode estar corrompido." |
| Character creation error | "Erro ao criar personagem: {reason}" |

### Exit Codes

| Code | Meaning |
|------|--------|
| 0 | Successful exit (menu closed normally) |
| 1 | Fatal error (storage corruption, import failure) |

### Contract Version: 1.0
