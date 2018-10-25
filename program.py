from game_service import GameServiceLocal
import os

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
    game_service = GameServiceLocal()

    # game_service.setup_api()

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
    print("!!!GAME STARTED!!!")
    print()

    game_service.perform_action("Start game", None)

    while not game_service.game.finished:
        game_state = get_game_state(game_service)
        print_game_state(game_state)

        while True:
            command = input(print_player_actions(game_state["Available actions"]))
            if command == 'exit':
                os._exit(1)
            result = game_service.perform_action("Player action", command)
            if result['result'] == 'ERROR':
                print("ERROR: " + result['error_message'])
            if result['result'] == 'OK':
                break

    print_game_state(get_game_state(game_service))

    for r in game_service.game.get_game_results():
        print(r["Name"] + " " + r["Best hand"][0] + " " + r["Best hand"][1])
