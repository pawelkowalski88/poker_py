from jsonconvert import JsonConvert
from table import Table
import hashlib

@JsonConvert.register
class GameState(object):

    def __init__(
            self, state="Waiting", table=None, players=None, 
            current_player="", available_actions=None, 
            round_no=None, pot=None, game_results=None):
        self.state = state
        self.table = table
        self.players = players
        self.current_player = current_player
        self.available_actions = available_actions
        self.round_no = round_no
        self.pot = pot
        self.game_results = game_results
        self.hash_value = self.calculate_hash_value()

    @classmethod
    def empty_game_state(self):
        return GameState("", None, None, "", None, 0, 0, None)

    def calculate_hash_value(self):
        asJson = JsonConvert.ToJSON(self)
        return hashlib.md5(asJson.encode('utf-8')).hexdigest()
        #return 1

    