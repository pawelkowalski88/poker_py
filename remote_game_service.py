import requests
from table import Table
from card import Card
import json
from collections import namedtuple
from jsonconvert import JsonConvert

class RemoteGameService():

    def __init__(self, base_url):
        self.base_url = base_url

    def add_player(self, params):
        player_data = {"Name": params}
        request = requests.post(self.base_url + '/add_player', data=player_data)
        result = request.json()
        return result

    def get_game_state(self):
        request = requests.get(self.base_url + '/game_state')
        data = request.text
        # result = json.loads(data, object_hook=lambda d: namedtuple('X', self.extract_fields(d.keys()))(*d.values()))
        result = JsonConvert.FromJSON(data)
        return result

    def extract_fields(self, field_names):
        result = list(map(lambda f: f.replace(" ","_").lower(), field_names))
        return result

    # def player_action
