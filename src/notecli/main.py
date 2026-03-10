import sys

def main():
    print("⚔️  Bem-vindo ao NoteCLI! ⚔️")
    print("---")
                
    args = sys.argv[1:]
    if "explore" in args:
        print("Você entra na masmorra e saca sua espada...")
    else:
        print("Use 'notecli explore' para começar sua jornada.")

if __name__ == "__main__":
    main()

