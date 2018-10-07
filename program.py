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
    if players:
        print("Players in game:")
        for p in players:
            print(p)
    else:
        print("No players in game")
    if cur_player:
        print("It is your turn, " + str(cur_player))
    


game_service = GameService()

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
    game_service.perform_action("Next move", None)