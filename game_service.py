from game import Game
from player import Player
from jsonable import Jsonable
import command
import hashlib
import json


class GameServiceLocal():

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

    def setup_api(self):
        import game_server
        game_server.game_service = self

    # def perform_action(self, action_name, action_params):
    #     return self.game_actions[action_name](action_params)
        
    def get_players(self, params):
        return self.game.players

    def add_player(self, params):
        # self.game.add_player(params["player name"])
        self.game.add_player(params)

    def start_game(self, params):
        self.game.initialize_round()

    def get_player(self, params):
        self.game.get_player(params["player name"])

    def set_player_ready(self, params):
        return self.game.set_player_ready(params)

    def player_action(self, cmd):
        command_parser = command.CommandParser(self.game_state["Available actions"])
        return command_parser.parse_and_exetute(cmd, self.game.player_action)

    def get_game_results(self):
        result = self.game.game_results_rich
        return result

    def hash_list(self, input_list):
        result = ""
        for subval in input_list:
            if isinstance(subval, dict):
                result += self.hash_dict(subval)
            elif isinstance(subval, Jsonable):
                result += self.hash_dict(dict(subval))
            else:
                result += str(subval)
        return result

    def hash_dict(self, input_dict):
        result = ""
        for attr, value in input_dict.items():
            result+=attr
            if isinstance(value, list):
                result += self.hash_list(value)
            elif isinstance(value, dict):
                result += self.hash_dict(value)            
            elif isinstance(value, Jsonable):
                result += self.hash_dict(dict(value))
            else:
                result += str(value)
        return result


    def hash_game_state(self):
        result = ""
        for attr, value in self.game_state.items():
            result+=attr
            if isinstance(value, list):
                result += self.hash_list(value)
            elif isinstance(value, dict):
                result += self.hash_dict(value)
            elif isinstance(value, Jsonable):
                result += self.hash_dict(dict(value))
            else:
                result += str(value)
        return result




    def get_game_state(self, params):
        if self.game.started:
            self.game_state={
                "State": "Started",
                "Table": self.game.table,
                "Players": self.game.players,
                "Current player": self.game.current_player.name,
                "Available actions": self.game.get_current_available_actions(),
                "Round no": self.game.round_no,
                "Pot": self.game.pot,
                "Game results": {}
            }
        if not self.game.started:
            self.game_state={
                "State": "Waiting",
                "Table": {},
                "Players": self.game.players,
                "Current player": {},
                "Available actions": {},
                "Round no": {},
                "Pot": {},
                "Game results": self.get_game_results()
            }

        hash_value = self.hash_game_state()
        self.game_state["Hash value"] = hashlib.md5(hash_value.encode('utf-8')).hexdigest()

        return self.game_state
    
