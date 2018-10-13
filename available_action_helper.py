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
    if max_bet > 0:
        return True
    return False

