# Data Model: Dungeon Pre-Generation and Door Mechanics

**Purpose**: Define entities for door mechanics and pre-generated dungeons
**Created**: 2026-04-05

## Entity: DoorState

Enum representing door states.

**Values**:
- `FECHADA` — Door not yet opened
- `ARMADILHA` — Roll = 1, trap triggered
- `TRANCADA` — Roll = 2-3, needs torch to unlock
- `DESTRANCADA` — Roll = 4-6, segment revealed

## Entity: Door

Represents a door between segments.

**Fields**:
- `index` (int): Door index in segment (0-based)
- `state` (DoorState): Current state
- `target_segment_id` (int | None): Target segment ID (set when generated)
- `trap_result` (str | None): Trap result string (placeholder for now)

**Validation**:
- `index` >= 0
- `target_segment_id` set when door is first generated
- `trap_result` set only when state = ARMADILHA

## Entity: Segment (modified)

**Fields removed**: `connected_segments`

**Fields added**: `doors: list[Door]`

**Behavior**:
- On creation: initialized with `doors_count` doors in FECHADA state
- Each door has a `target_segment_id` assigned during pre-generation

## Entity: DungeonGraph (modified)

**New method**: `generate_full_dungeon()` — generates all segments until Final Room is placed.

**Algorithm**:
1. Start with initial staircase (level 1, 1 door)
2. Use BFS/iterative expansion: for each segment, roll transition table to determine connected segments
3. Continue until:
   - Level 3 reached → place Final Room as destination
   - No more staircase results and all leaf segments are dead-ends → mark last segment as Final Room
4. Assign door states: all doors start as FECHADA

## Storage Format

### Door in exploration.json

```json
{
  "doors": [
    {
      "index": 0,
      "state": "fechada",
      "target_segment_id": 1,
      "trap_result": null
    }
  ]
}
```

## Trap Tables

```python
TRAP_TABLES = {
    "Palácio": ["placeholder_1", "placeholder_2", ...],  # 6 entries
    "Cripta": [...],
    "Tumba": [...],
    "Santuário": [...],
    "Templo": [...],
    "Calabouço": [...],
}
```
