from pokerthegame.api.utils import JsonConvert


@JsonConvert.register
class Dummy:
    def __init__(self):
        pass
