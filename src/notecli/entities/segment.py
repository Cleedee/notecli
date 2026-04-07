"""Segment entities for dungeon exploration."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from notecli.entities.door import Door


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
        doors: List of Door objects.
        is_final_room: True if this is the Final Room.
        has_monsters: True if this segment has monsters.
    """
    id: int
    type: SegmentType
    level: int
    doors: List[Door] = field(default_factory=list)
    is_final_room: bool = field(default=False)
    has_monsters: bool = field(default=False)

    @property
    def doors_count(self) -> int:
        """Number of doors in this segment."""
        return len(self.doors)

    def get_door(self, index: int) -> Optional[Door]:
        """Get door by index, or None if invalid."""
        if 0 <= index < len(self.doors):
            return self.doors[index]
        return None

    def opened_doors_count(self) -> int:
        """Return number of doors that are currently open."""
        return sum(1 for d in self.doors if d.is_open)

    def remaining_doors_count(self) -> int:
        """Return number of doors that are not open."""
        return sum(1 for d in self.doors if not d.is_open)

    def locked_doors_count(self) -> int:
        """Return number of doors that are locked."""
        return sum(1 for d in self.doors if d.is_locked())

    def to_dict(self) -> dict:
        """Serialize to a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "level": self.level,
            "doors": [d.to_dict() for d in self.doors],
            "is_final_room": self.is_final_room,
            "has_monsters": self.has_monsters,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Segment":
        """Reconstruct a Segment from a stored dictionary."""
        segment = cls(
            id=data["id"],
            type=SegmentType(data["type"]),
            level=data["level"],
            is_final_room=data.get("is_final_room", False),
            has_monsters=data.get("has_monsters", False),
        )
        for door_data in data.get("doors", []):
            door = Door.from_dict(door_data)
            segment.doors.append(door)
        return segment


def create_doors_for_segment(seg: "Segment", target_ids: List[int]) -> None:
    """Create closed doors for a segment with given target IDs.

    Args:
        seg: The segment to add doors to.
        target_ids: List of target segment IDs for each door.
    """
    seg.doors = [
        Door(index=i, is_open=False, is_locked=False, has_trap=False, target_segment_id=tid)
        for i, tid in enumerate(target_ids)
    ]
