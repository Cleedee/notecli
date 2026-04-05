import sys

from notecli.cli.character_menu import show_menu


def main():
    print("⚔️  Bem-vindo ao NoteCLI! ⚔️")
    print("---")

    args = sys.argv[1:]
    if len(args) > 0 and args[0] == "character":
        show_menu()
    elif "explore" in args:
        print("Você entra na masmorra e saca sua espada...")
    else:
        print("Use 'notecli character' para gerenciar personagens.")
        print("Use 'notecli explore' para começar sua jornada.")

if __name__ == "__main__":
    main()

