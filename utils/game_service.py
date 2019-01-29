from utils.game import Game
from utils.game_state import GameState
from utils import command


class GameServiceLocal:

    def __init__(self):
        self.game = Game()
        self.game.add_player("Pawel")
        self.game.add_player("Zenek")
        self.game_state = None
        self.my_player = None
        print("Game instance created.")

    def setup_api(self):
        import utils.game_server as game_server
        game_server.game_service = self

    def get_players(self, params):
        return self.game.players

    def add_player(self, params):
        if params in list(map(lambda p: p.name, self.game.players)):
            return {'result': 'ERROR', 'error_message': 'A player of the same name already exists.'}

        self.my_player = self.game.add_player(params)
        return {'result': 'OK', 'payload': self.my_player}

    def player_action(self, cmd, player):
        command_parser = command.CommandParser(self.game.get_current_available_actions(player))
        return command_parser.parse_and_execute(cmd, self.game.player_action, player)

    def get_game_results(self):
        result = self.game.game_results_rich
        return result

    def get_game_state(self, player):
        if len(list(filter(lambda p: p.name == player, self.game.players))) == 0:
            return {'result': 'ERROR', 'error_message': 'This player does not exist.'}

        if self.game.current_player:
            current_player_name = self.game.current_player.name
        else:
            current_player_name = ""

        if self.game.started:
            self.game_state = GameState(
                "Started",
                self.game.table,
                self.game.get_players(player),
                current_player_name,
                self.game.get_current_available_actions(player),
                self.game.round_no,
                self.game.pot,
                None
            )
        elif not self.game.finished:
            self.game_state = GameState(
                state="Waiting",
                table=self.game.table,
                players=self.game.players,
                current_player=current_player_name,
                available_actions=self.game.get_current_available_actions(player),
                round_no=self.game.round_no,
                pot=self.game.pot,
                game_results=self.get_game_results()
            )
        else:
            self.game_state = GameState(
                state="Finished",
                table=self.game.table,
                players=self.game.players,
                current_player=current_player_name,
                available_actions=[],
                round_no=self.game.round_no,
                pot=self.game.pot,
                game_results=self.get_game_results()
            )

        return {'result': 'OK', 'payload': self.game_state}
