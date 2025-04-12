import ast
import csv
import datetime
import os

import pandas as pd

from Game.Utils import Utils


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
            df = pd.read_csv('data/game_data.csv')
            print(len(df))
            return len(df) + 1
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

        new_game_data = {
            "id": [get_next_id],
            "date": [current_date],
            "player_who_starts": [player_who_starts],
            "winner": [winner],
            "shots_played_player": [shots_played_player],
            "shots_played_ia": [shots_played_ia],
            "shots": [shots]
        }

        df_new_game = pd.DataFrame(new_game_data)

        file_exists = os.path.isfile('data/game_data.csv')

        # Append to the existing CSV file
        df_new_game.to_csv('data/game_data.csv', mode='a', header=not file_exists, index=False)

    @staticmethod
    def evaluate_moves_from_history(current_shots, player_turn):
        """Evaluates moves based on historical game data.

        Args:
            current_shots (list): The list of shots played in the current game.
            player_turn (int): The current player's turn (1 for human, -1 for AI).

        Returns:
            dict: A dictionary with suggested moves and their scores based on historical data.
        """
        points_config = Utils.load_points_config()
        move_scores = {}

        # Load historical game data
        try:
            df = pd.read_csv('data/game_data.csv')
            for index, row in df.iterrows():
                winner = row['winner']
                shots = eval(row['shots']) # Convert string representation of list to actual list

                # Check if the current game matches the start of a historical game
                if shots[:len(current_shots)] == current_shots:
                    # Evaluate the next move in the historical game
                    next_move = shots[len(current_shots)]
                    if next_move not in move_scores:
                        move_scores[next_move] = 0

                    # Adjust score based on the outcome of the historical game
                    if winner == player_turn:
                        move_scores[next_move] += points_config["historical_win_score"]
                    elif winner == -player_turn:
                        move_scores[next_move] -= points_config["historical_loss_score"]

        except FileNotFoundError:
            print("No historical game data found.")

        return move_scores
