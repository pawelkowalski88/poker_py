from game_service import GameServiceLocal
from player import Player
import os, time, hashlib

# def get_game_state(game_service):
#     return game_service.get_game_state(None)

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
        if cur_player == my_player.name:
            print("It is your turn, " + str(cur_player))
        else:
            print(str(cur_player) + "'s turn.")
    print()


def print_player_actions(player_actions):
    result = ""
    for a in player_actions:
        result += a.name + " - " + a.key + " "

    return result

def print_ready_players_and_results(game_state):

    print()
    for r in game_state["Game results"]:
        print(r["Name"] + " " + r["Best hand"]["Name"] + " " + r["Best hand"]["Value"])

    print()

    for p in game_state['Players']:
        print(p.name + " " + player_ready_as_str(p.ready))
    print()





def player_ready_as_str(ready):
    if ready:
        return "Ready"
    return "Not ready"


if __name__ == '__main__':   
    game_service = GameServiceLocal()

    game_service.setup_api()

    game_service.add_player("Pawel")
    game_service.add_player("Karolina")

    my_player = game_service.game.players[0]

    game_service.start_game(None)        

    game_service.set_player_ready("Pawel")
    game_service.set_player_ready("Karolina")

    game_state = {"Hash value": 0}
    while not game_service.game.finished:

        game_state_old = game_state
        game_state = game_service.get_game_state(None)
        if game_state_old["Hash value"] != game_state["Hash value"]:
            if game_state["State"] == "Waiting":
                print_ready_players_and_results(game_state)
            else:
                print_game_state(game_state)

        time.sleep(1)
        
        if game_state['Current player'] == my_player.name:
            while True:
                command = input(print_player_actions(game_state["Available actions"])).strip()
                if command == 'exit':
                    os._exit(1)
                result = game_service.player_action(command)
                if result['result'] == 'ERROR':
                    print("ERROR: " + result['error_message'])
                if result['result'] == 'OK':
                    break

    print_game_state(game_service.get_game_state(None))

    for r in game_service.game.get_game_results():
        print(r["Name"] + " " + r["Best hand"][0] + " " + r["Best hand"][1])

