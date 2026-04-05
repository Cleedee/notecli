"""Interactive character menu CLI."""

import sys
from typing import Callable

from notecli.cli.storage import load_characters, save_characters
from notecli.entities.player import PlayerCharacter
from notecli import tables
from notecli.dice import Roller


def _prompt(prompt_text: str) -> str:
    """Read user input with a prompt, returning stripped text."""
    return input(prompt_text).strip()


def show_menu() -> None:
    """Display the main character menu and process user choices."""
    while True:
        print("\n=== Menu de Personagens ===")
        print("1) personagens")
        print("2) novo personagem")
        print("0) sair")

        try:
            choice = _prompt("> ")
        except (KeyboardInterrupt, EOFError):
            print()
            handle_exit()
            return

        if choice in ("0", "q"):
            handle_exit()
            return
        elif choice == "1":
            _handle_view_characters()
        elif choice == "2":
            _handle_create_character()
        else:
            handle_invalid_input()


def handle_invalid_input() -> None:
    """Display error message for invalid menu choice."""
    print("Opção inválida. Escolha 1, 2 ou 0/q para sair.", file=sys.stderr)


def handle_exit() -> None:
    """Clean exit from the menu."""
    print("Saindo...")
    sys.exit(0)


def _handle_view_characters() -> None:
    """Handle option 1: display character list and optionally show details."""
    characters = load_characters()
    if not characters:
        print("Nenhum personagem encontrado. Crie um novo personagem.")
        return

    print("\n=== Personagens Salvos ===")
    list_characters(characters)

    # Prompt for detail view or back
    try:
        choice = _prompt("Número do personagem para detalhes (ou 0 para voltar): ")
    except (KeyboardInterrupt, EOFError):
        print()
        return

    if choice == "0":
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(characters):
            from notecli.entities.player import PlayerCharacter
            pc = PlayerCharacter.from_dict(characters[idx])
            show_character_detail(pc, idx + 1)
        else:
            print("Número inválido.", file=sys.stderr)
    except (ValueError, KeyError) as e:
        print(f"Erro ao carregar personagem: {e}", file=sys.stderr)


def _handle_create_character() -> None:
    """Handle option 2: create new character and optionally loop."""
    while True:
        pc = create_character()
        show_creation_summary(pc)
        try:
            again = _prompt("Criar outro personagem? (s/n) > ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            return
        if again != "s":
            return


def create_character() -> PlayerCharacter:
    """Create a new character with randomized ancestry and profession.

    Returns:
        The newly created PlayerCharacter, already saved to storage.
    """
    # Roll ancestry
    ancestry_roll = Roller.roll_2d6()
    ancestry = tables.ANCESTRIES[ancestry_roll]
    print(f"🎲 Rolando ancestralidade... 2d6 = {ancestry_roll} → {ancestry.name} ({ancestry.health_points} HP)")

    # Roll profession
    prof_roll = Roller.roll_2d6()
    occupation = tables.OCCUPATIONS[prof_roll]
    print(f"🎲 Rolando profissão... 2d6 = {prof_roll} → {occupation.name} (+{occupation.additional_hit_points} HP, {occupation.starting_weapon})")

    # Create character
    pc = PlayerCharacter(
        name=ancestry.name[:4].title(),  # Auto-generated short name
        occupation=occupation.name,
        torches=10,
        health_points=ancestry.health_points + occupation.additional_hit_points,
        hp_current=ancestry.health_points + occupation.additional_hit_points,
        ancestry=ancestry.name,
        starting_weapon=occupation.starting_weapon,
    )

    # Apply ancestry-specific effects (magics, etc.)
    ancestry.apply(pc)

    # Ensure HP reflects ancestry base + occupation bonus after apply
    pc.health_points = ancestry.health_points + occupation.additional_hit_points
    if pc.hp_current < pc.health_points:
        pc.hp_current = pc.health_points

    # Save to storage
    characters = load_characters()
    characters.append(pc.to_dict())
    save_characters(characters)

    print(f"\n⚔️ Novo personagem criado!")
    return pc


def show_creation_summary(pc: PlayerCharacter) -> None:
    """Display a summary of the newly created character."""
    print(f"  Nome: {pc.name}")
    print(f"  Ancestralidade: {pc.ancestry}")
    print(f"  Profissão: {pc.occupation}")
    print(f"  HP: {pc.hp_current}/{pc.health_points}")
    print(f"  Arma inicial: {pc.starting_weapon}")
    print(f"  Tochas: {pc.torches}")
    if pc.magics:
        magic_names = ", ".join(m["name"] for m in pc.magics)
        print(f"  Magias: {magic_names}")


def list_characters(characters: list) -> None:
    """Display a numbered list of characters with summary info."""
    if not characters:
        print("  Nenhum personagem encontrado.")
        return

    for i, ch in enumerate(characters, 1):
        status = "vivo" if ch.get("alive", True) else "morto"
        hp = f"{ch['hp_current']}/{ch['health_points']}"
        name = ch.get("name", "Sem nome")
        ancestry = ch.get("ancestry", "?")
        occupation = ch.get("occupation", "?")
        print(f"  {i}) {ancestry} {occupation} — HP: {hp} — {status} ({name})")


def show_character_detail(pc, number: int) -> None:
    """Display full details of a single character."""
    print(f"\n=== Personagem {number}: {pc.name} ===")
    print(f"  Ancestralidade: {pc.ancestry}")
    print(f"  Profissão: {pc.occupation}")
    print(f"  HP: {pc.hp_current}/{pc.health_points}")
    print(f"  Tochas: {pc.torches}")
    print(f"  Arma inicial: {pc.starting_weapon}")
    print(f"  Estado: {'vivo 🔥' if pc.is_alive() else 'morto 💀'}")
    if pc.magics:
        print("  Magias:")
        for m in pc.magics:
            print(f"    - {m['name']} ({m['uses']} usos)")
    else:
        print("  Magias: nenhuma")
