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
    generate_full_dungeon,
    open_door,
    unlock_door,
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

    remaining = segment.remaining_doors_count()
    locked = segment.locked_doors_count()
    total = segment.doors_count

    if total == 0:
        print("   Nenhuma porta disponível — caminho sem saída.")
    elif remaining == 0 and total > 0:
        print(f"   {total} porta(s) já explorada(s). Nenhuma restante.")
    elif remaining == 1:
        desc = f"{remaining} porta"
        if locked > 0:
            desc += f" ({locked} trancada)"
        print(f"   {desc} à frente.")
    else:
        desc = f"{remaining} portas"
        if locked > 0:
            desc += f" ({locked} trancada(s))"
        print(f"   {desc} à frente.")

    # Show door states
    for door in segment.doors:
        status = door.display_status()
        print(f"   {status} — Porta {door.index + 1}")


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
    dungeon_type_name = dungeon.type.name

    while True:
        current = graph.current_segment()
        if current is None:
            print("Erro: nenhum segmento atual.")
            return

        display_segment(current, graph)
        print()

        # Build action prompt
        actions = []
        for door in current.doors:
            if not door.is_open:
                actions.append(f"abrir {door.index + 1}")
            elif door.is_locked:
                actions.append(f"destrancar {door.index + 1}")
        actions.append("voltar")
        actions.append("sair")
        actions.append("salvar_e_sair")
        actions.append("ajuda")

        action_prompt = f"Ações: {', '.join(actions)}\n> "

        try:
            cmd = _prompt(action_prompt).strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if cmd == "ajuda":
            print("\nComandos disponíveis:")
            print("  abrir <N>        — Abre a porta N (rolagem d6)")
            print("  destrancar <N>   — Destranc porta N (consome 1 tocha)")
            print("  voltar           — Retorna ao segmento anterior")
            print("  sair             — Sai da masmorra (encerra exploração)")
            print("  salvar_e_sair    — Salva progresso e sai (pode retomar)")
            print("  status           — Mostra status do personagem")
            print("  ajuda            — Mostra esta ajuda")
            print("  q                — Sai do jogo")
            continue

        if cmd in ("q",):
            _handle_save_quit(pc, graph)
            return

        if cmd in ("sair",):
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

            door_idx = door_num - 1
            if door_idx < 0 or door_idx >= current.doors_count:
                print(
                    f"⚠️ Porta {door_num} não existe. Este segmento tem {current.doors_count} portas.",
                    file=sys.stderr,
                )
                continue

            _handle_open_door(pc, graph, door_idx, dungeon_type_name)

            # Check if we reached Final Room
            new_current = graph.current_segment()
            if new_current and new_current.is_final_room:
                display_segment(new_current, graph)
                print("\n🎉 Você completou a masmorra!")
                _deactivate_session()
                return

            continue

        if cmd.startswith("destrancar"):
            parts = cmd.split()
            if len(parts) < 2:
                print("⚠️ Use: destrancar <número da porta>", file=sys.stderr)
                continue
            try:
                door_num = int(parts[1])
            except ValueError:
                print("⚠️ Número da porta inválido.", file=sys.stderr)
                continue

            door_idx = door_num - 1
            _handle_unlock_door(pc, graph, door_idx)
            continue

        print("⚠️ Comando desconhecido. Digite 'ajuda' para ver as opções.", file=sys.stderr)


def _handle_open_door(pc, graph: DungeonGraph, door_idx: int, dungeon_type_name: str) -> None:
    """Handle opening a door with roll."""
    

    current = graph.current_segment()
    door = current.get_door(door_idx)

    # Already opened
    if door and door.is_open:
        target = graph.segments.get(door.target_segment_id)
        if target:
            t_name = _SEGMENT_NAMES.get(target.type, target.type.value)
            print(f"\n🚪 Porta {door_idx + 1} já foi aberta ({door.display_status()}). Ela leva a: {t_name} (Nível {target.level})")
            graph.set_current(target.id)
            display_segment(target, graph)
        return

    print(f"\n🚪 Você tenta abrir a porta {door_idx + 1}...")
    state, msg = open_door(graph, door_idx, dungeon_type_name)

    print(f"🎲 Rolagem: {msg}")

    if state == "trap":
        print(f"   ⚠️ Armadilha acionada! (placeholder)")
    elif state == "trancada":
        print(f"   🔒 A porta está trancada. Use 'destrancar {door_idx + 1}' para abrir.")
    else:
        target = graph.current_segment()
        if target:
            display_segment(target, graph)

    _save_session(graph)


def _handle_unlock_door(pc, graph: DungeonGraph, door_idx: int) -> None:
    """Handle unlocking a door, consuming torch."""
    success, msg = unlock_door(graph, door_idx, pc)
    print(f"\n{msg}")

    if success:
        target = graph.current_segment()
        if target:
            display_segment(target, graph)

        # Persist character
        _save_character(pc)
        _save_session(graph)


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
        _save_session(graph)


