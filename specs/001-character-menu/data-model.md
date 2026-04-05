# Data Model: Character Menu

## Character Record

**Purpose**: Persistent representation of a player character for storage and retrieval.

**Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Player-chosen or auto-generated name |
| `ancestry` | string | Ancestry name (e.g., "Homem-Gosma", "Meio-Dragão") |
| `occupation` | string | Profession name (e.g., "Ferreiro", "Nobre") |
| `health_points` | int | Maximum HP (ancestry base + occupation bonus) |
| `hp_current` | int | Current HP (starts equal to health_points) |
| `torches` | int | Number of torches (max 10) |
| `light_on` | bool | Whether torch light is currently active |
| `magics` | list | Magic spells owned by the character |
| `starting_weapon` | string | Weapon from profession |
| `alive` | bool | Whether character is alive |

**Validation rules**:
- `torches` MUST be between 0 and 10
- `hp_current` MUST be >= 0 and <= `health_points`
- `health_points` MUST be > 0
- `ancestry` MUST match a known entry in `ANCESTRIES` (keys 2-12)
- `occupation` MUST match a known entry in `OCCUPATIONS` (keys 2-12)

**State transitions**:
- New character: `alive=true`, `hp_current=health_points`, `light_on=false`, `torches=10` (full starting supply)
- Death: `alive=true` → `alive=false` (future combat feature)

### Magic Entry (nested in Character Record)

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Magic name (e.g., "Light", "Heal", "Freeze") |
| `uses` | int | Remaining uses of this magic |

**Note**: The `applier` callable is NOT serialized. It is reconstructed on load via `factory_magic(name)`.

## Storage Format (JSON)

```json
{
  "version": 1,
  "characters": [
    {
      "name": "Jackie",
      "ancestry": "Humano",
      "occupation": "Mendigo",
      "health_points": 24,
      "hp_current": 24,
      "torches": 10,
      "light_on": false,
      "starting_weapon": "pedaço de pau",
      "alive": true,
      "magics": [
        { "name": "Light", "uses": 3 }
      ]
    }
  ]
}
```

## Ancestry Table (2d6 → Ancestry)

| 2d6 Roll | Ancestry | HP | Special |
|----------|----------|----|--------|
| 2 | Homem-Gosma | 10 | — |
| 3 | Vagalóide | 16 | Light magic (3 uses) |
| 4 | Fada | 8 | 5 random magics |
| 5 | Gnomo | 14 | 3 random magics |
| 6 | Elfo | 16 | 1 random magic |
| 7 | Humano | 20 | — |
| 8 | Anão | 18 | — |
| 9 | Pequenino | 14 | — |
| 10 | Povo Gato | 19 | — |
| 11 | Rinoceróide | 24 | — |
| 12 | Meio-Dragão | 30 | Fireball magic (3 uses) |

## Profession Table (2d6 → Occupation)

| 2d6 Roll | Occupation | HP Bonus | Starting Weapon |
|----------|-----------|----------|----------------|
| 2 | Mendigo | +4 | pedaço de pau |
| 3 | Coveiro | +2 | pá |
| 4 | Nobre | +0 | rapieira |
| 5 | Estudante | +0 | adaga |
| 6 | Ferreiro | +4 | martelo |
| 7 | Guarda | +4 | espada curta |
| 8 | Cozinheiro | +2 | cutelo |
| 9 | Chaveiro | +2 | adaga |
| 10 | Lenhador | +4 | machado |
| 11 | Lenhador | +4 | machado |
| 12 | Gladiador | +6 | espada curta |

**Character Creation Flow**:
1. Roll 2d6 → look up `ANCESTRIES` → get `Ancestry`
2. Roll 2d6 → look up `OCCUPATIONS` → get `Occupation`
3. Apply ancestry to PlayerCharacter (sets base HP + ancestry-specific magics)
4. Apply occupation bonuses (`additional_hit_points` added to HP, set `starting_weapon`)
5. Assign default starting torches (10)
6. Save to storage

## Relationships

```
Character Record ──┬── Ancestry (2d6 lookup, sets base HP + ancestry-specific magics)
                   ├── Occupation (2d6 lookup, adds profession-specific HP bonus + starting weapon)
                   └── Magic[] (list of magic entries with name + uses)
```
