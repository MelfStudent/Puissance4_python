from Game.Plateau import Plateau

def main():
    """Main function to start.

    Initializes the game board and starts the game loop. Handles manual interruptions
    gracefully by catching KeyboardInterrupt exceptions.
    """
    try:
        plateau = Plateau()
        plateau.start_game()
    except KeyboardInterrupt:
        # Handle manual interruption (e.g., user pressing Ctrl+C)
        print("\n-----------------------------")
        print("Manual interruption detected!")
        print("-----------------------------")

if __name__ == "__main__":
    """Entry point of the script.

    Ensures that the main function is called only when the script is executed directly,
    not when it is imported as a module.
    """
    main()
