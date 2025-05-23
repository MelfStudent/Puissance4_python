import ast
import os
from pathlib import Path

import seaborn as sns
import random

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, gridspec
from matplotlib.backends.backend_pdf import PdfPages

from .Database import Database
from .Graphics import Graphics
from .IA import IA
from .Player import Player
from .Utils import Utils


class Plateau:
    """Class representing the game board

    This class manages the game state, including the board, current player,
    and game logic such as checking for wins and switching players.
    """
    def __init__(self):
        """Initializes the game board and game state
        """
        self._shots = None
        self._winner = None
        self._shots_played_ia = None
        self._shots_played_player = None
        self._player_who_starts = None
        self._current_player = None
        self._game_over = None
        self._plateau = None
        self._reset_game()

    def _reset_game(self):
        """Resets the game state to initial values
        """
        self._plateau = np.zeros((6, 7), dtype=int)
        self._game_over = False
        self._current_player = 0
        self._player_who_starts = 0
        self._shots_played_player = 0
        self._shots_played_ia = 0
        self._winner = 0
        self._shots = []

    def get_plateau(self):
        """Getter for the game board
        """
        return self._plateau

    def set_plateau(self, plateau):
        """Setter for the game board
        """
        self._plateau = plateau

    def get_shots(self):
        """Getter for the list of shots played
        """
        return self._shots

    def set_shots(self, shots):
        """Setter for the list of shots played
        """
        self._shots = shots

    def get_shots_played_ia(self):
        """Getter for the number of shots played by the AI
        """
        return self._shots_played_ia

    def set_shots_played_ia(self, shots_played_ia):
        """Setter for the number of shots played by the AI
        """
        self._shots_played_ia = shots_played_ia

    def get_shots_played_player(self):
        """Getter for the number of shots played by the player
        """
        return self._shots_played_player

    def set_shots_played_player(self, shots_played_player):
        """Setter for the number of shots played by the player
        """
        self._shots_played_player = shots_played_player

    def get_player_who_starts(self):
        """Getter for the player who starts the game
        """
        return self._player_who_starts

    def set_player_who_starts(self, player_who_starts):
        """Setter for the player who starts the game
        """
        self._player_who_starts = player_who_starts

    def get_current_player(self):
        """Getter for the current player
        """
        return self._current_player

    def set_current_player(self, current_player):
        """Setter for the current player
        """
        self._current_player = current_player

    def get_game_over(self):
        """Getter for the game over status
        """
        return self._game_over

    def set_game_over(self, game_over):
        """Setter for the game over status
        """
        self._game_over = game_over

    def get_winner(self):
        """Getter for the winner of the game
        """
        return self._winner

    def set_winner(self, winner):
        """Setter for the winner of the game
        """
        self._winner = winner

    def display_plateau(self):
        """Displays the board in the console as a grid with colored tokens
        """
        PLAYER_COLOR = "\033[93m●\033[0m"
        IA_COLOR = "\033[91m●\033[0m"
        EMPTY_COLOR = "\033[97m○\033[0m"

        print("\n  1 2 3 4 5 6 7")
        print(" ---------------")

        for row in self.get_plateau():
            print("|", end=" ")
            for cell in row:
                if cell == 1:
                    print(PLAYER_COLOR, end=" ")
                elif cell == -1:
                    print(IA_COLOR, end=" ")
                else:
                    print(EMPTY_COLOR, end=" ")
            print("|")

        print(" ---------------\n")

    def player_action(self):
        """Displays the player or AI index depending on who is playing, and calls their game function
        """
        current_player_str = "Player" if self.get_current_player() == 1 else "IA"
        print(f"{current_player_str} turn!")

        if self.get_current_player() == 1:
            Player.player_choice(self)

        elif self.get_current_player() == -1:
            IA.ia_choice(self)

    def switch_player(self):
        """Toggles the player's hint to play based on the previous player
        """
        self.set_current_player(-1 if self.get_current_player() == 1 else 1)

    def check_win(self):
        """Checks if there is a winner or the game is a draw and updates the game state accordingly.
        """
        if Utils.get_player_to_win(self.get_plateau()) == 1:
            self.set_game_over(True)
            self.display_plateau()
            self.set_winner(1)
            print("Player wins!")

        elif Utils.get_player_to_win(self.get_plateau()) == -1:
            self.set_game_over(True)
            self.display_plateau()
            self.set_winner(-1)
            print("IA wins!")

        elif not np.any(self.get_plateau() == 0):
            self.set_game_over(True)
            self.display_plateau()
            print("The game is a draw because the board is full!")

    def save_game(self):
        """Calls the save_new_game method of the Database class to save the current game state to a CSV file
        """
        Database.save_new_game(self.get_player_who_starts(), self.get_winner(), self.get_shots_played_player(), self.get_shots_played_ia(), self.get_shots())

    def player_choice_who_starts(self):
        """Prompts the user to choose who starts the game between human, AI, or random
        """
        print("Player who starts!")
        print("1. You")
        print("2. IA")
        print("3. Random")

        while True:
            try:
                choice = int(input("Please enter your choice: "))
                if choice == 1:
                    self.set_player_who_starts(1)
                    self.set_current_player(1)
                    break
                elif choice == 2:
                    self.set_player_who_starts(-1)
                    self.set_current_player(-1)
                    break
                elif choice == 3:
                    self.set_player_who_starts([-1, 1][random.choice([0, 1])])
                    self.set_current_player(self.get_player_who_starts())
                    break
                else:
                    print("Error: Please enter a number between 1 and 2.")
            except ValueError:
                print("Please enter a number.")

    @staticmethod
    def show_graphics():
        """Displays all the graphics
        """
        Graphics.plot_overview()
        Graphics.plot_trend_dispersion()
        Graphics.plot_wins_by_first_player()
        Graphics.plot_column_play_counts()
        Graphics.plot_games_per_month()
        Graphics.plot_shots_frequency_per_game()

    @staticmethod
    def welcome_menu_options():
        """Display the welcome menu options
        """
        print("1. Start a new game")
        print("2. Statistics panel")
        print("3. Quit the game")

    @staticmethod
    def handle_export():
        """Exports all game data to a CSV file
        """
        try:
            df = pd.read_csv("../data/game_data.csv")
        except FileNotFoundError:
            print("No game data found.")
            return

        filename = input("Enter filename (leave empty for default): ").strip()
        if not filename:
            filename = "exported_game_data.csv"

        Database.export_dataframe(df, filename)

    @staticmethod
    def handle_filtered_export():
        """Exports filtered game data to a CSV file
        """
        df = Database.filter_game_data()
        if df is None or df.empty:
            print("\nNo filtered data to export.")
            return

        df = Database.select_columns(df)
        df = Database.sort_game_data(df)

        filename = input("Enter filename for filtered export (leave empty for default): ").strip()
        if not filename:
            filename = "filtered_game_data.csv"

        Database.export_dataframe(df, filename)

    @staticmethod
    def show_all_data_terminal():
        """Displays all game data in the terminal
        """
        try:
            df = pd.read_csv("../data/game_data.csv")
            if df.empty:
                print("\n⚠️ No game data available.")
            else:
                print("\n=== All Game Data ===")
                print(df.to_string(index=False))
        except FileNotFoundError:
            print("No data file found.")

    @staticmethod
    def show_filtered_data_terminal():
        """Displays filtered game data in the terminal
        """
        df = Database.filter_game_data()
        if df is None:
            return
        if df.empty:
            print("\nNo matching data found.")
            return

        df = Database.select_columns(df)
        df = Database.sort_game_data(df)

        print("\n=== Filtered Game Data ===")
        print(df.to_string(index=False))

    @staticmethod
    def prepare_data(df):
        """Prepares the data for statistical analysis.

        Args:
            df (pd.DataFrame): The DataFrame containing the game data.

        Returns:
            pd.DataFrame: The DataFrame with additional columns for analysis.
        """
        df["starter_wins"] = df["player_who_starts"] == df["winner"]
        df["total_shots"] = df["shots_played_player"] + df["shots_played_ia"]
        df["date"] = pd.to_datetime(df["date"])
        df["is_win"] = df["winner"] == 1
        df["winner_str"] = df["winner"].apply(lambda x: "Player" if x == 1 else "IA")
        return df

    @staticmethod
    def compute_statistics(df):
        """Computes various statistics from the game data.

        Args:
            df (pd.DataFrame): The DataFrame containing the game data.

        Returns:
            tuple: A tuple containing the following statistics:
                - win_counts (pd.Series): The count of wins for each winner.
                - win_percentages (pd.Series): The percentage of wins for each winner.
                - starter_win_rate (float): The win rate of the starting player.
                - avg_shots (float): The average number of shots per game.
                - all_coords (list): A list of all coordinates played in the games.
        """
        win_counts = df["winner_str"].value_counts()
        win_percentages = (win_counts / len(df) * 100).round(2)
        starter_win_rate = df["starter_wins"].mean() * 100
        avg_shots = df["total_shots"].mean()

        all_coords = []
        for s in df["shots"]:
            try:
                coords = ast.literal_eval(s)
                all_coords.extend(coords)
            except:
                continue

        return win_counts, win_percentages, starter_win_rate, avg_shots, all_coords

    @staticmethod
    def statistical_analysis(mode="graphic"):
        """Performs statistical analysis and displays the results in the specified mode

        This method reads the game data from 'data/game_data.csv', prepares it for analysis, computes various statistics,
        and then displays the results either in the terminal or as a graphical dashboard based on the specified mode.

        Args:
            mode (str): The mode in which to display the analysis results. Can be "graphic" or "terminal".
        """
        try:
            df = pd.read_csv("../data/game_data.csv")
        except FileNotFoundError:
            print("No game data found.")
            return

        df = Plateau.prepare_data(df)
        win_counts, win_percentages, starter_win_rate, avg_shots, all_coords = Plateau.compute_statistics(df)

        if mode == "terminal":
            Plateau.display_terminal_report(df, win_counts, win_percentages, starter_win_rate, avg_shots,
                                                 all_coords)
        elif mode == "graphic":
            Plateau.display_graphical_dashboard(df, win_counts, win_percentages, starter_win_rate, avg_shots,
                                                     all_coords)
        else:
            print("Invalid mode. Use 'graphic' or 'terminal'.")

    @staticmethod
    def display_terminal_report(df, win_counts, win_percentages, starter_win_rate, avg_shots, all_coords):
        """Displays the statistical report in the terminal

        This method prints a summary of the game statistics to the terminal, including the total number of games,
        win counts and percentages, starter win rate, average number of moves per game, and the most played columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the game data.
            win_counts (pd.Series): The count of wins for each winner.
            win_percentages (pd.Series): The percentage of wins for each winner.
            starter_win_rate (float): The win rate of the starting player.
            avg_shots (float): The average number of shots per game.
            all_coords (list): A list of all coordinates played in the games.
        """
        print("\n=== Game Statistics Report ===")
        print(f"\nTotal games: {len(df)}")
        print("\n--- Win Counts ---")
        for winner, count in win_counts.items():
            print(f"{winner}: {count} games ({win_percentages[winner]}%)")

        print(f"\nStarter win rate: {starter_win_rate:.2f}%")
        print(f"Average number of moves per game: {avg_shots:.2f}")

        if all_coords:
            coords_df = pd.DataFrame(all_coords, columns=["row", "column"])
            freq_col = coords_df["column"].value_counts().sort_index()
            print("\n--- Most Played Columns ---")
            for col, count in freq_col.items():
                print(f"Column {col}: {count} moves")
        else:
            print("\nNo move data available.")

    @staticmethod
    def display_graphical_dashboard(df, win_counts, win_percentages, starter_win_rate, avg_shots, all_coords):
        """Displays the statistical report as a graphical dashboard

        This method creates a graphical dashboard with various plots to visualize the game statistics, including
        the number of wins, player win rate over time, number of moves per winner, distribution of total moves,
        most played columns, and a summary text.

        Args:
            df (pd.DataFrame): The DataFrame containing the game data.
            win_counts (pd.Series): The count of wins for each winner.
            win_percentages (pd.Series): The percentage of wins for each winner.
            starter_win_rate (float): The win rate of the starting player.
            avg_shots (float): The average number of shots per game.
            all_coords (list): A list of all coordinates played in the games.
        """
        fig = plt.figure(constrained_layout=True, figsize=(16, 10))
        spec = gridspec.GridSpec(ncols=3, nrows=2, figure=fig)

        ax1 = fig.add_subplot(spec[0, 0])
        win_counts.plot(kind="bar", color=["#4caf50", "#f44336"], ax=ax1)
        ax1.set_title("Number of Wins")
        ax1.set_ylabel("Games")
        ax1.set_xlabel("Winner")

        ax2 = fig.add_subplot(spec[0, 1])
        df.set_index("date").resample("D")["is_win"].mean().plot(ax=ax2, color="#2196f3")
        ax2.set_title("Player Win Rate Over Time")
        ax2.set_ylabel("Win Rate")

        ax3 = fig.add_subplot(spec[0, 2])
        sns.boxplot(x="winner_str", y="total_shots", data=df, hue="winner_str", palette="Set2", ax=ax3, legend=False)
        ax3.set_title("Number of Moves per Winner")
        ax3.set_xlabel("Winner")
        ax3.set_ylabel("Moves")

        ax4 = fig.add_subplot(spec[1, 0])
        df["total_shots"].hist(bins=10, color="#9c27b0", ax=ax4)
        ax4.set_title("Distribution of Total Moves")
        ax4.set_xlabel("Moves per Game")
        ax4.set_ylabel("Games")

        ax5 = fig.add_subplot(spec[1, 1])
        if all_coords:
            coords_df = pd.DataFrame(all_coords, columns=["row", "column"])
            col_freq = coords_df["column"].value_counts().sort_index()
            col_freq.plot(kind="bar", color="#ff9800", ax=ax5)
            ax5.set_title("Most Played Columns")
            ax5.set_xlabel("Column (0 to 6)")
            ax5.set_ylabel("Total Moves")
        else:
            ax5.text(0.5, 0.5, "No move data available", ha='center', va='center')
            ax5.set_title("Most Played Columns")
            ax5.axis("off")

        ax6 = fig.add_subplot(spec[1, 2])
        ax6.axis("off")
        text = (
            f"Total Games: {len(df)}\n"
            f"Player Wins: {win_counts.get('Player', 0)} ({win_percentages.get('Player', 0)}%)\n"
            f"IA Wins: {win_counts.get('IA', 0)} ({win_percentages.get('IA', 0)}%)\n"
            f"Starter Win Rate: {starter_win_rate:.2f}%\n"
            f"Avg. Moves per Game: {avg_shots:.2f}"
        )
        ax6.text(0, 1, text, fontsize=12, verticalalignment='top')

        fig.suptitle("Game Statistics Dashboard", fontsize=16, fontweight='bold')
        plt.show()

    @staticmethod
    def generate_pdf_report():
        """Generates a PDF report of the game statistics
        """
        df = Plateau.load_data()
        if df is None:
            print("No game data found.")
            return

        stats = Plateau.compute_all_stats(df)
        filepath = Plateau.get_report_filepath()

        with PdfPages(filepath) as pdf:
            fig = plt.figure(constrained_layout=True, figsize=(16, 24))
            spec = gridspec.GridSpec(ncols=2, nrows=5, figure=fig, height_ratios=[0.1, 1, 1, 1,1])

            fig.suptitle("Connect Four - Game Statistics Report", fontsize=16, fontweight='bold',y=0.97)

            # Plot Overview
            ax1 = fig.add_subplot(spec[1, 0])
            Graphics.plot_overview(ax=ax1)

            # Plot Trend and Dispersion
            ax2 = fig.add_subplot(spec[1, 1])
            Graphics.plot_trend_dispersion(ax=ax2)

            # Plot Wins by First Player
            ax3 = fig.add_subplot(spec[2, 0])
            Graphics.plot_wins_by_first_player(ax=ax3)

            # Plot Column Play Counts
            ax4 = fig.add_subplot(spec[2, 1])
            Graphics.plot_column_play_counts(ax=ax4)

            # Plot Games per Month
            ax5 = fig.add_subplot(spec[3, 0])
            Graphics.plot_games_per_month(ax=ax5)

            # Plot Shots Frequency per Game
            ax6 = fig.add_subplot(spec[3, 1])
            Graphics.plot_shots_frequency_per_game(ax=ax6)

            ax7 = fig.add_subplot(spec[4, :])
            Plateau.add_summary_text(ax7, df, stats)

            pdf.savefig(fig)
            plt.close(fig)

        print(f"\nPDF report saved to: {filepath}")

    @staticmethod
    def load_data():
        """Loads game data from the CSV file

        Returns:
            pd.DataFrame: A DataFrame containing the game data.
        """
        try:
            return pd.read_csv("../data/game_data.csv")
        except FileNotFoundError:
            return None

    @staticmethod
    def compute_all_stats(df):
        """Computes all necessary statistics for the game data

        Args:
            df (pd.DataFrame): The DataFrame containing the game data.

        Returns:
            dict: A dictionary containing the following statistics:
                - win_counts (pd.Series): The count of wins for each winner.
                - win_percentages (pd.Series): The percentage of wins for each winner.
                - starter_win_rate (float): The win rate of the starting player.
                - avg_shots (float): The average number of shots per game.
                - all_coords (list): A list of all coordinates played in the games.
        """
        df = Plateau.prepare_data(df)
        win_counts, win_percentages, starter_win_rate, avg_shots, all_coords = Plateau.compute_statistics(df)
        return {
            "win_counts": win_counts,
            "win_percentages": win_percentages,
            "starter_win_rate": starter_win_rate,
            "avg_shots": avg_shots,
            "all_coords": all_coords
        }

    @staticmethod
    def get_report_filepath():
        """Gets the file path for the PDF report

        Returns:
            str: The file path for the PDF report.
        """
        base_name = input("Enter report name (without .pdf): ").strip() or "game_analysis_report"
        downloads_path = str(Path.home() / "Downloads")
        counter = 1
        filename = f"{base_name}.pdf"
        filepath = os.path.join(downloads_path, filename)

        while os.path.exists(filepath):
            filename = f"{base_name}_{counter}.pdf"
            filepath = os.path.join(downloads_path, filename)
            counter += 1

        return filepath

    @staticmethod
    def create_fig_with_axes():
        """Creates a figure with subplots

       Returns:
           tuple: A tuple containing the figure and a list of axes.
       """
        fig = plt.figure(constrained_layout=True, figsize=(16, 10))
        spec = gridspec.GridSpec(ncols=3, nrows=2, figure=fig)
        axes = [fig.add_subplot(spec[i, j]) for i in range(2) for j in range(3)]
        return fig, axes

    @staticmethod
    def plot_all_charts(df, stats, axes):
        """Plots all charts for the PDF report

        Args:
            df (pd.DataFrame): The DataFrame containing the game data.
            stats (dict): A dictionary containing the computed statistics.
            axes (list): A list of axes for plotting the charts.
        """
        win_counts = stats["win_counts"]
        all_coords = stats["all_coords"]

        axes[0].bar(win_counts.index, win_counts.values, color=["#4caf50", "#f44336"])
        axes[0].set_title("Number of Wins")
        axes[0].set_ylabel("Games")
        axes[0].set_xlabel("Winner")

        df.set_index("date").resample("D")["is_win"].mean().plot(ax=axes[1], color="#2196f3")
        axes[1].set_title("Player Win Rate Over Time")
        axes[1].set_ylabel("Win Rate")

        sns.boxplot(x="winner_str", y="total_shots", data=df, hue="winner_str", palette="Set2", ax=axes[2],
                    legend=False)
        axes[2].set_title("Number of Moves per Winner")
        axes[2].set_xlabel("Winner")
        axes[2].set_ylabel("Moves")

        df["total_shots"].hist(bins=10, color="#9c27b0", ax=axes[3])
        axes[3].set_title("Distribution of Total Moves")
        axes[3].set_xlabel("Moves per Game")
        axes[3].set_ylabel("Games")

        if all_coords:
            coords_df = pd.DataFrame(all_coords, columns=["row", "column"])
            col_freq = coords_df["column"].value_counts().sort_index()
            col_freq.plot(kind="bar", color="#ff9800", ax=axes[4])
            axes[4].set_title("Most Played Columns")
            axes[4].set_xlabel("Column (0 to 6)")
            axes[4].set_ylabel("Total Moves")
            axes[4].set_xticks(range(len(col_freq)))
            axes[4].set_xticklabels([str(i) for i in col_freq.index], rotation=90)
        else:
            axes[4].text(0.5, 0.5, "No move data available", ha='center', va='center')
            axes[4].set_title("Most Played Columns")
            axes[4].axis("off")

    @staticmethod
    def add_summary_text(ax, df, stats):
        """Adds summary text to the PDF report

        Args:
            ax (matplotlib.axes.Axes): The axes to add the summary text to.
            df (pd.DataFrame): The DataFrame containing the game data.
            stats (dict): A dictionary containing the computed statistics.
        """
        ax.axis("off")
        wc, wp = stats["win_counts"], stats["win_percentages"]
        text = (
            f"Game Analysis Summary\n\n"
            f"Total Games: {len(df)}\n"
            f"Player Wins: {wc.get('Player', 0)} ({wp.get('Player', 0)}%)\n"
            f"IA Wins: {wc.get('IA', 0)} ({wp.get('IA', 0)}%)\n"
            f"Starter Win Rate: {stats['starter_win_rate']:.2f}%\n"
            f"Avg. Moves/Game: {stats['avg_shots']:.2f}\n\n"
        )
        ax.text(0, 1, text, fontsize=11, verticalalignment='top')

    def statistics_menu(self):
        """Submenu for statistics panel with options
        """
        while True:
            print("\n--- Statistics Panel ---")
            print("1. Export all game data to CSV")
            print("2. Export filtered game data to CSV")
            print("3. Show all game data in terminal")
            print("4. Show filtered game data in terminal")
            print("5. Show graphs")
            print("6. Data analysis")
            print("7. Generate PDF report")
            print("8. Delete filtered data")
            print("9. Back to main menu")

            choice = input("Your choice: ").strip()

            if choice == '1':
                self.handle_export()
            elif choice == '2':
                self.handle_filtered_export()
            elif choice == '3':
                self.show_all_data_terminal()
            elif choice == '4':
                self.show_filtered_data_terminal()
            elif choice == '5':
                self.show_graphics()
            elif choice == '6':
                while True:
                    print("\n--- Data Analysis Mode ---")
                    print("1. Display analysis in terminal")
                    print("2. Display analysis with graphs")
                    print("3. Back")

                    sub_choice = input("Choose an option: ")

                    if sub_choice == "1":
                        self.statistical_analysis(mode="terminal")
                    elif sub_choice == "2":
                        self.statistical_analysis(mode="graphic")
                    elif sub_choice == "3":
                        break
                    else:
                        print("Invalid option.")
            elif choice == '7':
                Plateau.generate_pdf_report()
            elif choice == '8':
                Database.delete_filtered_data()
            elif choice == '9':
                break
            else:
                print("Invalid choice. Please try again.")

    def welcome_menu(self):
        """Main welcome menu
        """
        while True:
            self.welcome_menu_options()
            choice = input("Your choice:")

            if choice == '1':
                self.start_game()
            elif choice == '2':
                self.statistics_menu()
            elif choice == '3':
                print("Goodbye and see you soon!")
                exit()
            else:
                print("Invalid choice. Please try again.")

    def start_game(self):
        """Starts the game by initializing the starting player and managing the game loop until the game ends
        """
        self._reset_game()
        self.player_choice_who_starts()

        while not self.get_game_over():
            self.display_plateau()
            self.player_action()
            self.switch_player()
            self.check_win()

        self.save_game()
