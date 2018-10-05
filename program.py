from game_service import GameService


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

while not game_service.game.finished:
    print(game_service.perform_action("Get state", None))
    game_service.perform_action("Next move", None)