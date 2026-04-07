"""Door entity with 3 independent attributes: visibility, lock, trap."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


@dataclass
class Door:
    """Represents a door between dungeon segments.

    Attributes:
        index: Door index in segment (0-based).
        is_open: Whether the door is physically open.
        is_locked: Whether the door is locked (needs torch to pick).
        has_trap: Whether the door has an active trap.
        target_segment_id: ID of the target segment (set on first reveal).
    """
    index: int
    is_open: bool = field(default=False)
    is_locked: bool = field(default=False)
    has_trap: bool = field(default=False)
    target_segment_id: Optional[int] = field(default=None)

    def close(self) -> None:
        """Close the door (sets is_open=False). Keeps lock and trap state."""
        self.is_open = False

    def is_revealed(self) -> bool:
        """Check if the door's destination has been revealed."""
        return self.target_segment_id is not None

    def can_enter(self) -> bool:
        """Check if player can enter through this door."""
        return self.is_open and not self.is_locked and not self.has_trap

    def display_status(self) -> str:
        """Return a human-readable status string."""
        if self.is_open:
            return "✅ Aberta"
        if self.is_locked and self.has_trap:
            return "🔐🔒 Fechada + Trancada + Armadilha"
        if self.is_locked:
            return "🔐 Fechada + Trancada"
        if self.has_trap:
            return "⚠️ Fechada + Armadilha"
        return "🔒 Fechada"

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dict."""
        return {
            "index": self.index,
            "is_open": self.is_open,
            "is_locked": self.is_locked,
            "has_trap": self.has_trap,
            "target_segment_id": self.target_segment_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Door":
        """Reconstruct from dict, with backward compatibility for old `state` field."""
        door = cls(
            index=data["index"],
            target_segment_id=data.get("target_segment_id"),
        )

        # Handle new format
        if "is_open" in data:
            door.is_open = data["is_open"]
            door.is_locked = data.get("is_locked", False)
            door.has_trap = data.get("has_trap", False)
            return door

        # Migrate from old `state` string format
        old_state = data.get("state", "fechada")
        if old_state == "destrancada":
            door.is_open = True
        elif old_state == "trancada":
            door.is_locked = True
        elif old_state == "armadilha":
            door.has_trap = True
        # "fechada" → all False (default)

        return door
