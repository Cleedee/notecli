"""Interactive dungeon exploration menu CLI."""

import sys
from datetime import datetime
from typing import Optional

from notecli.dice import Roller
from notecli.entities.dungeon import (
    generate_dungeon,
    Dungeon,
    DungeonGraph,
    ExplorationSession,
    generate_initial_segment,
    generate_next_segment,
)
from notecli.entities.segment import SegmentType
from notecli.cli.storage import (
    load_characters,
    save_exploration,
    load_exploration,
    clear_exploration,
    save_characters,
)

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


def _prompt(prompt_text: str) -> str:
    """Read user input with a prompt, returning stripped text."""
    return input(prompt_text).strip()


def display_dungeon_info(dungeon: Dungeon) -> None:
    """Display dungeon type, name, and entrance description."""
    print(f"\n🏰 Gerando masmorra...")
    print(f"  Tipo: {dungeon.type.name}")
    print(f"  Nome: {dungeon.name}")
    print(f"\n📖 Você chega à entrada de {dungeon.name}.")
    print(f"   {dungeon.type.entrance_description}")


def display_segment(segment, graph: Optional[DungeonGraph] = None) -> None:
    """Display current segment info."""
    emoji = _SEGMENT_EMOJI.get(segment.type, "📍")
    name = _SEGMENT_NAMES.get(segment.type, segment.type.value)
    title = name.title() if name else segment.type.value

    print(f"\n{emoji} {title} — Nível {segment.level}")

    if segment.is_final_room:
        print("   🏆 Você encontrou a Sala Final!")

    doors = segment.doors_count
    remaining = segment.remaining_doors_count()
    opened = segment.opened_doors_count()

    if doors == 0:
        print("   Nenhuma porta disponível — caminho sem saída.")
    elif remaining == 0:
        print(f"   {opened} porta(s) já explorada(s). Nenhuma restante.")
    elif remaining == 1:
        print(f"   {remaining} porta à frente.")
    else:
        print(f"   {remaining} portas à frente.")

    # Show already-opened doors info
    for door_idx, target_id in segment.connected_segments:
        target = graph.segments.get(target_id) if graph else None
        target_desc = ""
        if target:
            t_name = _SEGMENT_NAMES.get(target.type, target.type.value)
            target_desc = f" → {t_name} (Nível {target.level})"
            if target.is_final_room:
                target_desc += " 🏆"
        print(f"   Porta {door_idx + 1}{target_desc} (explorada)")


