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
        action_result = self.game_actions[action_name](action_params)
        return action_result
        
    def get_players(self, params):
        return self.game.players

    def add_player(self, params):
        self.game.add_player(params["player name"])

    def start_game(self, params):
        self.game.initialize_round()

    def get_player(self, params):
        self.game.get_player(params["player name"])

    def player_action(self, params):
        result = self.game.player_action(params)
        self.get_game_state(None)
        return result

    def get_game_state(self, params):
        # table = self.game.table
        # players = self.game.players
        # self.current_player = self.game.get_current_player()
        # round_no = self.game.round_no
        # available_actions = self.game.get_current_available_actions()
        # pot = self.game.pot
        game_state={
            "Table": self.game.table,
            "Players": self.game.players,
            "Current player": self.game.current_player,
            "Available actions": self.game.get_current_available_actions(),
            "Round no": self.game.round_no,
            "Pot": self.game.pot,
            "Game results": self.game.game_results
        }
        return game_state

    # def check_game(self):
    #     return self.game.finished
    
    # def get_current_player(self):
    #     return self.game.get_current_player()



# game_service = GameService()
# game_service.perform_action("Add player", {"player name": "Pawel"})
# game_service.perform_action("Add player", {"player name": "Karolina"})
# game_service.perform_action("Add player", {"player name": "Tyna"})
# game_service.perform_action("Start game", None)

# while not game_service.game.finished:
#     print(game_service.perform_action("Get state", None))
#     game_service.perform_action("Next move", None)
    
