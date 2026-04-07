"""Dungeon map display CLI module."""

import sys

from notecli.cli.storage import load_exploration
from notecli.entities.segment import SegmentType

from notecli.entities.dungeon import DungeonGraph

_SEGMENT_EMOJI = {
    SegmentType.ESCADARIA: "🪜",
    SegmentType.CORREDOR: "🚶",
    SegmentType.SALA: "🏛️",
    SegmentType.SALA_FINAL: "🏆",
}

_SEGMENT_NAMES = {
    SegmentType.ESCADARIA: "Escadaria",
    SegmentType.CORREDOR: "Corredor",
    SegmentType.SALA: "Sala",
    SegmentType.SALA_FINAL: "Sala Final",
}



def display_map() -> None:
    """Display the full dungeon map from the last exploration session.

    Shows all segments, doors, states, and connections with a legend.
    If no session exists, displays an informative message.
    """
    session_data = load_exploration()
    if session_data is None:
        print("Nenhuma masmorra foi explorada ainda. Execute 'notecli explore' para começar.")
        return

    graph_data = session_data.get("segment_graph")
    if graph_data is None:
        print("Nenhuma masmorra foi explorada ainda. Execute 'notecli explore' para começar.")
        return

    graph = DungeonGraph.from_dict(graph_data)
    dungeon_name = session_data.get("dungeon", {}).get("name", "Masmorra desconhecida")

    # Header
    print(f"\n🏰 {dungeon_name}")
    print("═" * 40)

    # Sort segments by id for consistent output
    sorted_segments = sorted(graph.segments.values(), key=lambda s: s.id)

    for seg in sorted_segments:
        emoji = _SEGMENT_EMOJI.get(seg.type, "📍")
        name = _SEGMENT_NAMES.get(seg.type, seg.type.value)
        final_marker = " 🏆" if seg.is_final_room else ""

        print(f"\n  {emoji} {name} — Nível {seg.level}{final_marker}")

        if not seg.doors:
            print("    (sem portas)")
            continue

        for i, door in enumerate(seg.doors):
            icon = door.display_status()
            state_name = door.display_status()
            target = graph.segments.get(door.target_segment_id)

            if target:
                t_emoji = _SEGMENT_EMOJI.get(target.type, "📍")
                t_name = _SEGMENT_NAMES.get(target.type, target.type.value)
                connector = "→" if i == 0 else " "
                print(f"    {connector} {icon} Porta {door.index + 1} ({state_name}) {t_emoji} {t_name} (Nível {target.level})")
            else:
                print(f"    {icon} Porta {door.index + 1} ({state_name})")

    # Legend
    print("\n── Legenda ──")
    print("  Segmentos: 🪜 Escadaria  🚶 Corredor  🏛️ Sala  🏆 Sala Final")
    print("  Portas:    🔒 Fechada  ⚠️ Armadilha  🔐 Trancada  ✅ Destrancada")
