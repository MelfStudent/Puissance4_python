import random

import numpy as np

from Game.Database import Database
from Game.IA import IA
from Game.Player import Player

class Plateau:
    def __init__(self):
        self.plateau = np.zeros((6, 7), dtype=int)
        self.game_over = False
        self.current_player = 0
        self.player_who_starts = 0
        self.shots_played_player = 0
        self.shots_played_ia = 0
        self.winner = 0
        self.shots = []

    """
    Displays the board in the console as a grid with colored tokens
    """
    def display_plateau(self):
        player_color = "\033[93m●\033[0m"
        ia_color = "\033[91m●\033[0m"
        empty_color = "\033[97m○\033[0m"

        print("\n  1 2 3 4 5 6 7")
        print(" ---------------")

        for row in self.plateau:
            print("|", end=" ")
            for cell in row:
                if cell == 1:
                    print(player_color, end=" ")
                elif cell == -1:
                    print(ia_color, end=" ")
                else:
                    print(empty_color, end=" ")
            print("|")

        print(" ---------------\n")

    """
    Displays the player or AI index depending on who is playing, and calls their game function
    """
    def player_action(self):
        print(f"Player {self.current_player}'s turn!")

        if self.current_player == 1:
            Player.player_choice(self)

        elif self.current_player == -1:
            IA.ia_choice(self)

    """
    Toggles the player's hint to play based on the previous player
    """
    def switch_player(self):
        if self.current_player == 1:
            self.current_player = -1
        else:
            self.current_player = 1

    """
    Checks the game board for a winning condition.
    
    Returns:
            int: 1 if the human player wins, -1 if the AI wins, 0 if no winner yet.
    """
    def get_player_to_win(self):
        for line in range(6):
            for column in range(7):
                if self.plateau[line][column] != 0:
                    if column + 3 < 7 and all(
                            self.plateau[line][column + i] == self.plateau[line][column] for i in range(4)):
                        return self.plateau[line][column]

                    if line + 3 < 6 and all(
                            self.plateau[line + i][column] == self.plateau[line][column] for i in range(4)):
                        return self.plateau[line][column]

                    if line + 3 < 6 and column + 3 < 7 and all(
                            self.plateau[line + i][column + i] == self.plateau[line][column] for i in range(4)):
                        return self.plateau[line][column]

                    if line - 3 >= 0 and column + 3 < 7 and all(
                            self.plateau[line - i][column + i] == self.plateau[line][column] for i in range(4)):
                        return self.plateau[line][column]
        return 0

    """
    Checks if there is a winner or the game is a draw and updates the game state accordingly.
    """
    def check_win(self):
        if self.get_player_to_win() == 1:
            self.game_over = True
            self.display_plateau()
            self.winner = 1
            print("Player wins!")

        elif self.get_player_to_win() == -1:
            self.game_over = True
            self.display_plateau()
            self.winner = -1
            print("IA wins!")

        elif not np.any(self.plateau == 0):
            self.game_over = True
            self.display_plateau()
            print("The game is a draw because the board is full!")

    """
    Calls the save_new_game method of the Database class to save the current game state to a CSV file
    """
    def save_game(self):
        Database.save_new_game(self.player_who_starts, self.winner, self.shots_played_player, self.shots_played_ia, self.shots)

    """
    Prompts the user to choose who starts the game between human, AI, or random
    """
    def player_choice_who_starts(self):
        print("Player who starts!")
        print("1. You")
        print("2. IA")
        print("3. Random")

        while True:
            try:
                choice = int(input("Please enter your choice: "))
                if choice == 1:
                    self.player_who_starts = 1
                    self.current_player = 1
                    break
                elif choice == 2:
                    self.player_who_starts = -1
                    self.current_player = -1
                    break
                elif choice == 3:
                    self.player_who_starts = [-1, 1][random.choice([0, 1])]
                    self.current_player = self.player_who_starts
                    break
                else:
                    print("Error: Please enter a number between 1 and 2.")
            except ValueError:
                print("Please enter a number.")

    """
    Starts the game by initializing the starting player and managing the game loop until the game ends.
    """
    def start_game(self):
        self.player_choice_who_starts()

        while not self.game_over:
            self.display_plateau()
            self.player_action()
            self.switch_player()
            self.check_win()

        self.save_game()
