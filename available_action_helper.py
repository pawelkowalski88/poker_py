from player import Player

def check_available(players, current_player):
    max_bet = max(map(lambda p: p.bet, players))
    if current_player.bet == max_bet:
        return True
    return False

def fold_available(players, current_player):
    return True

def bet_available(players, current_player):
    max_bet = max(map(lambda p: p.bet, players))
    if max_bet == 0:
        return True
    return False

def raise_available(players, current_player):
    max_bet = max(map(lambda p: p.bet, players))
    if max_bet > 0 and max_bet < current_player.balance + current_player.bet:
        return True
    return False

def call_available(players, current_player):
    max_bet = max(map(lambda p: p.bet, players))
    if current_player.bet < max_bet and max_bet < (current_player.bet + current_player.balance):
        return True
    return False

def all_in_available(players, current_player):
    max_bet = max(map(lambda p: p.bet, players))
    if max_bet >= (current_player.bet + current_player.balance) and current_player.balance > 0:
        return True
    return False

class PlayerAction():

    def __init__(self, name, key, func):
        self.name = name
        self.key = key
        self.func = func

def get_available_actions(players, current_player):
    player_actions = [
        PlayerAction("Check", "C", check_available),
        PlayerAction("Fold", "F", fold_available),
        PlayerAction("Bet", "B", bet_available),
        PlayerAction("Raise", "R", raise_available),
        PlayerAction("Call", "C", call_available),
        PlayerAction("All in", "A", all_in_available)
    ]
    result = list(filter(lambda pa: pa.func(players, current_player), player_actions))
    return result

players = []
players.append(Player("Pawel"))
players.append(Player("Karolina"))

players[0].bet = 0
players[1].bet = 5000
players[0].balance = 1200

print(list(map(lambda pa: pa.name + " - " + pa.key, get_available_actions(players, players[0]))))

