# Data Model: Dungeon Segment Generation

**Purpose**: Define entities and data structures for dungeon segment generation
**Created**: 2026-04-05

## Entity: SegmentType

Enum representing the type of a dungeon segment.

**Values**:
- `ESCADARIA` — Staircase leading down to next level
- `CORREDOR` — Corridor with 1-3 doors
- `SALA` — Room with 0-2 doors (or staircase as special result)
- `SALA_FINAL` — Final Room (goal of exploration)

**Validation**: Must be one of the 4 enum values.

## Entity: Segment

Represents a single segment of the dungeon.

**Fields**:
- `id` (int): Unique auto-incremented identifier
- `type` (SegmentType): Type of this segment
- `level` (int): Dungeon level this segment belongs to (1-based)
- `doors_count` (int): Number of doors in this segment (0-3)
- `connected_segments` (list of tuples): `[(door_index, target_segment_id), ...]` — maps each door to a connected segment
- `is_final_room` (bool): True if this is the Final Room
- `has_monsters` (bool): True if this segment has monsters (for exit path checking)

**Validation**:
- `id` >= 0
- `level` >= 1
- `doors_count` >= 0
- `connected_segments` length <= `doors_count`

**State transitions**:
- `doors_count` set at generation time (immutable after)
- `connected_segments` populated when doors are first opened
- `is_final_room` set once when Final Room condition is met

## Entity: Dungeon (extended)

Represents the full dungeon with its segment graph.

**Fields** (new):
- `segments` (dict[int, Segment]): Map of segment_id → Segment
- `current_segment_id` (int): ID of the segment the player is currently in
- `max_level` (int): Highest level reached so far
- `visited_stack` (list[int]): Stack of segment IDs for backtracking
- `next_segment_id` (int): Auto-increment counter for new segment IDs

**Validation**:
- `current_segment_id` must exist in `segments`
- `visited_stack` must not be empty (at least entrance segment)
- `max_level` >= 1

**State transitions**:
- `segments` grows as new segments are generated
- `current_segment_id` changes when player moves or backtracks
- `visited_stack` pushes on advance, pops on backtrack
- `max_level` increases when staircase to new level is generated

## Entity: TransitionTable

Maps a segment type to possible next segments.

**Structure**:
```python
STAIRCASE_TRANSITIONS = [
    {"type": "corredor", "doors": 1},
    {"type": "corredor", "doors": 2},
    {"type": "corredor", "doors": 3},
    {"type": "corredor", "doors": 1},
    {"type": "corredor", "doors": 2},
    {"type": "corredor", "doors": 3},
]

CORRIDOR_TRANSITIONS = [
    {"type": "sala", "doors": 1},
    {"type": "sala", "doors": 2},
    {"type": "sala", "doors": 1},
    {"type": "sala", "doors": 2},
    {"type": "sala", "doors": 1},
    {"type": "escadaria", "doors": 1},  # one result leads to staircase
]

ROOM_TRANSITIONS = [
    {"type": "sala", "doors": 0},
    {"type": "sala", "doors": 0},
    {"type": "sala", "doors": 0},
    {"type": "sala", "doors": 0},
    {"type": "sala", "doors": 0},
    {"type": "escadaria", "doors": 1},  # one result leads to staircase
]
```

**Selection**: `random.choice(table)` or `table[Roller.d6() - 1]`

## Relationships

```
Dungeon 1──* Segment (via segments dict)
            ├──* Segment (via connected_segments — graph edges)
            └── TransitionTable (static, 3 tables for 3 types)

Segment ──→ SegmentType (enum)
```

## Storage Format

### `~/.notecli/exploration.json` (extended)

```json
{
  "version": 2,
  "session": {
    "dungeon": {
      "type_name": "Templo",
      "name": "O Templo da Dor",
      "segments": {
        "0": {
          "id": 0,
          "type": "escadaria",
          "level": 1,
          "doors_count": 1,
          "connected_segments": [[0, 1]],
          "is_final_room": false,
          "has_monsters": false
        },
        "1": {
          "id": 1,
          "type": "corredor",
          "level": 1,
          "doors_count": 2,
          "connected_segments": [],
          "is_final_room": false,
          "has_monsters": false
        }
      },
      "current_segment_id": 1,
      "max_level": 1,
      "visited_stack": [0, 1],
      "next_segment_id": 2
    },
    "character_index": 1,
    "started_at": "2026-04-05T10:00:00",
    "active": true
  }
}
```

## Generation Rules (from Requirements)

| Rule | Source | Enforcement |
|------|--------|-------------|
| First segment = escadaria nível 1, 1 porta | FR-002 | `generate_initial_segment()` cria fixo |
| 3 tabelas × 6 opções | FR-003, FR-004 | `STAIRCASE_TRANSITIONS`, `CORRIDOR_TRANSITIONS`, `ROOM_TRANSITIONS` |
| Escadaria → corredor 1-3 portas | FR-005 | `STAIRCASE_TRANSITIONS` só contém corredor |
| Corredor → sala 1-2 portas ou escadaria 1 porta | FR-006 | 5 salas + 1 escadaria na tabela |
| Sala → sala 0 portas ou escadaria 1 porta | FR-007 | 5 salas 0 portas + 1 escadaria |
| Não regenerar segmentos | FR-008 | Verificar `target_segment_id` existente antes de criar |
| Escadaria aumenta nível | FR-010 | `level = previous_level + 1` ao gerar escadaria |
| Nível 3 → Sala Final | FR-011 | Verificar `max_level >= 3` → `SALA_FINAL` |
| Último segmento sem saída → Sala Final | FR-012 | Verificar grafos leaf nodes |
