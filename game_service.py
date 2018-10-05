from game import Game
from player import Player


class GameService():

    def __init__(self):
        self.game = Game()
        self.game_actions={
        "Add player": self.add_player,
        "Get players": self.get_players,
        "Get player": self.get_player,
        "Start game": self.start_game,
        "Next move": self.next_player,
        "Get state": self.get_game_state
        }

    def perform_action(self, action_name, action_params):
        return self.game_actions[action_name](action_params)

    def get_table(self):
        return self.game.print_table()

    def get_players(self, params):
        return self.game.players

    def add_player(self, params):
        self.game.add_player(params["player name"])

    def start_game(self, params):
        self.game.deal_cards_to_players()
        self.game.get_next_player()

    def get_player(self, params):
        self.game.get_player(params["player name"])

    def next_player(self, params):
        current_player = self.game.get_next_player()
        if not current_player:
            self.game.reset_round()
            current_player = self.game.get_next_player()
        return current_player

    def get_game_state(self, params):
        table = self.game.table
        players = self.game.players
        current_player = self.game.get_current_player()

        game_state={
            "Table": table,
            "Players": players,
            "Current player": current_player
        }

        return game_state

    def check_game(self):
        return self.game.finished
    
    def get_current_player(self):
        return self.game.get_current_player()



game_service = GameService()
game_service.perform_action("Add player", {"player name": "Pawel"})
game_service.perform_action("Add player", {"player name": "Karolina"})
game_service.perform_action("Add player", {"player name": "Tyna"})
game_service.perform_action("Start game", None)

while not game_service.game.finished:
    print(game_service.perform_action("Get state", None))
    game_service.perform_action("Next move", None)
    
