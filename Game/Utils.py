import json

class Utils:
    """Utility class

    This class contains static methods to check the game board for winning conditions.
    """
    @staticmethod
    def get_player_to_win(plateau):
        """Checks the game board for a winning condition

        Iterates through the game board to check for any winning conditions.
        A player wins if they have four consecutive tokens in a row horizontally,
        vertically, or diagonally.

        Args:
            plateau (np.array): The 6x7 array representing the game board.

        Returns:
            int: 1 if the human player wins, -1 if the AI wins, 0 if no winner yet.
        """
        for line in range(6):
            for column in range(7):
                if plateau[line][column] != 0:
                    # Check horizontal win
                    if column + 3 < 7 and all(
                            plateau[line][column + i] == plateau[line][column] for i in range(4)):
                        return plateau[line][column]

                    # Check vertical win
                    if line + 3 < 6 and all(
                            plateau[line + i][column] == plateau[line][column] for i in range(4)):
                        return plateau[line][column]

                    # Check diagonal (descending) win
                    if line + 3 < 6 and column + 3 < 7 and all(
                            plateau[line + i][column + i] == plateau[line][column] for i in range(4)):
                        return plateau[line][column]

                    # Check diagonal (ascending) win
                    if line - 3 >= 0 and column + 3 < 7 and all(
                            plateau[line - i][column + i] == plateau[line][column] for i in range(4)):
                        return plateau[line][column]
        return 0

    @staticmethod
    def load_points_config():
        """Load the points configuration from a JSON file
        """
        with open('config/points_config.json', 'r') as json_file:
            return json.load(json_file)
