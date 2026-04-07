"""Dungeon entities for exploration sessions."""

from dataclasses import dataclass, field
from typing import Optional
import random

from notecli.entities.dungeon_name import generate_dungeon_name
from notecli.entities.segment import Segment, SegmentType, create_doors_for_segment
from notecli.entities.door import Door


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

    def create_segment(
        self,
        seg_type: SegmentType,
        level: int,
        door_target_ids: list[int],
        is_final_room: bool = False,
        has_monsters: bool = False,
    ) -> Segment:
        """Create and add a new segment to the graph with doors.

        Args:
            seg_type: Type of segment.
            level: Dungeon level.
            door_target_ids: List of target segment IDs for each door.
            is_final_room: Whether this is the Final Room.
            has_monsters: Whether this segment has monsters.

        Returns:
            The newly created segment.
        """
        seg_id = self._allocate_id()
        segment = Segment(
            id=seg_id,
            type=seg_type,
            level=level,
            is_final_room=is_final_room,
            has_monsters=has_monsters,
        )
        create_doors_for_segment(segment, door_target_ids)
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


def close_opened_doors(segment) -> int:
    """Close all opened doors in a segment."""
    count = 0
    for door in segment.doors:
        if door.is_open:
            door.close()
            count += 1
    return count



def enter_room(graph, door_index, dungeon_type_name):
    """Enter the room through an open, unlocked, trap-free door."""
    current = graph.current_segment()
    if current is None:
        return False, "Erro: nenhum segmento atual."

    door = current.get_door(door_index)
    if door is None:
        return False, f"Porta {door_index + 1} nao existe."

    if not door.can_enter():
        return False, f"Nao e possivel entrar pela porta {door_index + 1}."

    target = graph.segments.get(door.target_segment_id)
    if target is None:
        return False, f"Destino da porta {door_index + 1} nao encontrado."

    door.close()
    close_opened_doors(current)

    graph.set_current(target.id)
    return True, "🔑 Voce entra. Porta fecha atras."

def roll_door() -> tuple:
    """Roll d6 to determine door state.
    Returns: (state_name, message)
    """
    roll = random.randint(1, 6)
    if roll == 1:
        return "armadilha", "⚠️ Armadilha acionada!"
    elif roll <= 3:
        return "trancada", "🔐 Porta Trancada!"
    else:
        return "destrancada", "✅ Porta Destrancada!"


def trigger_trap(dungeon_type_name: str) -> str:
    """Trigger a trap and return the result from the appropriate trap table.

    Args:
        dungeon_type_name: Name of the current dungeon type.

    Returns:
        Trap result string (placeholder for now).
    """
    from notecli.tables import TRAP_TABLES

    table = TRAP_TABLES.get(dungeon_type_name, TRAP_TABLES["Templo"])
    roll = random.randint(1, 6)
    return table[roll - 1]


def generate_initial_segment(graph: DungeonGraph) -> Segment:
    """Generate the initial staircase segment (level 1, 1 door with target -1).

    Args:
        graph: The DungeonGraph to add the segment to.

    Returns:
        The newly created initial segment.
    """
    segment = graph.create_segment(
        seg_type=SegmentType.ESCADARIA,
        level=1,
        door_target_ids=[-1],  # Target filled during full generation
    )
    graph.set_current(segment.id)
    return segment


