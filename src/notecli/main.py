import sys

from notecli.cli.character_menu import show_menu
from notecli.cli.explore_menu import explore


def main():
    print("⚔️  Bem-vindo ao NoteCLI! ⚔️")
    print("---")

    args = sys.argv[1:]
    if len(args) > 0 and args[0] == "character":
        show_menu()
    elif "explore" in args:
        resume = "--resume" in args
        explore(resume=resume)
    else:
        print("Use 'notecli character' para gerenciar personagens.")
        print("Use 'notecli explore' para começar sua jornada.")

if __name__ == "__main__":
    main()

