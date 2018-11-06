from player import Player
from jsonconvert import JsonConvert

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
    if not my_player.ready:
        return True
    return False

class PlayerActionAvailability():

    def __init__(self, name, key, func, has_value):
        self.name = name
        self.key = key
        self.func = func
        self.has_value = has_value

    def to_player_action(self):
        return PlayerAction(self.name, self.key, self.has_value)

@JsonConvert.register
class PlayerAction():
    def __init__(self, name="", key="", has_value=None):
        self.name = name
        self.key = key
        self.has_value = has_value


def get_available_actions(players, current_player, my_player):
    player_actions = [
        PlayerActionAvailability("Check", "C", check_available, False),
        PlayerActionAvailability("Fold", "F", fold_available, False),
        PlayerActionAvailability("Bet", "B", bet_available, True),
        PlayerActionAvailability("Raise", "R", raise_available, True),
        PlayerActionAvailability("Call", "C", call_available, False),
        PlayerActionAvailability("All in", "A", all_in_available, False),
        PlayerActionAvailability("Confirm ready", "Y", confirm_ready_available, False)
    ]
    return list(map(lambda p: p.to_player_action(), filter(lambda pa: pa.func(players, current_player, my_player), player_actions)))



