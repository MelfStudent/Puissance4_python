import random
import time

class IA:
    @staticmethod
    def ia_choice(plateau):
        print("AI is thinking")
        time.sleep(random.uniform(1, 3))
        column = random.randint(0, 6)
        while plateau.plateau[0][column] != 0:
            column = random.randint(0, 6)

        for row in range(5, -1, -1):
            if plateau.plateau[row][column] == 0:
                plateau.plateau[row][column] = -1
                plateau.shots.append((row, column))
                plateau.shots_played_ia += 1
                print("AI has just played its part")
                break
