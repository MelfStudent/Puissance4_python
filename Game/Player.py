class Player:
    """
    Asks the player to choose a column to place their token in, then the token is added to the game board

    Parameters:
        array: plateau | table containing the positions of the moves played such as (5, 1)
    """
    @staticmethod
    def player_choice(plateau):
        while True:
            try:
                column = int(input("Choisissez une colonne (1-7) : ")) - 1

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
