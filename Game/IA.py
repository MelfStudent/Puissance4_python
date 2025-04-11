import random
import time

class IA:
    """
    Simulates the AI game by randomly placing a token

    Parameters:
        array: plateau | table containing the positions of the moves played such as (5, 1)
    """
    @staticmethod
    @staticmethod
    def ia_choice(plateau):
        print("AI is thinking")
        time.sleep(random.uniform(1, 3))

        possible_moves = IA.generate_possible_moves(plateau)

        column = random.choice(list(possible_moves.keys()))
        row = possible_moves[column]

        plateau.plateau[row][column] = -1
        plateau.shots.append((row, column))
        plateau.shots_played_ia += 1
        print("AI has just played its part")

    @staticmethod
    def generate_possible_moves(plateau):
        possible_moves = {}
        for column in range(7):
            for row in range(5, -1, -1):
                if plateau.plateau[row][column] == 0:
                    possible_moves[column] = row
                    break

        return possible_moves
