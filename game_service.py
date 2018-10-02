from game import Game
from player import Player

class GameService():

    def __init__(self):
        self.game = Game()

    def get_table(self):
        return self.game.print_table()

    def get_players(self):
        return self.game.players

    def add_player(self, name):
        self.game.add_player(name)

    def start_game(self):
        self.game.deal_cards_to_players()

    def get_player(self, name):
        return self.game.get_player(name)

    def perform_action(self, action):
        self.game.add_new_card_to_table()

    def check_game(self):
        return self.game.finished



game_service = GameService()

game_service.add_player("Pawel")
game_service.add_player("Karolina")

print(list(map(lambda p: str(p), game_service.get_players())))

game_service.start_game()

print(game_service.get_table())
input("PRESS ENTER")
while not game_service.check_game():
    game_service.perform_action(None)
    print(game_service.get_table())
    input("PRESS ENTER")