def select_or_create_character():
    """Let the player select an existing character or create a new one."""
    from notecli.entities.player import PlayerCharacter

    characters = load_characters()

    if not characters:
        print("\n⚠️ Nenhum personagem encontrado. Criando novo personagem...")
        return _create_character()

    while True:
        print("\n=== Escolha um Personagem ===")
        for i, ch in enumerate(characters, 1):
            status = "vivo" if ch.get("alive", True) else "morto"
            hp = f"{ch['hp_current']}/{ch['health_points']}"
            name = ch.get("name", "Sem nome")
            ancestry = ch.get("ancestry", "?")
            occupation = ch.get("occupation", "?")
            print(f"  {i}) {ancestry} {occupation} — HP: {hp} — {status} ({name})")

        print("  0) Criar novo personagem")
        print("  q) Sair")

        try:
            choice = _prompt("> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            return None

        if choice == "q":
            return None

        if choice == "0":
            return _create_character()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(characters):
                pc = PlayerCharacter.from_dict(characters[idx])
                return pc
            else:
                print(
                    "⚠️ Opção inválida. Escolha um número da lista ou 0 para criar novo personagem.",
                    file=sys.stderr,
                )
        except ValueError:
            print("⚠️ Opção inválida. Digite um número.", file=sys.stderr)


def _create_character():
    """Create a new character using the character menu flow."""
    from notecli.cli.character_menu import (
        create_character as menu_create_character,
    )

    try:
        pc = menu_create_character()
        return pc
    except Exception as e:
        print(f"⚠️ Erro ao criar personagem: {e}", file=sys.stderr)
        return None


def start_new_session(dungeon, character_index: int, graph: DungeonGraph) -> ExplorationSession:
    """Start a new exploration session with segment graph."""
    session = ExplorationSession(
        dungeon=dungeon,
        character_index=character_index,
        started_at=datetime.now().isoformat(),
        active=True,
        segment_graph=graph,
    )
    save_exploration(session.to_dict())
    return session


def show_character_status(pc) -> None:
    """Display character status line after selection."""
    magic_info = ""
    if pc.magics:
        magic_names = ", ".join(f"{m['name']} ({m['uses']})" for m in pc.magics)
        magic_info = f" | Magias: {len(pc.magics)} ({magic_names})"
    else:
        magic_info = " | Magias: 0"

    print(
        f"\n🗡️ {pc.ancestry} {pc.occupation} começa a exploração..."
    )
    print(
        f"   Tochas: {pc.torches}{magic_info} | HP: {pc.hp_current}/{pc.health_points}"
    )


def exploration_loop(pc, dungeon, graph: DungeonGraph) -> None:
    """Main exploration loop: display segment, accept commands."""
    while True:
        current = graph.current_segment()
        if current is None:
            print("Erro: nenhum segmento atual.")
            return

        display_segment(current, graph)
        print()

        # Build action prompt
        actions = []
        if current.remaining_doors_count() > 0:
            for d in range(current.doors_count):
                if not current.is_connected(d):
                    actions.append(f"abrir {d + 1}")
        actions.append("voltar")
        actions.append("sair")
        actions.append("ajuda")

        action_prompt = f"Ações: {', '.join(actions)}\n> "

        try:
            cmd = _prompt(action_prompt).strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if cmd == "ajuda":
            print("\nComandos disponíveis:")
            print("  abrir <N>  — Abre a porta N")
            print("  voltar     — Retorna ao segmento anterior")
            print("  sair       — Tenta sair da masmorra")
            print("  status     — Mostra status do personagem")
            print("  ajuda      — Mostra esta ajuda")
            print("  q/sair     — Sai do jogo")
            continue

        if cmd in ("q", "sair"):
            _handle_exit(pc, graph)
            return

        if cmd == "voltar":
            _handle_backtrack(pc, graph)
            continue

        if cmd == "status":
            show_character_status(pc)
            continue

        if cmd.startswith("abrir"):
            parts = cmd.split()
            if len(parts) < 2:
                print("⚠️ Use: abrir <número da porta>", file=sys.stderr)
                continue
            try:
                door_num = int(parts[1])
            except ValueError:
                print("⚠️ Número da porta inválido.", file=sys.stderr)
                continue

            door_idx = door_num - 1  # 0-based
            if door_idx < 0 or door_idx >= current.doors_count:
                print(
                    f"⚠️ Porta {door_num} não existe. Este segmento tem {current.doors_count} portas.",
                    file=sys.stderr,
                )
                continue

            _handle_open_door(pc, graph, door_idx)

            # Check if we reached Final Room
            new_current = graph.current_segment()
            if new_current and new_current.is_final_room:
                display_segment(new_current, graph)
                print("\n🎉 Você completou a masmorra!")
                # Save and offer exit
                session_data = load_exploration()
                if session_data:
                    session_data["active"] = False
                    from notecli.cli.storage import save_exploration as _save
                    _save({"version": 1, "session": session_data})
                return

            continue

        print("⚠️ Comando desconhecido. Digite 'ajuda' para ver as opções.", file=sys.stderr)


def _handle_open_door(pc, graph: DungeonGraph, door_idx: int) -> None:
    """Handle opening a door, generating or visiting the target segment."""
    current = graph.current_segment()

    # If door already opened, just show info
    target_id = current.get_target(door_idx)
    if target_id is not None:
        target = graph.segments.get(target_id)
        if target:
            t_name = _SEGMENT_NAMES.get(target.type, target.type.value)
            print(f"\n🚪 Porta {door_idx + 1} já foi aberta. Ela leva a: {t_name} (Nível {target.level})")
            graph.set_current(target.id)
            display_segment(target, graph)
        return

    print(f"\n🚪 Você abre a porta {door_idx + 1}...")

    new_segment = generate_next_segment(graph, door_idx)

    # Consume 1 torch on entering new segment
    pc.consume_torch()

    # Persist character
    characters = load_characters()
    for i, ch in enumerate(characters):
        if ch.get("name") == pc.name and ch.get("ancestry") == pc.ancestry:
            characters[i] = pc.to_dict()
            break
    save_characters(characters)

    # Persist session
    session_data = load_exploration()
    if session_data:
        session_data["segment_graph"] = graph.to_dict()
        from notecli.cli.storage import save_exploration as _save
        _save({"version": 1, "session": session_data})


def _handle_backtrack(pc, graph: DungeonGraph) -> None:
    """Handle backtracking to previous segment."""
    if graph.is_at_entrance():
        print("\nVocê está na entrada da masmorra.")
        _handle_exit(pc, graph)
        return

    prev = graph.backtrack()
    if prev:
        print("\n🔙 Você retorna ao segmento anterior...")
        display_segment(prev, graph)

        # Persist session
        session_data = load_exploration()
        if session_data:
            session_data["segment_graph"] = graph.to_dict()
            from notecli.cli.storage import save_exploration as _save
            _save({"version": 1, "session": session_data})


def _handle_exit(pc, graph: DungeonGraph) -> None:
    """Handle exiting the dungeon."""
    # Check if path to entrance has monsters
    has_monsters = False
    for seg_id in graph.visited_stack:
        seg = graph.segments.get(seg_id)
        if seg and seg.has_monsters:
            has_monsters = True
            break

    if has_monsters:
        print("\n⚠️ Há monstros no caminho até a entrada! Cuidado ao sair.")
    else:
        try:
            choice = _prompt("\n⚠️ Caminho livre. Sair da masmorra? (s/n) > ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            return

        if choice == "s":
            # Deactivate session
            session_data = load_exploration()
            if session_data:
                session_data["active"] = False
                from notecli.cli.storage import save_exploration as _save
                _save({"version": 1, "session": session_data})

            # Persist character
            characters = load_characters()
            for i, ch in enumerate(characters):
                if ch.get("name") == pc.name and ch.get("ancestry") == pc.ancestry:
                    characters[i] = pc.to_dict()
                    break
            save_characters(characters)

            print("\n🏁 Você sai da masmorra com vida.")
            print(f"   Personagem {pc.name} salvo.")
            return

    print("Continuando a exploração...")


def explore(resume: bool = False) -> None:
    """Main exploration entry point."""
    # Try to resume if requested
    if resume:
        session_data = load_exploration()
        if session_data and session_data.get("active"):
            graph = None
            if "segment_graph" in session_data:
                graph = DungeonGraph.from_dict(session_data["segment_graph"])

            if graph and graph.current_segment():
                from notecli.entities.player import PlayerCharacter
                characters = load_characters()
                if 0 < session_data["character_index"] <= len(characters):
                    pc = PlayerCharacter.from_dict(characters[session_data["character_index"] - 1])
                    print("\n🔄 Sessão de exploração encontrada:")
                    current = graph.current_segment()
                    t_name = _SEGMENT_NAMES.get(current.type, current.type.value)
                    print(f"   Segmento: {t_name} — Nível {current.level}")
                    print(f"   Salas visitadas: {len(graph.segments)}")

                    try:
                        choice = _prompt("Continuar desta sessão? (s/n) > ").strip().lower()
                    except (KeyboardInterrupt, EOFError):
                        print()
                        return

                    if choice == "s":
                        print(f"\n🗡️ {pc.ancestry} {pc.occupation} continua explorando...")
                        exploration_loop(pc, None, graph)
                        return
                else:
                    clear_exploration()
                    print("Personagem não encontrado. Iniciando nova exploração...")
            else:
                clear_exploration()
                print("Sessão corrompida. Iniciando nova exploração...")
        else:
            clear_exploration()

    # Generate new dungeon
    roll = Roller.d6()
    dungeon = generate_dungeon(roll)

    # Display dungeon info
    display_dungeon_info(dungeon)

    # Select or create character
    pc = select_or_create_character()
    if pc is None:
        print("Exploração cancelada.")
        return

    # Initialize segment graph
    graph = DungeonGraph()
    initial = generate_initial_segment(graph)

    # Display initial segment
    print("\n" + "=" * 40)
    display_segment(initial, graph)

    # Consume 1 torch on exploration start
    pc.consume_torch()

    # Persist updated character
    characters = load_characters()
    for i, ch in enumerate(characters):
        if ch.get("name") == pc.name and ch.get("ancestry") == pc.ancestry:
            characters[i] = pc.to_dict()
            break
    save_characters(characters)

    # Find character index
    char_index = 0
    for i, ch in enumerate(characters, 1):
        if ch.get("name") == pc.name and ch.get("ancestry") == pc.ancestry:
            char_index = i
            break

    if char_index == 0:
        char_index = len(characters)

    start_new_session(dungeon, char_index, graph)

    # Show status
    show_character_status(pc)

    # Enter exploration loop
    print("\nDigite 'ajuda' para ver as ações disponíveis.")
    exploration_loop(pc, dungeon, graph)
