from pokerthegame.api.utils import JsonConvert


@JsonConvert.register
class GameResultsCollection():

    def __init__(self, results = []):
        self.results = results