def _handle_exit(pc, graph: DungeonGraph) -> None:
    """Handle exiting the dungeon."""
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
            _deactivate_session()
            _save_character(pc)
            print("\n🏁 Você sai da masmorra com vida.")
            print(f"   Personagem {pc.name} salvo.")
            return

    print("Continuando a exploração...")


def _handle_save_quit(pc, graph: DungeonGraph) -> None:
    """Save current progress and quit, keeping session active for resume."""
    _save_session(graph)
    _save_character(pc)
    print("\n💾 Progresso salvo. Personagem permanece na masmorra.")
    print(f"   Execute 'notecli explore --resume' para continuar de onde parou.")
    print(f"   Segmento atual: {graph.current_segment_id}")
    print(f"   Tochas: {pc.torches} | HP: {pc.hp_current}/{pc.health_points}")


def _save_session(graph: DungeonGraph) -> None:
    """Persist current session state."""
    session_data = load_exploration()
    if session_data:
        session_data["segment_graph"] = graph.to_dict()
        from notecli.cli.storage import save_exploration as _save
        _save({"version": 1, "session": session_data})


def _save_character(pc) -> None:
    """Persist character state safely — never overwrite with empty list."""
    characters = load_characters()
    if not characters:
        return  # Safety guard: never save empty list
    for i, ch in enumerate(characters):
        if ch.get("name") == pc.name and ch.get("ancestry") == pc.ancestry:
            characters[i] = pc.to_dict()
            save_characters(characters)
            return
    # If character not found, don't save — avoid corrupting existing data


def _deactivate_session() -> None:
    """Deactivate the current exploration session."""
    session_data = load_exploration()
    if session_data:
        session_data["active"] = False
        from notecli.cli.storage import save_exploration as _save
        _save({"version": 1, "session": session_data})


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
                        from notecli.entities.dungeon import Dungeon
                        dungeon_data = session_data.get("dungeon", {})
                        dungeon_type = None
                        from notecli import tables
                        for dt in tables.DUNGEON_TYPES.values():
                            if dt.name == dungeon_data.get("type_name"):
                                dungeon_type = dt
                                break
                        dungeon = Dungeon(
                            type=dungeon_type,
                            name=dungeon_data.get("name", "Masmorra desconhecida"),
                        )
                        print(f"\n🗡️ {pc.ancestry} {pc.occupation} continua explorando...")
                        exploration_loop(pc, dungeon, graph)
                        return
                else:
                    clear_exploration()
                    print("Personagem não encontrado. Iniciando nova exploração...")
            else:
                clear_exploration()
                print("Sessão corrompida. Iniciando nova exploração...")
        else:
            clear_exploration()

    # If not resuming, check for active session and prompt
    if not resume:
        session_data = load_exploration()
        if session_data and session_data.get("active"):
            try:
                choice = _prompt("\n🔄 Sessão ativa encontrada. Retomar? (r/n) > ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print()
                return

            if choice == "r":
                graph = None
                if "segment_graph" in session_data:
                    graph = DungeonGraph.from_dict(session_data["segment_graph"])

                if graph and graph.current_segment():
                    from notecli.entities.player import PlayerCharacter
                    from notecli.entities.dungeon import Dungeon
                    characters = load_characters()
                    if 0 < session_data["character_index"] <= len(characters):
                        pc = PlayerCharacter.from_dict(characters[session_data["character_index"] - 1])
                        # Reconstruct dungeon from session data
                        dungeon_data = session_data.get("dungeon", {})
                        dungeon_type = None
                        from notecli import tables
                        for dt in tables.DUNGEON_TYPES.values():
                            if dt.name == dungeon_data.get("type_name"):
                                dungeon_type = dt
                                break
                        dungeon = Dungeon(
                            type=dungeon_type,
                            name=dungeon_data.get("name", "Masmorra desconhecida"),
                        )
                        print(f"\n🗡️ {pc.ancestry} {pc.occupation} continua explorando...")
                        exploration_loop(pc, dungeon, graph)
                        return

                clear_exploration()
                print("Erro ao retomar sessão. Iniciando nova exploração...")
            elif choice == "n":
                clear_exploration()
                print("Iniciando nova exploração...")
            else:
                clear_exploration()
                print("Opção inválida. Iniciando nova exploração...")

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

    # Generate FULL dungeon before exploration
    graph = DungeonGraph()
    generate_full_dungeon(graph, dungeon.type.name)

    # Set current to initial segment
    initial_id = 0
    graph.set_current(initial_id)

    # Display initial segment
    print("\n" + "=" * 40)
    initial = graph.current_segment()
    if initial:
        display_segment(initial, graph)

    # Find character index
    characters = load_characters()
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
