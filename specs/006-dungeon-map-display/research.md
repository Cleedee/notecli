# Research: Dungeon Map Display

**Purpose**: Document design decisions for dungeon map display feature
**Created**: 2026-04-05

## Decision 1: Map text format

**Context**: Must be readable in 80 columns, show segments, doors, and states.

**Decision**: Hierarchical indented list with visual tree structure using box-drawing characters.

**Rationale**: Simple, hierarchical, fits in 80 columns.

**Alternatives considered**:
- ASCII art grid — rejected: complex for non-planar graphs
- Graphviz — rejected: external dependency
- JSON dump — rejected: not user-readable

## Decision 2: Session reading

**Context**: Data already persisted in `exploration.json`.

**Decision**: Use existing `load_exploration()`. If None or inactive, show "Nenhuma masmorra explorada."

**Rationale**: Reuses existing infrastructure. Simple.
