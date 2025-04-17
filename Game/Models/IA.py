import random
import time
import numpy as np

from .Database import Database
from .Utils import Utils

class IA:
    """Class representing the artificial intelligence

    This class contains static methods to manage the AI's choices, generate possible moves,
    evaluate moves, and count alignments.
    """

    @staticmethod
    def ia_choice(plateau):
        """Manages the AI's choice by selecting the best possible move

        The AI simulates thinking with a random delay, generates possible moves,
        evaluates them, and plays the move with the highest score.

        Args:
            plateau (Plateau): The instance of the game board.
        """
        print("AI is thinking...")
        time.sleep(random.uniform(1, 2))

        possible_moves = IA.generate_possible_moves(plateau)

        evaluated_moves = IA.evaluate_moves(plateau, possible_moves)

        # Selects the move with the highest score
        best_move = max(evaluated_moves, key=evaluated_moves.get)
        row, col = best_move

        # Place the AI's token on the board
        board = plateau.get_plateau()
        board[row][col] = -1
        plateau.set_plateau(board)

        # Add the move to the list of played shots
        shots = plateau.get_shots()
        shots.append((row, col))
        plateau.set_shots(shots)

        plateau.set_shots_played_ia(plateau.get_shots_played_ia() + 1)

        print(f"AI played at column {col + 1}")

    @staticmethod
    def generate_possible_moves(plateau):
        """Generates a dictionary of possible moves on the board

        The keys are the positions (row, column) and the values are initialized to 0.

        Args:
            plateau (Plateau): The instance of the game board.

        Returns:
            dict: A dictionary of possible moves with their initial scores.
        """
        possible_moves = {}
        for col in range(7):
            for row in range(5, -1, -1):
                if plateau.get_plateau()[row][col] == 0:
                    possible_moves[(row, col)] = 0  # Initialisation à 0
                    break
        return possible_moves

    @staticmethod
    def evaluate_moves(plateau_obj, moves):
        """Evaluates each possible move by simulating the move on the board

        Assigns scores based on the possibility of winning, blocking the opponent,
        and the alignment of tokens.

        Args:
            plateau_obj (Plateau): The instance of the game board.
            moves (dict): The dictionary of possible moves.

        Returns:
            dict: The dictionary of possible moves with their updated scores.
        """
        points_config = Utils.load_points_config()

        board = plateau_obj.get_plateau()
        player = 1
        ia = -1

        historical_scores = Database.evaluate_moves_from_history(plateau_obj.get_shots(), ia)

        for (row, col) in moves:
            simulated_board = np.copy(board)
            simulated_board[row][col] = ia

            # Check if the move leads to a win for the AI
            if Utils.get_player_to_win(simulated_board) == ia:
                moves[(row, col)] += points_config["immediate_win"]
                continue

            simulated_board[row][col] = player
            # Check if the move blocks a win for the player
            if Utils.get_player_to_win(simulated_board) == player:
                moves[(row, col)] += points_config["block_opponent_win"]

            # Check if the move gives the player a win on the next turn
            for next_col in range(7):
                for next_row in range(5, -1, -1):
                    if simulated_board[next_row][next_col] == 0:
                        simulated_board[next_row][next_col] = player
                        if Utils.get_player_to_win(simulated_board) == player:
                            moves[(row, col)] -= points_config["avoid_giving_win"]
                        simulated_board[next_row][next_col] = 0  # Reset the simulated move
                        break

            # Add points for potential alignments of the AI and the player
            moves[(row, col)] += IA.count_alignment(board, row, col, ia) * points_config["ai_alignment_score"]
            moves[(row, col)] += IA.count_alignment(board, row, col, player) * points_config["player_alignment_score"]

            moves[(row, col)] += points_config["central_column_preference"] - abs(3 - col)  # Higher score for columns closer to the center

            # Add historical score if available
            if (row, col) in historical_scores:
                moves[(row, col)] += historical_scores[(row, col)]

        return moves

    @staticmethod
    def count_alignment(board, row, col, player):
        """Counts the number of aligned tokens in all directions

        Counts horizontal, vertical, and diagonal alignments for a given player
        from a specific position.

        Args:
            board (np.array): The array representing the game board.
            row (int): The row of the position to evaluate.
            col (int): The column of the position to evaluate.
            player (int): The player for whom to count the alignments (1 for human, -1 for AI).

        Returns:
            int: The maximum number of aligned tokens found.
        """
        count = 0

        def count_dir(dr, dc):
            """Counts the number of aligned tokens in a given direction.

            Args:
                dr (int): Row movement for the direction.
                dc (int): Column movement for the direction.

            Returns:
                int: The number of aligned tokens in this direction.
            """
            total = 1
            for direction in [1, -1]:
                r, c = row, col
                for _ in range(3):
                    r += dr * direction
                    c += dc * direction
                    if 0 <= r < 6 and 0 <= c < 7 and board[r][c] == player:
                        total += 1
                    else:
                        break
            return total

        # Check the four possible directions: horizontal, vertical, and diagonals
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            count = max(count, count_dir(dr, dc))

        return count
