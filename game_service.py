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
        "Player action": self.player_action,
        "Get state": self.get_game_state
        }

    def perform_action(self, action_name, action_params):
        result = self.game_actions[action_name](action_params)
        #print(self.game.check_betting_fished())
        return result

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

    def player_action(self, params):
        self.game.player_action(params)
        self.get_game_state(None)

    def get_game_state(self, params):
        table = self.game.table
        players = self.game.players
        self.current_player = self.game.get_current_player()
        round_no = self.game.round_no
        game_state={
            "Table": table,
            "Players": players,
            "Current player": self.current_player,
            "Round no": round_no
        }
        return game_state

    def check_game(self):
        return self.game.finished
    
    def get_current_player(self):
        return self.game.get_current_player()



# game_service = GameService()
# game_service.perform_action("Add player", {"player name": "Pawel"})
# game_service.perform_action("Add player", {"player name": "Karolina"})
# game_service.perform_action("Add player", {"player name": "Tyna"})
# game_service.perform_action("Start game", None)

# while not game_service.game.finished:
#     print(game_service.perform_action("Get state", None))
#     game_service.perform_action("Next move", None)
    
