"""Segment entities for dungeon exploration."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple


class SegmentType(Enum):
    """Types of dungeon segments."""
    ESCADARIA = "escadaria"
    CORREDOR = "corredor"
    SALA = "sala"
    SALA_FINAL = "sala_final"


@dataclass
class Segment:
    """Represents a single segment of the dungeon.

    Attributes:
        id: Unique auto-incremented identifier.
        type: Type of this segment.
        level: Dungeon level (1-based).
        doors_count: Number of doors in this segment.
        connected_segments: List of (door_index, target_segment_id).
        is_final_room: True if this is the Final Room.
        has_monsters: True if this segment has monsters.
    """
    id: int
    type: SegmentType
    level: int
    doors_count: int
    connected_segments: List[Tuple[int, int]] = field(default_factory=list)
    is_final_room: bool = field(default=False)
    has_monsters: bool = field(default=False)

    def opened_doors_count(self) -> int:
        """Return number of doors that have been opened (have connections)."""
        return len(self.connected_segments)

    def remaining_doors_count(self) -> int:
        """Return number of doors that haven't been opened yet."""
        return self.doors_count - self.opened_doors_count()

    def is_connected(self, door_index: int) -> bool:
        """Check if a specific door has been opened."""
        return any(d == door_index for d, _ in self.connected_segments)

    def get_target(self, door_index: int) -> int | None:
        """Get target segment ID for a given door, or None if not opened."""
        for d, target_id in self.connected_segments:
            if d == door_index:
                return target_id
        return None

    def add_connection(self, door_index: int, target_segment_id: int) -> None:
        """Record that a door leads to a specific segment."""
        self.connected_segments.append((door_index, target_segment_id))

    def to_dict(self) -> dict:
        """Serialize to a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "level": self.level,
            "doors_count": self.doors_count,
            "connected_segments": [[d, t] for d, t in self.connected_segments],
            "is_final_room": self.is_final_room,
            "has_monsters": self.has_monsters,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Segment":
        """Reconstruct a Segment from a stored dictionary."""
        return cls(
            id=data["id"],
            type=SegmentType(data["type"]),
            level=data["level"],
            doors_count=data["doors_count"],
            connected_segments=[
                (d, t) for d, t in data.get("connected_segments", [])
            ],
            is_final_room=data.get("is_final_room", False),
            has_monsters=data.get("has_monsters", False),
        )
