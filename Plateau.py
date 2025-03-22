import random

import numpy as np

from IA import IA
from Player import Player

class Plateau:
    def __init__(self):
        self.plateau = np.zeros((6, 7), dtype=int)
        self.game_over = False
        self.current_player = random.choice([1, 2])

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

    def player_action(self):
        print(f"Player {self.current_player}'s turn!")

        if self.current_player == 1:
            Player.player_choice(self)

        elif self.current_player == 2:
            IA.ia_choice(self)

    def switch_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def start_game(self):
        while not self.game_over:
            self.display_plateau()
            self.player_action()
