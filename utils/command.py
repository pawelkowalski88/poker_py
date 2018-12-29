from utils.available_action_helper import PlayerAction

"""Defines actions that may be taken by the player. Contains display name, letter code and information 
if the action takes parameters.
"""
player_actions = [
    PlayerAction("Check", "C", False),
    PlayerAction("Fold", "F", False),
    PlayerAction("Bet", "B", True),
    PlayerAction("Raise", "R", True),
    PlayerAction("Call", "C", True),
    PlayerAction("All in", "A", False),
    PlayerAction("Confirm ready", "Y", False)
]


class CommandParser:
    """Responsible for parsing, validating and executing game commands.

    """

    def __init__(self, available_commands):
        """Initializes a new instance of the CommandParser class.

        :param available_commands: The collection of the available commands.
        """
        self.available_commands = available_commands

    def parse_and_execute(self, command: str, function, player=None):
        """Searches for a command by its letter code, checks the number of parameters. If the command is valid
        the given function is executed.

        :param command: The command text coming from the user.
        :param function: The function to be executed when the command get validated properly.
        :param player: The reference to the player to be passed to the executed function.
        :return: Returns the validation or function execution result. If the validation fails,
        returns the validation error message. If the validation is passed, re-returns what the function returns.
        """

        elements = command.split(' ')

        try:
            cmd = next(filter(lambda a: a.key.lower() == elements[0], self.available_commands))
        except StopIteration:
            return {"result": "ERROR", "error_message": "No such command!"}
        except TypeError:
            return {"result": "ERROR", "error_message": "Internal error"}

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
