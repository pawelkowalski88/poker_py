from game_service import GameService

def get_game_state(game_service):
    return game_service.perform_action("Get state", None)

def print_game_state(game_state):
    print()
    print()
    table = game_state["Table"]
    players = game_state["Players"]
    cur_player = game_state["Current player"]
    if table:
        print("Cards on the table:")
        card_str = []
        card_str = [c.__str__() for c in table]
        print("".join(card_str))
    else:
        print("No cards on the table")
    print()
    print("Pot: " + str(game_state["Pot"]))
    if players:
        print("Players in game:")
        for p in players:
            print(p)
    else:
        print("No players in game")
    print()
    if cur_player:
        print("It is your turn, " + str(cur_player.name))
    print()


def print_player_actions(player_actions):
    result = ""
    for a in player_actions:
        result += a.name + " - " + a.key + " "

    return result


if __name__ == '__main__':   
    game_service = GameService()


    game_service.perform_action("Add player", {"player name": "Pawel"})
    game_service.perform_action("Add player", {"player name": "Karolina"})

    game_service.game.players[0].balance = 3000

    while True:
        print("P - nowy gracz")
        print("G - graj")
        choice = input("?")

        if choice.upper() == "P":
            player_name = input("Podaj imie gracza:")
            game_service.perform_action("Add player", {"player name": player_name})
        
        if choice.upper() == "G":
            break

    print("\n")
    print("!!!ROZPOCZYNAMY GRE!!!")
    print("\n")


    game_service.perform_action("Start game", None)
    while not game_service.game.finished:
        game_state = get_game_state(game_service)
        print_game_state(game_state)
        #choice = input("C - call, B - bet, F - fold, R - raise")
        choice = input(print_player_actions(game_state["Available actions"]))
        action_params = {'Action name': ""}
        if choice.lower() == 'b':
            amount = input("What amount?")
            action_params = {'Action name': 'Bet', 'Amount': amount}
        elif choice.lower() == 'c':
            max_bet = game_service.game.max_bet
            action_params = {'Action name': 'Call', 'Max bet': max_bet}
        elif choice.lower() == 'f':
            action_params = {'Action name': 'Fold'}
        elif choice.lower() == 'r':
            amount = input("What amount to raise?")
            action_params = {'Action name': 'Raise', 'Amount': amount}    
        elif choice.lower() == 'a':
            action_params = {'Action name': 'All in'}
        elif choice.lower() == 'y':
            action_params = {'Action name': 'Confirm ready'}
        else:
            continue
        #game_service.perform_action("Player action", {"Action name": "Bet", "Amount": 100})
        result = game_service.perform_action("Player action", action_params)
        if result['result'] == 'ERROR':
            print("ERROR: " + result['error_message'])

    print_game_state(get_game_state(game_service))

    for r in game_service.game.get_game_results():
        print(r["Name"] + " " + r["Best hand"][0] + " " + r["Best hand"][1])
        # for h in r["Hands"]:
        #     print(h)
