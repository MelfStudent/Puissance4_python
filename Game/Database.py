import csv
import datetime

class Database:
    @staticmethod
    def get_next_id():
        try:
            with open('data/game_data.csv', 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                return len(rows) + 1
        except FileNotFoundError:
            return 1

    @staticmethod
    def save_new_game(player_who_starts:int, winner:int, shots_played_player:int, shots_played_ia:int, shots):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        get_next_id = Database.get_next_id()

        with open('Data/game_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([get_next_id, current_date, player_who_starts, winner, shots_played_player, shots_played_ia, shots])
