# Contract: `notecli explore` Command

**Purpose**: Define the CLI interface contract for dungeon exploration
**Created**: 2026-04-04

## Command Schema

```
notecli explore [--resume]
```

### Subcommand: `explore`

Starts a new dungeon exploration session or resumes an active one.

**Arguments**:
- `--resume` (optional): Resumes an active exploration session if one exists. Without this flag, always starts a new session (prompting to discard existing one if present).

**Exit Codes**:
- `0`: Exploration session started or resumed successfully
- `1`: Error (no characters available, storage corrupted, invalid state)

## Interaction Flow

### Flow 1: New Session (no existing characters)

```
$ notecli explore

🏰 Gerando masmorra...
  Tipo: Palácio
  Nome: O Palácio da Dor Nebulosa

📖 Você chega à entrada do Palácio da Dor Nebulosa.
   Portões de ferro retorcido marcam a entrada de uma residência real há muito abandonada.
   O vento uiva através de janelas vazias, carregando o cheiro de pedra úmida.

⚠️ Nenhum personagem encontrado. Criando novo personagem...

🎲 Rolando ancestralidade... 2d6 = 7 → Humano (20 HP)
🎲 Rolando profissão... 2d6 = 4 → Nobre (+2 HP, Espada curta)

⚔️ Novo personagem criado: Humano Nobre (HP: 22/22)

🗡️ Humano Nobre entra no Palácio da Dor Nebulosa...
   Tochas: 10 | Magias: 0 | HP: 22/22

Digite 'ajuda' para ver as ações disponíveis.
> _
```

### Flow 2: New Session (existing characters)

```
$ notecli explore

🏰 Gerando masmorra...
  Tipo: Cripta
  Nome: A Cripta dos Ossos Perdidos

📖 Você chega à entrada da Cripta dos Ossos Perdidos.
   Uma escadaria em espiral desce para a escuridão, com paredes cobertas de nichos vazios.
   O ar é gelado e um silêncio pesado preenche o corredor.

=== Escolha um Personagem ===
  1) Gnomo Coveiro — HP: 16/16 — vivo (Gnomo)
  2) Elfo Nobre — HP: 18/18 — vivo (Elfo)
  0) Criar novo personagem
  q) Sair

> 1

⚔️ Gnomo Coveiro entra na Cripta dos Ossos Perdidos...
   Tochas: 8 | Magias: 2 (Light, Heal) | HP: 16/16

Digite 'ajuda' para ver as ações disponíveis.
> _
```

### Flow 3: Resume Session

```
$ notecli explore --resume

🔄 Sessão de exploração encontrada:
   Masmorra: A Masmorra do Medo Antigo
   Personagem: Humano Nobre (HP: 18/22)
   Salas visitadas: 3

Continuar desta sessão? (s/n) > s

🗡️ Humano Nobre continua explorando A Masmorra do Medo Antigo...
   Tochas: 7 | Magias: 1 (Heal) | HP: 18/22

Digite 'ajuda' para ver as ações disponíveis.
> _
```

### Flow 4: Invalid Input

```
> 5
⚠️ Opção inválida. Escolha um número da lista ou 0 para criar novo personagem.

> abc
⚠️ Opção inválida. Digite um número.

> -1
⚠️ Opção inválida. Digite um número.
```

## Output Format

All output is written to **stdout** except errors, which go to **stderr**.

### Success Output Structure

```
[emoji] [action/message]
  [indented detail line]
  [indented detail line]
```

### Error Output Structure (stderr)

```
⚠️ [error message in Portuguese]
```

## Input Validation

| Input | Valid Values | Error Message |
|-------|-------------|---------------|
| Character choice | Integer 1-N, 0, q | "Opção inválida. Escolha um número da lista ou 0 para criar novo personagem." |
| Resume prompt | s, n | "Opção inválida. Digite 's' ou 'n'." |
| General command | Valid action keyword | "Comando desconhecido. Digite 'ajuda' para ver as ações disponíveis." |

## Data Contracts

### Dungeon Type (static)

```python
class DungeonType:
    name: str                    # Ex: "Templo"
    entrance_description: str    # Ex: "Colunas antigas sustentam..."
```

### Dungeon (runtime)

```python
class Dungeon:
    type: DungeonType
    name: str
    entrance_shown: bool
    current_room: int
    rooms_visited: int
```

### Exploration Session (persisted)

```json
{
  "version": 1,
  "session": {
    "dungeon": {
      "type_name": "str",
      "name": "str",
      "entrance_shown": true,
      "current_room": 0,
      "rooms_visited": 0
    },
    "character_index": 2,
    "started_at": "ISO 8601",
    "active": true
  }
}
```
