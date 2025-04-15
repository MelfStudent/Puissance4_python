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

    @staticmethod
    def export_dataframe(df: pd.DataFrame, filename: str = "exported_game_data.csv"):
        if df is None or df.empty:
            print("No data to export.")
            return

        downloads_dir = os.path.expanduser("~/Downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        if not filename.endswith(".csv"):
            filename += ".csv"

        base_name, ext = os.path.splitext(filename)
        final_path = os.path.join(downloads_dir, filename)

        counter = 1
        while os.path.exists(final_path):
            final_path = os.path.join(downloads_dir, f"{base_name}_{counter:02d}{ext}")
            counter += 1

        try:
            df.to_csv(final_path, index=False)
            print(f"Data exported to: {final_path}")
        except Exception as e:
            print(f"Failed to export data: {e}")

    @staticmethod
    def select_columns(df: pd.DataFrame) -> pd.DataFrame:
        print("\nChoose columns to include (comma-separated):")
        for idx, col in enumerate(df.columns, 1):
            print(f"{idx}. {col}")

        selection = input("Your choice (e.g. 1,3,5): ").strip()
        if not selection:
            return df

        try:
            selected_indices = [int(i) - 1 for i in selection.split(",")]
            selected_columns = [df.columns[i] for i in selected_indices if 0 <= i < len(df.columns)]
            return df[selected_columns]
        except (ValueError, IndexError):
            print("Invalid input. Showing all columns.")
            return df

    @staticmethod
    def filter_game_data():
        print("\n-- Apply Filters --")

        date_start = input("Start date (YYYY-MM-DD) or press Enter to skip: ").strip()
        date_end = input("End date (YYYY-MM-DD) or press Enter to skip: ").strip()

        print("Filter by who started the game?")
        print("1. Player")
        print("2. IA")
        print("3. No filter")
        starter_choice = input("Your choice: ").strip()

        print("Filter by result?")
        print("1. Player victory")
        print("2. IA victory")
        print("3. No filter")
        result_choice = input("Your choice: ").strip()

        try:
            df = pd.read_csv("data/game_data.csv", parse_dates=["date"])

            if date_start:
                df = df[df["date"] >= pd.to_datetime(date_start)]
            if date_end:
                df = df[df["date"] <= pd.to_datetime(date_end)]

            if starter_choice == "1":
                df = df[df["player_who_starts"] == 1]
            elif starter_choice == "2":
                df = df[df["player_who_starts"] == -1]

            if result_choice == "1":
                df = df[df["winner"] == 1]
            elif result_choice == "2":
                df = df[df["winner"] == -1]

            return df

        except FileNotFoundError:
            print("No game data found.")
            return None
