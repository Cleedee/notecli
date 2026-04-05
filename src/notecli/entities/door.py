"""Door entities for dungeon exploration."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class DoorState(Enum):
    """States of a dungeon door."""
    FECHADA = "fechada"
    ARMADILHA = "armadilha"
    TRANCADA = "trancada"
    DESTRANCADA = "destrancada"


@dataclass
class Door:
    """Represents a door between dungeon segments.

    Attributes:
        index: Door index in segment (0-based).
        state: Current state of the door.
        target_segment_id: ID of the target segment (set during generation).
        trap_result: Trap result string (set when state = ARMADILHA).
    """
    index: int
    state: DoorState
    target_segment_id: int
    trap_result: Optional[str] = field(default=None)

    def is_opened(self) -> bool:
        """Check if door has been opened (any state other than FECHADA)."""
        return self.state != DoorState.FECHADA

    def is_locked(self) -> bool:
        """Check if door is locked."""
        return self.state == DoorState.TRANCADA

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dict."""
        return {
            "index": self.index,
            "state": self.state.value,
            "target_segment_id": self.target_segment_id,
            "trap_result": self.trap_result,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Door":
        """Reconstruct from dict."""
        return cls(
            index=data["index"],
            state=DoorState(data["state"]),
            target_segment_id=data["target_segment_id"],
            trap_result=data.get("trap_result"),
        )
