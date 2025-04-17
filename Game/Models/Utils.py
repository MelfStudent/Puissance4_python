import json
import numpy as np

class Utils:
    """Utility class

    This class contains static methods to check the game board for winning conditions.
    """
    @staticmethod
    def get_player_to_win(plateau: np.array) -> int:
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
                current_token = plateau[line][column]
                if current_token != 0:
                    # Check horizontal win
                    if column + 3 < 7 and all(
                            plateau[line][column + i] == current_token for i in range(4)):
                        return current_token

                    # Check vertical win
                    if line + 3 < 6 and all(
                            plateau[line + i][column] == current_token for i in range(4)):
                        return current_token

                    # Check diagonal (descending) win
                    if line + 3 < 6 and column + 3 < 7 and all(
                            plateau[line + i][column + i] == current_token for i in range(4)):
                        return current_token

                    # Check diagonal (ascending) win
                    if line - 3 >= 0 and column + 3 < 7 and all(
                            plateau[line - i][column + i] == current_token for i in range(4)):
                        return current_token
        return 0

    @staticmethod
    def load_points_config() -> dict:
        """Load the points configuration from a JSON file

        Returns:
            dict: The points configuration loaded from the JSON file.
        """
        try:
            with open('../config/points_config.json', 'r') as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            print("Error: points_config.json file not found.")
            return {}
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from points_config.json.")
            return {}
