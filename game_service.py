from game import Game
from player import Player
import command


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
        self.game_state = None

    def perform_action(self, action_name, action_params):
        return self.game_actions[action_name](action_params)
        
    def get_players(self, params):
        return self.game.players

    def add_player(self, params):
        self.game.add_player(params["player name"])

    def start_game(self, params):
        self.game.initialize_round()

    def get_player(self, params):
        self.game.get_player(params["player name"])

    def player_action(self, cmd):

        command_parser = command.CommandParser(self.game_state["Available actions"])
        return command_parser.parse_and_exetute(cmd, self.game.player_action)

    def get_game_state(self, params):
        self.game_state={
            "Table": self.game.table,
            "Players": self.game.players,
            "Current player": self.game.current_player,
            "Available actions": self.game.get_current_available_actions(),
            "Round no": self.game.round_no,
            "Pot": self.game.pot,
            "Game results": self.game.game_results
        }
        return self.game_state
    
