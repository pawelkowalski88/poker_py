from utils.jsonconvert import JsonConvert


@JsonConvert.register
class Dummy:
    def __init__(self):
        pass
