import csv
import datetime

class Database:
    """Class for managing game data storage and retrieval.

    This class provides methods to save game data to a CSV file and retrieve
    the next game ID for new entries.
    """
    @staticmethod
    def get_next_id():
        """Calculates the number of games recorded in the game_data.csv file and returns the number + 1.

        Reads the existing game data from 'data/game_data.csv' and returns the next available game ID.
        If the file does not exist, it returns 1.

        Returns:
            int: The number of games recorded in the game_data.csv file plus one.
        """
        try:
            with open('data/game_data.csv', 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                return len(rows) + 1
        except FileNotFoundError:
            return 1

    @staticmethod
    def save_new_game(player_who_starts:int, winner:int, shots_played_player:int, shots_played_ia:int, shots):
        """Saves a game to the game_data.csv file.

        Appends a new game record to 'Data/game_data.csv' with the following details:
        - Game ID
        - Current date and time
        - Starting player (1 for human, -1 for AI)
        - Winner (1 for human, -1 for AI)
        - Number of moves played by the human player
        - Number of moves played by the AI
        - List of moves played during the game

        Args:
            player_who_starts (int): -1 when the AI starts and 1 when the player starts.
            winner (int): -1 when the AI wins and 1 when the player wins.
            shots_played_player (int): Number of moves the player has played.
            shots_played_ia (int): Number of moves the AI has played.
            shots (list): List containing the positions of the moves played in the order of the game.
        """
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        get_next_id = Database.get_next_id()

        with open('Data/game_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([get_next_id, current_date, player_who_starts, winner, shots_played_player, shots_played_ia, shots])
