import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import ast
from collections import Counter

import pandas as pd

from .Database import Database

class Graphics:
    """Class for generating various graphs based on game data
    """
    @staticmethod
    def plot_overview():
        """Plot an overview of the game results (Player wins, AI wins, Draws)
        """
        df = Database.load_game_data()
        if df.empty:
            return

        total_games = len(df)
        player_wins = df[df['winner'] == 1].shape[0]
        ia_wins = df[df['winner'] == -1].shape[0]
        draws = total_games - player_wins - ia_wins

        labels = ['Player Wins', 'IA Wins', 'Draws']
        sizes = [player_wins, ia_wins, draws]
        colors = ['yellow', 'red', 'lightblue']
        explode = (0.1, 0.1, 0)

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.title('Overview of Game Results')
        plt.show()

    @staticmethod
    def plot_trend_dispersion():
        """Plot trend and dispersion measures (mean, median, standard deviation of moves)
        """
        df = Database.load_game_data()
        if df.empty:
            return

        # Calculate total moves (shots played by player + shots played by AI)
        df['total_moves'] = df['shots_played_player'] + df['shots_played_ia']
        mean_moves = df['total_moves'].mean()
        median_moves = df['total_moves'].median()
        std_moves = df['total_moves'].std()

        # Boxplot with mean and median
        plt.figure(figsize=(10, 6))
        plt.boxplot(df['total_moves'], vert=False, patch_artist=True, boxprops=dict(facecolor="lightblue"))
        plt.axvline(mean_moves, color='r', linestyle='--', label=f'Mean: {mean_moves:.2f}')
        plt.axvline(median_moves, color='g', linestyle='-', label=f'Median: {median_moves:.2f}')
        plt.text(mean_moves, 1.1, f'Std: {std_moves:.2f}', color='b')
        plt.xlabel('Number of Moves')
        plt.title('Trend and Dispersion Measures')
        plt.legend()
        plt.show()

    @staticmethod
    def plot_wins_by_first_player():
        """Plot the number of victories depending on who starts the game (Player or AI)
        """
        df = Database.load_game_data()
        if df.empty:
            return

        # Filter data based on who started the game (player or AI)
        player_starts = df[df['player_who_starts'] == 1]
        ai_starts = df[df['player_who_starts'] == -1]

        # Count the number of wins for each case
        player_starts_player_wins = player_starts[player_starts['winner'] == 1].shape[0]
        ai_starts_ai_wins = ai_starts[ai_starts['winner'] == -1].shape[0]

        labels = ['Player starts', 'AI starts']
        wins = [player_starts_player_wins, ai_starts_ai_wins]

        # Bar chart representation
        fig, ax = plt.subplots()
        ax.bar(labels, wins, color=['blue', 'red'])
        ax.set_ylabel('Number of victories')
        ax.set_title('Victories depending on who starts')
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.show()

    @staticmethod
    def plot_column_play_counts():
        """Plot the frequency of moves per column (1 to 7)
        """
        df = Database.load_game_data()
        if df.empty:
            return

        all_columns = []

        # Iterate through all shots and extract the column numbers
        for shot in df['shots']:
            try:
                parsed_shots = ast.literal_eval(shot)
                if isinstance(parsed_shots, list):
                    for (_, col) in parsed_shots:
                        all_columns.append(col +1)
            except:
                continue

        # Count the frequency of each column
        counts = Counter(all_columns)

        # Create the list of columns (1 to 7)
        columns = list(range(1, 8))
        frequencies = [counts.get(c, 0) for c in columns]

        fig, ax = plt.subplots()
        ax.bar(columns, frequencies, color='orange')
        ax.set_xlabel('Column (1 to 7)')
        ax.set_ylabel('Number of times played')
        ax.set_title('Frequency of play per column (all moves)')
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        plt.show()

    @staticmethod
    def plot_games_per_month():
        """Plot the number of games played per month
        """
        df = Database.load_game_data()
        if df.empty:
            return

        # Convert the date column to datetime format
        df['date'] = pd.to_datetime(df['date'])

        # Extract the month period (year-month)
        df['month'] = df['date'].dt.to_period('M')

        # Count the number of games per month
        games_per_month = df['month'].value_counts().sort_index()

        months = [str(m) for m in games_per_month.index]
        counts = games_per_month.values

        fig, ax = plt.subplots()
        ax.bar(months, counts, color='mediumseagreen')
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of games')
        ax.set_title('Number of games played per month')
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_shots_frequency_per_game():
        """Plot the frequency of shots (total moves) per game
        """
        df = Database.load_game_data()
        if df.empty:
            return

        # Parse the shots column (from string to list of tuples)
        df['parsed_shots'] = df['shots'].apply(ast.literal_eval)

        # Calculate the total number of shots per game
        df['total_shots'] = df['parsed_shots'].apply(len)

        # Count the frequency of each total number of shots
        shot_counts = df['total_shots'].value_counts().sort_index()

        fig, ax = plt.subplots()
        ax.bar(shot_counts.index, shot_counts.values, color='cornflowerblue')
        ax.set_xlabel("Total number of moves in the game")
        ax.set_ylabel("Number of games")
        ax.set_title("Frequency of shots played per game")
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.tight_layout()
        plt.show()
