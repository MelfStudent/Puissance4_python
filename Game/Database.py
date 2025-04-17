import datetime
import os
import pandas as pd

from Game.Utils import Utils

class Database:
    """Class for managing game data storage and retrieval

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
            Database._validate_columns(df)
            return len(df) + 1
        except FileNotFoundError:
            return 1
        except (pd.errors.EmptyDataError, ValueError):
            Database._recreate_csv_with_columns()
            return 1

    @staticmethod
    def save_new_game(player_who_starts:int, winner:int, shots_played_player:int, shots_played_ia:int, shots):
        """Saves a game to the game_data.csv file

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
        """Evaluates moves based on historical game data

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
            Database._validate_columns(df)
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
        except (pd.errors.EmptyDataError, ValueError):
            Database._recreate_csv_with_columns()

        return move_scores

    @staticmethod
    def _validate_columns(df):
        """Validates that the DataFrame contains the required columns
        """
        required_columns = {"id", "date", "player_who_starts", "winner", "shots_played_player", "shots_played_ia", "shots"}
        if not required_columns.issubset(df.columns):
            raise ValueError("CSV file does not contain the required columns.")

    @staticmethod
    def _recreate_csv_with_columns():
        """Recreates the CSV file with the required columns
        """
        empty_df = pd.DataFrame(columns=["id", "date", "player_who_starts", "winner", "shots_played_player", "shots_played_ia", "shots"])
        empty_df.to_csv('data/game_data.csv', index=False)

    @staticmethod
    def export_dataframe(df: pd.DataFrame, filename: str = "exported_game_data.csv"):
        """Exports a DataFrame to a CSV file

        Args:
            df (pd.DataFrame): The DataFrame to export.
            filename (str): The name of the file to export to. Defaults to "exported_game_data.csv".
        """
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
        """Selects specific columns from a DataFrame

        Args:
            df (pd.DataFrame): The DataFrame from which to select columns.

        Returns:
            pd.DataFrame: A DataFrame containing only the selected columns.
        """
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
        """Filters game data based on user-defined criteria.

        Returns:
            pd.DataFrame: The filtered DataFrame.
        """
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
            Database._validate_columns(df)

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
        except (pd.errors.EmptyDataError, ValueError):
            Database._recreate_csv_with_columns()
            return None

    @staticmethod
    def sort_game_data(df: pd.DataFrame) -> pd.DataFrame:
        """Sorts the game data based on user-defined criteria

        Args:
            df (pd.DataFrame): The DataFrame to sort.

        Returns:
            pd.DataFrame: The sorted DataFrame.
        """
        print("\nDo you want to sort the data?")
        print("1. Yes")
        print("2. No")
        sort_choice = input("Your choice: ").strip()

        if sort_choice == "1":
            print("\nChoose the column to sort by:")
            for idx, col in enumerate(df.columns, 1):
                if col != "shots":
                    print(f"{idx}. {col}")

            column_choice = input("Your choice: ").strip()
            try:
                column_index = int(column_choice) - 1
                if column_index < 0 or column_index >= len(df.columns):
                    raise ValueError
                column_name = df.columns[column_index]

                if column_name == "shots":
                    print("Sorting by 'shots' is not allowed.")
                    return df

                print("\nChoose the sort order:")
                print("1. Ascending")
                print("2. Descending")
                order_choice = input("Your choice: ").strip()

                if order_choice == "1":
                    return df.sort_values(by=column_name, ascending=True)
                elif order_choice == "2":
                    return df.sort_values(by=column_name, ascending=False)
                else:
                    print("Invalid choice. No sorting applied.")
            except (ValueError, IndexError):
                print("Invalid input. No sorting applied.")

        return df

    @staticmethod
    def delete_filtered_data():
        """Deletes filtered game data
        """
        df = Database.apply_filters()
        if Database.display_data_to_delete(df):
            confirm = input("\nAre you sure you want to delete these records? (yes/no): ").strip().lower()
            if confirm == "yes":
                Database.delete_and_update_indices(df)
            else:
                print("Deletion canceled.")

    @staticmethod
    def delete_and_update_indices(df):
        """Deletes specified records and updates the indices in the CSV file

        Args:
            df (pd.DataFrame): The DataFrame containing the records to delete.
        """
        original_df = pd.read_csv("data/game_data.csv")
        original_df = original_df[~original_df.index.isin(df.index)]

        original_df = original_df.reset_index(drop=True)
        original_df["id"] = original_df.index + 1

        original_df.to_csv("data/game_data.csv", index=False)
        print("Data deleted successfully and indices updated.")

    @staticmethod
    def display_data_to_delete(df):
        """Displays the data to be deleted and confirms the deletion

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be deleted.

        Returns:
            bool: True if the data matches the filters and the user confirms the deletion, False otherwise.
        """
        if df is None or df.empty:
            print("No data matches the filters. Nothing to delete.")
            return False

        print("\nData to be deleted:")
        print(df.to_string(index=False))
        return True

    @staticmethod
    def apply_filters():
        """Applies filters to the game data for deletion.

        Returns:
            pd.DataFrame: The filtered DataFrame.
        """
        print("\n-- Apply Filters to Delete Data --")

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
            Database._validate_columns(df)

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
        except (pd.errors.EmptyDataError, ValueError):
            Database._recreate_csv_with_columns()
            return None
