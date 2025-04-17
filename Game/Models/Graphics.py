import matplotlib.pyplot as plt
import pandas as pd

class Graphics:
    """Class for generating various graphs based on game data
    """

    @staticmethod
    def load_game_data():
        """Loads game data from the CSV file

        Returns:
            pd.DataFrame: A DataFrame containing the game data.
        """
        try:
            return pd.read_csv('../data/game_data.csv')
        except FileNotFoundError:
            print("No game data found.")
            return pd.DataFrame()

    @staticmethod
    def plot_overview():
        """Plot an overview of the game results
        """
        df = Graphics.load_game_data()
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
    def plot_frequency_moves():
        """Plot the frequency of moves per game
        """
        df = Graphics.load_game_data()
        if df.empty:
            return

        df['total_moves'] = df['shots_played_player'] + df['shots_played_ia']

        plt.figure(figsize=(10, 6))
        plt.hist(df['total_moves'], bins=10, color='purple', edgecolor='black')
        plt.xlabel('Number of Moves')
        plt.ylabel('Frequency')
        plt.title('Frequency of Moves per Game')
        plt.show()

    @staticmethod
    def plot_trend_dispersion():
        """Plot trend and dispersion measures
        """
        df = Graphics.load_game_data()
        if df.empty:
            return

        df['total_moves'] = df['shots_played_player'] + df['shots_played_ia']
        mean_moves = df['total_moves'].mean()
        median_moves = df['total_moves'].median()
        std_moves = df['total_moves'].std()

        plt.figure(figsize=(10, 6))
        plt.boxplot(df['total_moves'], vert=False, patch_artist=True, boxprops=dict(facecolor="lightblue"))
        plt.axvline(mean_moves, color='r', linestyle='--', label=f'Mean: {mean_moves:.2f}')
        plt.axvline(median_moves, color='g', linestyle='-', label=f'Median: {median_moves:.2f}')
        plt.text(mean_moves, 1.1, f'Std: {std_moves:.2f}', color='b')
        plt.xlabel('Number of Moves')
        plt.title('Trend and Dispersion Measures')
        plt.legend()
        plt.show()
