from available_action_helper import PlayerAction

class CommandParser():

    def __init__(self, available_commands):
        self.available_commands = available_commands

    def parse_and_exetute(self, command: str, function, player=None):
        elements = command.split(' ')

        try:
            cmd = next(filter(lambda a: a.key.lower() == elements[0], self.available_commands))
        except (StopIteration):
            return {"result": "ERROR", "error_message": "No such command!"}

        if cmd.has_value:
            if len(elements) > 1:
                value = elements[1]
            else:
                return {"result": "ERROR", "error_message": f"The {cmd.name} command needs a parameter!"}
        else:
            if len(elements) > 1:
                return {"result": "ERROR", "error_message": f"Too many parameters for {cmd.name} command!"}
            else:
                value = None
        
        return function({"Action name": cmd.name, "Value": value, "Player": player})


    def execute(self, params):
        print(f"Name: {params['Action name']}, Value: {params['Value']}")
        return {"result": "OK"}

player_actions = [
    PlayerAction("Check", "C", False),
    PlayerAction("Fold", "F", False),
    PlayerAction("Bet", "B", True),
    PlayerAction("Raise", "R", True),
    PlayerAction("Call", "C", True),
    PlayerAction("All in", "A", False),
    PlayerAction("Confirm ready", "Y", False)
]