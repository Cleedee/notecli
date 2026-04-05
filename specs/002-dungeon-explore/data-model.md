# Data Model: Dungeon Exploration

**Purpose**: Define entities and data structures for dungeon exploration feature
**Created**: 2026-04-04

## Entity: DungeonType

Represents a type of dungeon with associated metadata.

**Fields**:
- `name` (str): Nome do tipo (ex: "Templo", "Masmorra")
- `entrance_description` (str): Texto descritivo da entrada (2-3 frases em português)

**Validation**:
- `name` must be non-empty
- `entrance_description` must be non-empty

**State**: Immutable after definition (static game content)

## Entity: Dungeon

Represents a generated dungeon instance.

**Fields**:
- `type` (DungeonType): Tipo sorteado da masmorra
- `name` (str): Nome composto gerado (ex: "O Palácio da Dor Nebulosa")
- `entrance_shown` (bool): Se a descrição de entrada já foi exibida
- `current_room` (int): Índice da sala atual (0 = entrada, ainda não explorada)
- `rooms_visited` (int): Contador de salas visitadas

**Validation**:
- `type` must be a valid DungeonType
- `current_room` >= 0
- `rooms_visited` >= 0

**State transitions**:
- `new` → `entrance_shown=True` (após exibir descrição)
- `current_room` increments when player moves to next room

## Entity: ExplorationSession

Represents an active exploration session linking a dungeon to a character.

**Fields**:
- `dungeon` (Dungeon): A masmorra sendo explorada
- `character_index` (int): Índice do personagem na lista de salvos (1-based)
- `started_at` (str): Timestamp de início (ISO 8601)
- `active` (bool): Se a sessão está ativa (True) ou foi encerrada

**Validation**:
- `character_index` >= 1
- `started_at` valid ISO format

**State transitions**:
- `active=True` → `active=False` (quando jogador sai ou personagem morre)

## Entity: DungeonNameTables

Tables for procedural dungeon name generation.

**Structure**:
```python
{
    "articles": List[str],        # ["O", "A", "As", "Os"]
    "substantives": List[str],    # ["Templo", "Masmorra", "Catacumba", ...]
    "modifiers": List[str],       # ["da Dor", "da Névoa", "Nebulosa", ...]
    "prepositions": List[str]     # ["de", "da", "do", "das", "dos"]
}
```

**Generation rule**:
```
name = f"{random.choice(articles)} {random.choice(substantives)} {random.choice(prepositions)} {random.choice(modifiers)}"
```

**Validation**:
- All lists must be non-empty
- Each item must be a non-empty string

## Relationships

```
ExplorationSession 1──1 Dungeon
                     ├──1 DungeonType
                     └──1 DungeonNameTables (static, shared)

PlayerCharacter (existing) ←── ExplorationSession (via character_index)
```

## Storage Format

### `~/.notecli/exploration.json`

```json
{
  "version": 1,
  "session": {
    "dungeon": {
      "type_name": "Templo",
      "name": "O Templo da Dor Nebulosa",
      "entrance_shown": true,
      "current_room": 0,
      "rooms_visited": 0
    },
    "character_index": 2,
    "started_at": "2026-04-04T15:30:00",
    "active": true
  }
}
```

## Validation Rules (from Requirements)

| Rule | Source | Enforcement |
|------|--------|-------------|
| Tipo sorteado entre 6 | FR-001 | `random.randint(1, 6)` → lookup em `DUNGEON_TYPES` (Palácio, Cripta, Tumba, Santuário, Templo, Calabouço) |
| Nome composto de 3+ tabelas | FR-002 | `generate_dungeon_name()` usa 4 listas |
| Descrição corresponde ao tipo | FR-003 | `DungeonType.entrance_description` é atrelado ao tipo |
| Validação de input do menu | FR-008 | Loop `while True` com `try/except ValueError` |
| Persistência de sessão | FR-009 | `save_exploration()` após cada ação |
