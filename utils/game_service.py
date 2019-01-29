from utils.game import Game
from utils.game_state import GameState
from utils import command


class GameServiceLocal:

    def __init__(self):
        self.__game = Game()
        self.__game.add_player("Pawel")
        self.__game.add_player("Zenek")
        self.__game_state = None
        self.__my_player = None
        print("Game instance created.")

    def setup_api(self):
        import utils.game_server as game_server
        game_server.game_service = self

    def get_players(self, params):
        return self.__game.players

    def add_player(self, params):
        if params in list(map(lambda p: p.name, self.__game.players)):
            return {'result': 'ERROR', 'error_message': 'A player of the same name already exists.'}

        self.__my_player = self.__game.add_player(params)
        return {'result': 'OK', 'payload': self.__my_player}

    def player_action(self, cmd, player):
        command_parser = command.CommandParser(self.__game.get_current_available_actions(player))
        return command_parser.parse_and_execute(cmd, self.__game.player_action, player)

    def get_game_results(self):
        result = self.__game.game_results_rich
        return result

    def get_game_state(self, player):
        if len(list(filter(lambda p: p.name == player, self.__game.players))) == 0:
            return {'result': 'ERROR', 'error_message': 'This player does not exist.'}

        if self.__game.current_player:
            current_player_name = self.__game.current_player.name
        else:
            current_player_name = ""

        if self.__game.started:
            self.__game_state = GameState(
                "Started",
                self.__game.table,
                self.__game.get_players(player),
                current_player_name,
                self.__game.get_current_available_actions(player),
                self.__game.round_no,
                self.__game.pot,
                None
            )
        elif not self.__game.finished:
            self.__game_state = GameState(
                state="Waiting",
                table=self.__game.table,
                players=self.__game.players,
                current_player=current_player_name,
                available_actions=self.__game.get_current_available_actions(player),
                round_no=self.__game.round_no,
                pot=self.__game.pot,
                game_results=self.get_game_results()
            )
        else:
            self.__game_state = GameState(
                state="Finished",
                table=self.__game.table,
                players=self.__game.players,
                current_player=current_player_name,
                available_actions=[],
                round_no=self.__game.round_no,
                pot=self.__game.pot,
                game_results=self.get_game_results()
            )

        return {'result': 'OK', 'payload': self.__game_state}
