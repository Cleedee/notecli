# Data Model: Dungeon Map Display

**Purpose**: Document data flow for map display
**Created**: 2026-04-05

## Data Flow

```
ExplorationSession (from exploration.json)
  └── segment_graph: DungeonGraph
        ├── segments: dict[int, Segment]
        │     ├── type: SegmentType
        │     ├── level: int
        │     ├── doors: list[Door]
        │     │     ├── state: DoorState
        │     │     └── target_segment_id: int
        │     └── is_final_room: bool
        └── current_segment_id: int
```

## Output Format

Hierarchical list with legend. No new entities.
