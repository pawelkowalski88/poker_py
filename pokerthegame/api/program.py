import os
import time
import threading
from pokerthegame.api.utils import RemoteGameService
from pokerthegame.api.utils import GameServiceLocal
from pokerthegame.api.utils import GameState

game_state = None
stop_refreshing = False
game_state_refreshed = False


def print_game_state(game_state):
    clear_screen()
    print()
    print()
    table = game_state.table
    players = game_state.players
    cur_player = game_state.current_player
    if table:
        print("Cards on the table:")
        card_str = []
        card_str = [c.__str__() for c in table]
        print("".join(card_str))
    else:
        print("No cards on the table")
    print()
    print("Pot: " + str(game_state.pot))
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
    if player_actions:
        for a in player_actions:
            result += a.name + " - " + a.key + " "

        return result
    return ""


def print_ready_players_and_results(game_state):
    clear_screen()
    print()
    table = game_state.table
    players = game_state.players
    cur_player = game_state.current_player
    if table:
        print("Cards on the table:")
        card_str = []
        card_str = [c.__str__() for c in table]
        print("".join(card_str))
    else:
        print("No cards on the table")
    print()
    print("Pot: " + str(game_state.pot))
    if players:
        print("Players in game:")
        for p in players:
            if p.active:
                print(p)
    else:
        print("No players in game")
    print()
    for r in game_state.game_results.results:
        # print(r["name"] + " " + r["best_hand"]["name"] + " " + r["best_hand"]["value"])
        print(r["name"] + " " + r["best_hand"]["name"] + " " + r["best_hand"]["value"])

    print()
    print()

    for p in game_state.players:
        if p.active:
            print(p.name + " " + player_ready_as_str(p.ready, p.active))
    print()


def clear_screen():
    print("\033[H\033[J")


def player_ready_as_str(ready, active):
    if active:
        if ready:
            return "Ready"
        return "Not ready"
    else:
        return "Out"


def refresh_player_command():
    global game_state_refreshed
    global stop_refreshing
    if game_state_refreshed:
        if game_state.current_player == my_player.name or not game_state.current_player and not my_player.ready:
            while True:
                if game_state.available_actions:
                    command = input("").strip()
                    stop_refreshing = True
                    game_state_refreshed = False
                    if command == 'exit':
                        os._exit(1)
                    result = game_service.player_action(command, my_player.name)
                    if result['result'] == 'ERROR':
                        print("ERROR: " + result['error_message'])
                    if result['result'] == 'OK':
                        stop_refreshing = False
                        break
                else:
                    break


def refresh_game_state():
    global game_state
    global game_state_refreshed
    global stop_refreshing
    while True:
        if not stop_refreshing:
            game_state_old = game_state
            game_state = game_service.get_game_state({"player": my_player.name})
            if game_state_old.hash_value != game_state.hash_value:
                if game_state.state == "Waiting":
                    print_ready_players_and_results(game_state)
                elif game_state.state == "Finished":
                    print_ready_players_and_results(game_state)
                    print("GAME OVER")
                    active_players = list(filter(lambda p: p.balance > 0, game_state.players))
                    print("The winner is " + active_players[0].name)
                    return
                else:
                    print_game_state(game_state)
                if game_state.current_player == my_player.name or not game_state.current_player and not my_player.ready:
                    print(print_player_actions(game_state.available_actions))
            game_state_refreshed = True
        time.sleep(0.5)


while True:
    clear_screen()
    game_mode = input("Host - H, Join - J, Exit - E:")
    if game_mode.lower() == "h":
        game_service = GameServiceLocal()
        game_service.setup_api()
        break
    elif game_mode.lower() == "j":
        game_service = RemoteGameService("http://localhost:5000")
        break
    elif game_mode.lower() == "e":
        os._exit(1)
game_state = GameState.empty_game_state()

my_player_name = input("Please enter your name:")
my_player = game_service.add_player(my_player_name)

thread_counter = 0
input_thread = threading.Thread(target=refresh_game_state)
input_thread.daemon = True
input_thread.start()
time.sleep(0.1)

# while not game_service.game.finished:

while True:
    refresh_player_command()
    if game_state.state == "Finished":
        stop_refreshing = True
        if isinstance(game_service, RemoteGameService):
            print("Connection to server terminated")
            break

# print_game_state(game_service.get_game_state(None))

# for r in game_service.game.get_game_results():
#     print(r["Name"] + " " + r["Best hand"][0] + " " + r["Best hand"][1])