def generate_full_dungeon(graph: DungeonGraph, dungeon_type_name: str) -> None:
    """Generate the entire dungeon before exploration begins.

    Each door from every segment leads to a newly generated segment.
    All doors are connected. Final Room is placed when level 3 is reached
    or when all doors are connected and the last segment has no further exits.

    Args:
        graph: The DungeonGraph to populate.
        dungeon_type_name: Name of the dungeon type (for trap table reference).
    """
    from notecli import tables

    transition_map = {
        SegmentType.ESCADARIA: tables.STAIRCASE_TRANSITIONS,
        SegmentType.CORREDOR: tables.CORRIDOR_TRANSITIONS,
        SegmentType.SALA: tables.ROOM_TRANSITIONS,
    }
    type_map = {
        "escadaria": SegmentType.ESCADARIA,
        "corredor": SegmentType.CORREDOR,
        "sala": SegmentType.SALA,
    }

    # Create initial staircase with 1 door (target = -1, to be filled)
    initial = graph.create_segment(SegmentType.ESCADARIA, 1, [-1])
    graph.set_current(initial.id)

    final_room_id: Optional[int] = None

    # Iterate until all doors have targets
    max_iterations = 200  # safety limit
    iteration = 0
    while iteration < max_iterations:
        iteration += 1

        # Find first unconnected door
        unconnected = None
        for seg in sorted(graph.segments.values(), key=lambda s: s.id):
            for door in seg.doors:
                if door.target_segment_id in (None, -1):
                    unconnected = (seg, door)
                    break
            if unconnected:
                break

        if unconnected is None:
            # All doors connected — place Final Room on last segment if not already
            if final_room_id is None:
                last_seg = max(graph.segments.values(), key=lambda s: s.id)
                last_seg.is_final_room = True
                last_seg.type = SegmentType.SALA_FINAL
                last_seg.doors = []
                final_room_id = last_seg.id
            break

        parent_seg, door = unconnected
        t_table = transition_map.get(parent_seg.type, tables.ROOM_TRANSITIONS)
        roll = random.randint(1, 6)
        choice = t_table[roll - 1]

        new_level = parent_seg.level
        if choice["type"] == "escadaria":
            new_level = parent_seg.level + 1

        new_type = type_map.get(choice["type"], SegmentType.SALA)

        is_final = False
        if new_level >= 3 and new_type == SegmentType.ESCADARIA:
            new_type = SegmentType.SALA_FINAL
            is_final = True

        # Final Room has no exit doors (boss room)
        final_doors_count = 0 if is_final else choice.get("doors", 0)

        new_seg_id = graph._allocate_id()
        new_segment = Segment(
            id=new_seg_id,
            type=new_type,
            level=new_level,
            is_final_room=is_final,
        )
        create_doors_for_segment(new_segment, [
            -1 for _ in range(final_doors_count)
        ])
        graph.segments[new_seg_id] = new_segment
        if new_level > graph.max_level:
            graph.max_level = new_level

        # Connect the door
        door.target_segment_id = new_seg_id

        if is_final:
            final_room_id = new_seg_id
            break

    # Ensure Final Room is marked
    if final_room_id is not None:
        final_room = graph.segments.get(final_room_id)
        if final_room:
            final_room.is_final_room = True
            final_room.type = SegmentType.SALA_FINAL



def open_door(graph, door_index, dungeon_type_name):
    """Attempt to open a door, rolling for state."""
    current = graph.current_segment()
    if current is None:
        return "error", "Erro: nenhum segmento atual."

    door = current.get_door(door_index)
    if door is None:
        return "error", f"Porta {door_index + 1} não existe."

    if door.is_open:
        target = graph.segments.get(door.target_segment_id)
        if target:
            return "already_open", f"Porta já aberta → {target.type.value} (Nível {target.level})"
        return "already_open", "Porta já aberta."

    if door.is_revealed() and not door.is_locked and not door.has_trap:
        return "already_revealed", "Porta já revelada. Pode entrar."

    if door.is_locked:
        return "locked", "🔐 Porta Trancada! Use 'destrancar' para abrir (consome 1 tocha)."

    if door.has_trap:
        trap_result = trigger_trap(dungeon_type_name)
        door.is_open = True
        door.has_trap = False
        return "trap", f"⚠️ Armadilha! {trap_result}"

    state_name, msg = roll_door()

    if state_name == "armadilha":
        trap_result = trigger_trap(dungeon_type_name)
        door.is_open = True
        door.has_trap = True
        return "trap", f"{msg} {trap_result}"

    elif state_name == "trancada":
        door.is_locked = True
        return "trancada", f"{msg} Use 'destrancar' para abrir (consome 1 tocha)."

    else:
        if door.target_segment_id is None:
            return "error", "Erro: porta sem destino."
        door.is_open = True
        target = graph.segments.get(door.target_segment_id)
        if target:
            msg = f"{msg} → {target.type.value} (Nível {target.level})"
        return "destrancada", msg

def unlock_door(graph, door_index, pc):
    """Unlock a locked door by picking the lock, consuming 1 torch."""
    current = graph.current_segment()
    if current is None:
        return False, "Erro: nenhum segmento atual."

    door = current.get_door(door_index)
    if door is None:
        return False, f"Porta {door_index + 1} não existe."

    if not door.is_locked:
        return False, f"Porta {door_index + 1} não está trancada."

    if pc.torches < 1:
        return False, "🌑 Suas tochas acabaram! Não é possível destrancar a porta."

    pc.consume_torch()
    door.is_locked = False
    door.is_open = True

    target = graph.segments.get(door.target_segment_id)
    if target:
        return True, f"🔑 Porta {door_index + 1} destrancada! → {target.type.value} (Nível {target.level})"
    return True, f"🔑 Porta {door_index + 1} destrancada!"
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
