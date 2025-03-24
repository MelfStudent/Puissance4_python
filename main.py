from Game.Plateau import Plateau

def main():
    try:
        plateau = Plateau()
        plateau.start_game()
    except KeyboardInterrupt:
        print("\n-----------------------------")
        print("Manual interruption detected!")
        print("-----------------------------")

if __name__ == "__main__":
    main()
