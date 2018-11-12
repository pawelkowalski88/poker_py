from game import Game
from player import Player
from game_state import GameState
import command
import hashlib
import json
from dummy import Dummy


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
        self.my_player = None

    def setup_api(self):
        import game_server
        game_server.game_service = self

    # def perform_action(self, action_name, action_params):
    #     return self.game_actions[action_name](action_params)
        
    def get_players(self, params):
        return self.game.players

    def add_player(self, params):
        # self.game.add_player(params["player name"])
        self.my_player = self.game.add_player(params)
        return self.my_player

    def start_game(self, params):
        self.game.initialize_round()

    def get_player(self, params):
        self.game.get_player(params["player name"])

    def set_player_ready(self, params):
        return self.game.set_player_ready(params)

    def player_action(self, cmd, player):
        command_parser = command.CommandParser(self.game.get_current_available_actions(player))
        return command_parser.parse_and_exetute(cmd, self.game.player_action, player)

    def get_game_results(self):
        result = self.game.game_results_rich
        return result

    def get_available_actions(self, player):
        return self.game.get_current_available_actions(player)

    def get_game_state(self, params):
        if self.game.current_player:
            current_player_name = self.game.current_player.name
        else:
            current_player_name = ""

        my_player = params["player"]

        if self.game.started:
            self.game_state = GameState(
                "Started",
                self.game.table,
                self.game.get_players(my_player),
                current_player_name,
                self.game.get_current_available_actions(my_player),
                self.game.round_no,
                self.game.pot,
                None
            )
        elif not self.game.finished:
            self.game_state = GameState(
                state = "Waiting",
                table = self.game.table,
                players = self.game.players,
                current_player = current_player_name,
                available_actions = self.game.get_current_available_actions(my_player),
                round_no = self.game.round_no,
                pot = self.game.pot,
                game_results = self.get_game_results()
            )
        else:
            self.game_state = GameState(
                state = "Finished",
                table = self.game.table,
                players = self.game.players,
                current_player = current_player_name,
                available_actions = [],
                round_no = self.game.round_no,
                pot = self.game.pot,
                game_results = self.get_game_results()
            )


        return self.game_state
    
