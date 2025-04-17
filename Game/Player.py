class Player:
    """Class representing the human player

    This class provides a method for the human player to choose a column
    to place their token on the game board.
    """
    @staticmethod
    def player_choice(plateau):
        """Asks the player to choose a column to place their token in, then adds the token to the game board

        Prompts the player to enter a column number between 1 and 7. If the column is valid and not full,
        the player's token is placed in the lowest available row of the chosen column.

        Args:
            plateau (Plateau): The game board instance containing the positions of the moves played.
        """
        while True:
            try:
                column = int(input("Choose a column (1-7): ")) - 1

                if column < 0 or column > 6:
                    print("Error: Please enter a number between 1 and 7.")
                elif plateau.plateau[0][column] != 0:
                    print("Error: This column is full. Choose another column.")
                else:
                    for row in range(5, -1, -1):
                        if plateau.plateau[row][column] == 0:
                            plateau.plateau[row][column] = 1
                            plateau.shots.append((row, column))
                            plateau.shots_played_player += 1
                            return
            except ValueError:
                print("Error: Please enter a valid number.")
