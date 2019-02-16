import requests
from pokerthegame.api.utils import JsonConvert
from pokerthegame.api.utils import Dummy


class RemoteGameService:

    def __init__(self, base_url):
        self.base_url = base_url

    def add_player(self, params):
        request = requests.post(self.base_url + '/add_player', json={"Name": params})
        result = request.text
        return JsonConvert.FromJSON(result)

    def get_game_state(self, player):
        request = requests.post(self.base_url + '/game_state', json=player)
        data = request.text
        # result = json.loads(data, object_hook=lambda d: namedtuple('X', self.extract_fields(d.keys()))(*d.values()))
        result = JsonConvert.FromJSON(data)
        if isinstance(result.game_results, Dummy):
            result.game_results = None
        return result

    def set_player_ready(self):
        pass

    def extract_fields(self, field_names):
        result = list(map(lambda f: f.replace(" ","_").lower(), field_names))
        return result

    def player_action(self, command, player_name):
        request = requests.post(self.base_url + '/player_action', json={"Action name": "Player action", "Action params": command, "Player": player_name})
        return request.json()

