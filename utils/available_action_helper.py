from utils.jsonconvert import JsonConvert


def check_available(players, current_player, my_player):
    if not current_player:
        return False
    if not current_player.ready:
        return False
    max_bet = max(map(lambda p: p.bet, players))
    if current_player.bet == max_bet:
        return True
    return False


def fold_available(players, current_player, my_player):
    if not current_player:
        return False
    if not current_player.ready:
        return False
    return True


def bet_available(players, current_player, my_player):
    if not current_player:
        return False
    if not current_player.ready:
        return False
    max_bet = max(map(lambda p: p.bet, players))
    if max_bet == 0:
        return True
    return False


def raise_available(players, current_player, my_player):
    if not current_player:
        return False
    if not current_player.ready:
        return False
    max_bet = max(map(lambda p: p.bet, players))
    if max_bet > 0 and max_bet < current_player.balance + current_player.bet:
        return True
    return False


def call_available(players, current_player, my_player):
    if not current_player:
        return False
    if not current_player.ready:
        return False
    max_bet = max(map(lambda p: p.bet, players))
    if current_player.bet < max_bet and max_bet < (current_player.bet + current_player.balance):
        return True
    return False


def all_in_available(players, current_player, my_player):
    if not current_player:
        return False
    if not current_player.ready:
        return False
    max_bet = max(map(lambda p: p.bet, players))
    if max_bet >= (current_player.bet + current_player.balance) and current_player.balance > 0:
        return True
    return False


def confirm_ready_available(players, current_player, my_player):
    if not my_player.ready and my_player.active:
        return True
    return False


class PlayerActionAvailability:
    """Represents a player action with a function stating if the action should be available to the player
    under the specific conditions.

    """

    def __init__(self, name, key, func, has_value):
        """Initializes a new instance of the PlayerActionAvailability class.

        :param name: The display name of the action.
        :param key: The shortcut key of the function. For example for "bet" the key might me 'B'.
        :param func: The function that returns if the function should be available in current conditions.
        :param has_value: True if the command should have a value parameter.
        """
        self.name = name
        self.key = key
        self.func = func
        self.has_value = has_value

    def to_player_action(self):
        """Contverts the current instance to a PlayerAction object with the current parameters.

        :return: A PlayerAction object based on the current instance.
        """
        return PlayerAction(self.name, self.key, self.has_value)


@JsonConvert.register
class PlayerAction:
    """Represents a player action.

    """
    def __init__(self, name="", key="", has_value=None):
        """Initializes a new instance of the PlayerAction class.

        :param name: The display name of the action.
        :param key: The shortcut key of the function. For example for "bet" the key might me 'B'.
        :param has_value: True if the command should have a value parameter.
        """
        self.name = name
        self.key = key
        self.has_value = has_value


def get_available_actions(players, current_player, my_player):
    """Checks all the palyer actions and returns the list of the available ones.

    :param players: The players collection.
    :param current_player: The player whose turn it is right now.
    :param my_player: The player who is asking for the available actions.
    :return: The list of the actions available.
    """

    player_actions = [
        PlayerActionAvailability("Check", "C", check_available, False),
        PlayerActionAvailability("Fold", "F", fold_available, False),
        PlayerActionAvailability("Bet", "B", bet_available, True),
        PlayerActionAvailability("Raise", "R", raise_available, True),
        PlayerActionAvailability("Call", "C", call_available, False),
        PlayerActionAvailability("All in", "A", all_in_available, False),
        PlayerActionAvailability("Confirm ready", "Y", confirm_ready_available, False)
    ]
    return list(map(lambda p: p.to_player_action(),
                    filter(lambda pa: pa.func(players, current_player, my_player), player_actions)))



