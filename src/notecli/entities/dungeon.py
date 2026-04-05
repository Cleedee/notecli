"""Dungeon entities for exploration sessions."""

from dataclasses import dataclass, field
from typing import Optional

from notecli.entities.dungeon_name import generate_dungeon_name


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


@dataclass
class ExplorationSession:
    """Represents an active exploration session linking a dungeon to a character."""

    dungeon: Dungeon
    character_index: int
    started_at: str
    active: bool = field(default=True)

    def to_dict(self) -> dict:
        """Serialize to a JSON-compatible dictionary."""
        return {
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
        return cls(
            dungeon=dungeon,
            character_index=data["character_index"],
            started_at=data["started_at"],
            active=data.get("active", True),
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
