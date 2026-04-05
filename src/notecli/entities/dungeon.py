"""Dungeon entities for exploration sessions."""

from dataclasses import dataclass, field
from typing import Optional

from notecli.entities.dungeon_name import generate_dungeon_name
from notecli.entities.segment import Segment, SegmentType


@dataclass
class DungeonType:
    """Represents a type of dungeon with entrance description."""

    article: str
    name: str
    entrance_description: str


@dataclass
class Dungeon:
    """Represents a generated dungeon instance."""

    type: DungeonType
    name: str
    entrance_shown: bool = field(default=False)
    current_room: int = field(default=0)
    rooms_visited: int = field(default=0)


class DungeonGraph:
    """Manages the graph of dungeon segments.

    Tracks segments, current position, level, and backtrack stack.
    """

    def __init__(self):
        self.segments: dict[int, Segment] = {}
        self.current_segment_id: Optional[int] = None
        self.max_level: int = 0
        self.visited_stack: list[int] = []
        self._next_id: int = 0

    def _allocate_id(self) -> int:
        seg_id = self._next_id
        self._next_id += 1
        return seg_id

    def add_segment(self, segment: Segment) -> int:
        """Add a segment to the graph and return its ID."""
        if segment.id not in self.segments:
            self.segments[segment.id] = segment
            if segment.level > self.max_level:
                self.max_level = segment.level
        return segment.id

    def create_segment(
        self,
        seg_type: SegmentType,
        level: int,
        doors_count: int,
        is_final_room: bool = False,
        has_monsters: bool = False,
    ) -> Segment:
        """Create and add a new segment to the graph."""
        seg_id = self._allocate_id()
        segment = Segment(
            id=seg_id,
            type=seg_type,
            level=level,
            doors_count=doors_count,
            is_final_room=is_final_room,
            has_monsters=has_monsters,
        )
        self.segments[seg_id] = segment
        if level > self.max_level:
            self.max_level = level
        return segment

    def set_current(self, segment_id: int) -> None:
        """Set the current segment and push to visited stack."""
        self.current_segment_id = segment_id
        if segment_id not in self.visited_stack or self.visited_stack[-1] != segment_id:
            self.visited_stack.append(segment_id)

    def current_segment(self) -> Optional[Segment]:
        """Get the current segment, or None."""
        if self.current_segment_id is None:
            return None
        return self.segments.get(self.current_segment_id)

    def backtrack(self) -> Optional[Segment]:
        """Go back to the previous segment. Returns new segment or None."""
        if len(self.visited_stack) <= 1:
            return None
        self.visited_stack.pop()
        self.current_segment_id = self.visited_stack[-1]
        return self.current_segment()

    def is_at_entrance(self) -> bool:
        """Check if player is at the first segment (entrance)."""
        return len(self.visited_stack) <= 1

    def to_dict(self) -> dict:
        """Serialize to a JSON-compatible dictionary."""
        return {
            "segments": {str(k): v.to_dict() for k, v in self.segments.items()},
            "current_segment_id": self.current_segment_id,
            "max_level": self.max_level,
            "visited_stack": self.visited_stack,
            "next_id": self._next_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DungeonGraph":
        """Reconstruct a DungeonGraph from a stored dictionary."""
        graph = cls()
        graph._next_id = data.get("next_id", 0)
        graph.max_level = data.get("max_level", 0)
        graph.visited_stack = data.get("visited_stack", [])
        graph.current_segment_id = data.get("current_segment_id")

        for seg_id_str, seg_data in data.get("segments", {}).items():
            segment = Segment.from_dict(seg_data)
            graph.segments[segment.id] = segment

        return graph


def generate_initial_segment(graph: DungeonGraph) -> Segment:
    """Generate the initial staircase segment (level 1, 1 door).

    Args:
        graph: The DungeonGraph to add the segment to.

    Returns:
        The newly created initial segment.
    """
    segment = graph.create_segment(
        seg_type=SegmentType.ESCADARIA,
        level=1,
        doors_count=1,
    )
    graph.set_current(segment.id)
    return segment


def generate_next_segment(
    graph: DungeonGraph, door_index: int
) -> Segment:
    """Generate a new segment by opening a door from the current segment.

    Uses the transition table corresponding to the current segment type.

    Args:
        graph: The DungeonGraph.
        door_index: Which door to open (0-based).

    Returns:
        The newly created or existing target segment.

    Raises:
        ValueError: If current segment is None or door is out of range.
    """
    from notecli import tables
    import random

    current = graph.current_segment()
    if current is None:
        raise ValueError("No current segment.")
    if door_index < 0 or door_index >= current.doors_count:
        raise ValueError(f"Invalid door index: {door_index}. Segment has {current.doors_count} doors.")

    # Check if door already opened
    existing_target = current.get_target(door_index)
    if existing_target is not None:
        return graph.segments[existing_target]

    # Select transition table based on current segment type
    transition_map = {
        SegmentType.ESCADARIA: tables.STAIRCASE_TRANSITIONS,
        SegmentType.CORREDOR: tables.CORRIDOR_TRANSITIONS,
        SegmentType.SALA: tables.ROOM_TRANSITIONS,
        SegmentType.SALA_FINAL: tables.ROOM_TRANSITIONS,
    }
    transition_table = transition_map.get(current.type, tables.ROOM_TRANSITIONS)

    # Roll d6 to select from table
    roll = random.randint(1, 6)
    choice = transition_table[roll - 1]

    # Determine level
    new_level = current.level
    if choice["type"] == "escadaria":
        new_level = current.level + 1

    # Determine segment type
    type_map = {
        "escadaria": SegmentType.ESCADARIA,
        "corredor": SegmentType.CORREDOR,
        "sala": SegmentType.SALA,
    }
    new_type = type_map.get(choice["type"], SegmentType.SALA)

    # Check for Final Room conditions
    is_final = False
    if new_level >= 3 and new_type == SegmentType.ESCADARIA:
        # Entering level 3 → Final Room
        new_type = SegmentType.SALA_FINAL
        is_final = True

    # Create the new segment
    new_segment = graph.create_segment(
        seg_type=new_type,
        level=new_level,
        doors_count=choice["doors"],
        is_final_room=is_final,
    )

    # Record the connection
    current.add_connection(door_index, new_segment.id)
    graph.set_current(new_segment.id)

    # Check if this should be Final Room (no more path forward and level < 3)
    if not is_final and new_segment.doors_count == 0 and graph.max_level < 3:
        # Mark as Final Room if no doors and can't reach level 3
        new_segment.is_final_room = True

    return new_segment


@dataclass
class ExplorationSession:
    """Represents an active exploration session linking a dungeon to a character."""

    dungeon: Dungeon
    character_index: int
    started_at: str
    active: bool = field(default=True)
    segment_graph: Optional[DungeonGraph] = field(default=None)

    def to_dict(self) -> dict:
        """Serialize to a JSON-compatible dictionary."""
        base = {
            "dungeon": {
                "type_name": self.dungeon.type.name,
                "name": self.dungeon.name,
                "entrance_shown": self.dungeon.entrance_shown,
                "current_room": self.dungeon.current_room,
                "rooms_visited": self.dungeon.rooms_visited,
            },
            "character_index": self.character_index,
            "started_at": self.started_at,
            "active": self.active,
        }
        if self.segment_graph:
            base["segment_graph"] = self.segment_graph.to_dict()
        return base

    @classmethod
    def from_dict(cls, data: dict) -> "ExplorationSession":
        """Reconstruct an ExplorationSession from a stored dictionary."""
        dungeon_data = data["dungeon"]
        # Look up the DungeonType by name
        from notecli import tables

        dungeon_type = None
        for dt in tables.DUNGEON_TYPES.values():
            if dt.name == dungeon_data["type_name"]:
                dungeon_type = dt
                break
        if dungeon_type is None:
            raise ValueError(f"Unknown dungeon type: {dungeon_data['type_name']}")

        dungeon = Dungeon(
            type=dungeon_type,
            name=dungeon_data["name"],
            entrance_shown=dungeon_data.get("entrance_shown", False),
            current_room=dungeon_data.get("current_room", 0),
            rooms_visited=dungeon_data.get("rooms_visited", 0),
        )

        segment_graph = None
        if "segment_graph" in data:
            segment_graph = DungeonGraph.from_dict(data["segment_graph"])

        return cls(
            dungeon=dungeon,
            character_index=data["character_index"],
            started_at=data["started_at"],
            active=data.get("active", True),
            segment_graph=segment_graph,
        )


def generate_dungeon(roll: int) -> Dungeon:
    """Generate a new dungeon from a d6 roll.

    Args:
        roll: Integer 1-6 corresponding to DUNGEON_TYPES.

    Returns:
        A new Dungeon instance with generated name and fresh state.

    Raises:
        ValueError: If roll is not between 1 and 6.
    """
    from notecli import tables

    if roll not in tables.DUNGEON_TYPES:
        raise ValueError(f"Invalid dungeon roll: {roll}. Must be 1-6.")

    dungeon_type = tables.DUNGEON_TYPES[roll]
    name = generate_dungeon_name(dungeon_type)

    return Dungeon(
        type=dungeon_type,
        name=name,
    )
