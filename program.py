from game_service import GameService

def print_game_state(game_service):
    game_state = game_service.perform_action("Get state", None)
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
    


game_service = GameService()


game_service.perform_action("Add player", {"player name": "Pawel"})
game_service.perform_action("Add player", {"player name": "Karolina"})

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
    print_game_state(game_service)
    choice = input("C - call, B - bet, F - fold, R - raise")
    action_params = {'Action name': ""}
    if choice.lower() == 'b':
        amount = input("What amount?")
        action_params = {'Action name': 'Bet', 'Amount': amount}
    if choice.lower() == 'c':
        max_bet = game_service.game.max_bet
        action_params = {'Action name': 'Call', 'Max bet': max_bet}
    if choice.lower() == 'r':
        max_bet = game_service.game.max_bet
        amount = input("What amount to raise?")
        action_params = {'Action name': 'Raise', 'Max bet': max_bet, 'Amount': amount}
    #game_service.perform_action("Player action", {"Action name": "Bet", "Amount": 100})
    game_service.perform_action("Player action", action_params)

print_game_state(game_service)

for r in game_service.game.get_game_results():
    print(r["Name"] + " " + r["Best hand"][0] + " " + r["Best hand"][1])
    # for h in r["Hands"]:
    #     print(h)
