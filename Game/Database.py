import csv
import datetime

class Database:

    """
    Calculates the number of games recorded in the game_data.csv file and returns the number + 1

    Returns:
        int: the number of games recorded in the game_data.csv file
    """
    @staticmethod
    def get_next_id():
        try:
            with open('data/game_data.csv', 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                return len(rows) + 1
        except FileNotFoundError:
            return 1

    """
    Saves a game to the game_data.csv file in the form (game id, date, starting player, winner, number of moves played by the player, number of moves played by the AI and moves played
    
    Parameters:
        int: player_who_starts |    -1 when the AI starts and 1 when the player starts
        int: winner |   -1 when the AI wins and 1 when the player wins
        int: shots_played_player |  number of moves the player has to play
        int: shots_played_ia |  number of moves the AI has to play
        array: shots |  table containing the position of the moves played in the order of the game
    """
    @staticmethod
    def save_new_game(player_who_starts:int, winner:int, shots_played_player:int, shots_played_ia:int, shots):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        get_next_id = Database.get_next_id()

        with open('Data/game_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([get_next_id, current_date, player_who_starts, winner, shots_played_player, shots_played_ia, shots])
