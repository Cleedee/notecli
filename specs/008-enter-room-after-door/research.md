# Research: Enter Room After Opening Door

**Purpose**: Document design decisions for enter-room-after-door feature
**Created**: 2026-04-05

## Decision 1: Door model with 3 independent attributes

**Context**: Door state was a single enum. Now needs visibility (Fechada/Aberta), lock (Trancada/Destrancada), trap (Sim/Não).

**Decision**: Door gets `is_open: bool`, `is_locked: bool`, `has_trap: bool`. Display combines these into readable status.

**Rationale**: Clear, explicit, easy to serialize.

**Alternatives considered**:
- Composite enum with 8 values — rejected: hard to reason about, inflexible
- Bitfield — rejected: less readable, harder to debug

## Decision 2: Close doors after action

**Context**: After entering or choosing another action, all opened doors close.

**Decision**: `close_opened_doors(segment)` function — iterates doors, sets `is_open = False` for doors that were open. Keeps `is_locked` and `has_trap` unchanged.

**Rationale**: Simple, one function call. Preserves lock/trap state.

## Decision 3: Already-revealed door allows entry without re-roll

**Context**: Player knows where door leads after first opening.

**Decision**: If door has `target_segment_id` set and `is_locked = False` and `has_trap = False`, offer "entrar" directly. No re-roll.

**Rationale**: Respects player knowledge. No redundant randomness.
