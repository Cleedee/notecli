# Research: Dungeon Pre-Generation and Door Mechanics

**Purpose**: Document design decisions for dungeon pre-generation and door mechanics
**Created**: 2026-04-05

## Decision 1: Full dungeon pre-generation vs incremental

**Context**: Previous feature generated segments on-demand when opening doors. Now the entire dungeon must exist before exploration.

**Decision**: Implement `generate_full_dungeon(graph)` that expands from the initial staircase segment using BFS until the Final Room is placed (level 3 or leaf node).

**Rationale**: Guarantees Final Room always exists. All doors can be opened. Easier persistence and debugging.

**Alternatives considered**:
- Incremental + Final Room scan — rejected: complexity, risk of dead-end dungeons
- Pre-defined dungeon layouts — rejected: loses procedural feel

## Decision 2: Door entity replaces connected_segments

**Context**: Segment currently has `connected_segments: list[(door_idx, target_id)]`.

**Decision**: `Door` dataclass with `index`, `state`, `target_segment_id`, `trap_result`. `Segment.doors: list[Door]`.

**Rationale**: Encapsulates state + destination. Compatible with JSON serialization.

**Alternatives considered**:
- Keep connected_segments + separate state dict — rejected: two sources of truth
- Door as nested dict — rejected: harder to type-check

## Decision 3: Door roll distribution

**Context**: d6 roll: 1 = Trap, 2-3 = Locked, 4-6 = Unlocked.

**Decision**: `roll_door()` function returns `DoorState`. Single roll per door — state persisted after first opening.

**Rationale**: Simple, deterministic, testable. Matches spec exactly.

## Decision 4: Trap tables structure

**Context**: 6 tables × 6 entries, one per dungeon type. Entries will be placeholders.

**Decision**: Define `TRAP_TABLES: dict[str, list[str]]` in `tables.py`. Keys = dungeon type names. Values = 6 placeholder strings.

**Rationale**: Structure ready for future feature without adding complexity now.
