class Utils:
    """
        Checks the game board for a winning condition.

        Returns:
                int: 1 if the human player wins, -1 if the AI wins, 0 if no winner yet.
        """
    @staticmethod
    def get_player_to_win(plateau):
        for line in range(6):
            for column in range(7):
                if plateau[line][column] != 0:
                    if column + 3 < 7 and all(
                            plateau[line][column + i] == plateau[line][column] for i in range(4)):
                        return plateau[line][column]

                    if line + 3 < 6 and all(
                            plateau[line + i][column] == plateau[line][column] for i in range(4)):
                        return plateau[line][column]

                    if line + 3 < 6 and column + 3 < 7 and all(
                            plateau[line + i][column + i] == plateau[line][column] for i in range(4)):
                        return plateau[line][column]

                    if line - 3 >= 0 and column + 3 < 7 and all(
                            plateau[line - i][column + i] == plateau[line][column] for i in range(4)):
                        return plateau[line][column]
        return 0