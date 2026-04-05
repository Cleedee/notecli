# Research: Dungeon Segment Generation

**Purpose**: Document design decisions for dungeon segment generation feature
**Created**: 2026-04-05

## Decision 1: Graph representation for segments

**Context**: Segments are connected by doors. We need to track which doors are opened and which segments exist.

**Decision**: Use a dict `{segment_id: Segment}` where each `Segment` has a list `connected_segments` of `(door_index, target_segment_id)` tuples. IDs are auto-incremented ints.

**Rationale**:
- Simple, O(1) lookup
- Easily serializable to JSON
- No external dependencies

**Alternatives considered**:
- Nested object graph — harder to serialize/persist
- External graph library — YAGNI, adds dependency
- Flat list with index references — less readable

## Decision 2: Transition table structure

**Context**: 3 tables with 6 options each, with specific distributions.

**Decision**: Define as lists of dicts in `tables.py`:
```python
STAIRCASE_TRANSITIONS = [
    {"type": "corredor", "doors": 1},
    {"type": "corredor", "doors": 2},
    ...
]
```
Selection via `random.choice(table)` or `Roller.d6() - 1`.

**Rationale**: Consistent with `DUNGEON_TYPES` pattern. Easy to tweak.

**Alternatives considered**:
- Enum + separate door count table — two lookups, more complex
- Weighted random — overkill for fixed 6 options

## Decision 3: Backtracking mechanism

**Context**: Player needs to go back through visited segments.

**Decision**: Stack (list) of `visited_segment_ids`. Push when advancing, pop when going back. Last item = entrance segment.

**Rationale**: Stack is the natural structure for "backtrack through path". Simple and efficient.

**Alternatives considered**:
- Full graph traversal — complex, unnecessary
- Parent pointer in each segment — works but less flexible for branching paths

## Decision 4: Final Room detection

**Context**: Final Room appears at level 3 OR as last segment if not enough staircases.

**Decision**: Check `current_level >= 3` when generating staircase destination → generate `SegmentType.SALA_FINAL`. For fallback: when no more connected segments exist and level < 3, mark last reached segment as Final Room.

**Rationale**: Simple logic at generation point. No extra state.

**Alternatives considered**:
- Pre-generate entire dungeon — loses procedural feel, wastes memory
- Counter-based — same result, less explicit

## Decision 5: Monster tracking (boolean flag)

**Context**: FR-014/FR-015 require knowing if path to entrance has monsters.

**Decision**: Each `Segment` has a `has_monsters: bool` flag. For this feature, it's set randomly or defaulted to False. Actual monster generation is a future feature.

**Rationale**: Minimal scaffolding. Enables exit path checking without full monster system.

**Alternatives considered**:
- Full monster entities now — out of scope for this feature
- No tracking — can't implement "exit if path clear" feature
