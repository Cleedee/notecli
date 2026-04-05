# Research: Torch Consumption

**Purpose**: Document design decisions for torch consumption feature
**Created**: 2026-04-04

## Decision 1: Reuse `PlayerCharacter.consume_torch()`

**Context**: The feature needs to consume 1 torch, activate light, and show a message when exploration starts.

**Decision**: Call the existing `PlayerCharacter.consume_torch()` method directly from `explore_menu.py` after character selection/creation and before saving the session.

**Rationale**:
- `consume_torch()` already implements: decrement torches by 1, set `light_on = True`, print success/warning message
- Zero code duplication (YAGNI)
- Existing tests for `consume_torch()` cover the base behavior

**Alternatives considered**:
- Create a dedicated function in `explore_menu` — rejected: duplicates logic already in `consume_torch()`
- Wrap in a new service layer — rejected: overkill for a single method call
