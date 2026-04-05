"""Interactive dungeon exploration menu CLI."""

import sys
from datetime import datetime
from typing import Optional

from notecli.dice import Roller
from notecli.entities.dungeon import generate_dungeon, Dungeon, ExplorationSession
from notecli.cli.storage import (
    load_characters,
    save_exploration,
    load_exploration,
    clear_exploration,
)


def _prompt(prompt_text: str) -> str:
    """Read user input with a prompt, returning stripped text."""
    return input(prompt_text).strip()


def display_dungeon_info(dungeon: Dungeon) -> None:
    """Display dungeon type, name, and entrance description.

    Args:
        dungeon: The dungeon to display.
    """
    print(f"\n🏰 Gerando masmorra...")
    print(f"  Tipo: {dungeon.type.name}")
    print(f"  Nome: {dungeon.name}")
    print(f"\n📖 Você chega à entrada de {dungeon.name}.")
    print(f"   {dungeon.type.entrance_description}")


def select_or_create_character() -> Optional["PlayerCharacter"]:
    """Let the player select an existing character or create a new one.

    Returns:
        The selected or created PlayerCharacter, or None if user quits.
    """
    # Import here to avoid circular dependency
    from notecli.cli.storage import load_characters
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


def _create_character() -> Optional["PlayerCharacter"]:
    """Create a new character using the character menu flow.

    Returns:
        The newly created PlayerCharacter, or None on error.
    """
    from notecli.cli.character_menu import (
        create_character as menu_create_character,
    )

    try:
        pc = menu_create_character()
        return pc
    except Exception as e:
        print(f"⚠️ Erro ao criar personagem: {e}", file=sys.stderr)
        return None


def start_new_session(
    dungeon: Dungeon, character_index: int
) -> ExplorationSession:
    """Start a new exploration session.

    Args:
        dungeon: The generated dungeon.
        character_index: 1-based index of the selected character.

    Returns:
        The new ExplorationSession.
    """
    session = ExplorationSession(
        dungeon=dungeon,
        character_index=character_index,
        started_at=datetime.now().isoformat(),
        active=True,
    )
    save_exploration(session.to_dict())
    return session


def resume_session() -> Optional[ExplorationSession]:
    """Resume an active exploration session if one exists.

    Returns:
        The resumed ExplorationSession, or None if no active session.
    """
    session_data = load_exploration()
    if session_data is None:
        return None

    session = ExplorationSession.from_dict(session_data)
    return session


def show_character_status(pc: "PlayerCharacter") -> None:
    """Display character status line after selection.

    Args:
        pc: The selected PlayerCharacter.
    """
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


def explore(resume: bool = False) -> None:
    """Main exploration entry point.

    Generates a dungeon, shows info, selects/creates a character,
    and starts (or resumes) the exploration session.

    Args:
        resume: If True, try to resume an existing session first.
    """
    # Try to resume if requested
    if resume:
        session = resume_session()
        if session:
            print("\n🔄 Sessão de exploração encontrada:")
            print(f"   Masmorra: {session.dungeon.name}")
            print(f"   Salas visitadas: {session.dungeon.rooms_visited}")

            try:
                choice = _prompt("Continuar desta sessão? (s/n) > ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print()
                return

            if choice == "s":
                # Load the character
                from notecli.entities.player import PlayerCharacter
                characters = load_characters()
                if 0 < session.character_index <= len(characters):
                    pc = PlayerCharacter.from_dict(
                        characters[session.character_index - 1]
                    )
                    print(
                        f"\n🗡️ {pc.ancestry} {pc.occupation} continua explorando {session.dungeon.name}..."
                    )
                    print(
                        f"   Tochas: {pc.torches} | HP: {pc.hp_current}/{pc.health_points}"
                    )
                    return
            else:
                clear_exploration()
                print("Iniciando nova exploração...")

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

    # Start session
    # Find character index
    characters = load_characters()
    char_index = 0
    for i, ch in enumerate(characters, 1):
        if ch.get("name") == pc.name and ch.get("ancestry") == pc.ancestry:
            char_index = i
            break

    if char_index == 0:
        # Character was just created, it should be the last one
        char_index = len(characters)

    start_new_session(dungeon, char_index)

    # Show status
    show_character_status(pc)
    print("\nDigite 'ajuda' para ver as ações disponíveis.")
