from flask import Flask
from flask import request
from flask import jsonify
from game import Game
from game_service import GameServiceLocal
import threading
import time
import atexit
import logging
import json

game_service: GameServiceLocal = None
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def start_server():
    print('Server module running.')
    app.run(host='127.0.0.1', port=5000)

def stop_server():
    print('Stopping server')

@app.route('/')
def index():
    return "Python poker game."

@app.route('/game_state')
def get_game_state():
    game_state = game_service.get_game_state(None)
    return_game_state={
        "Table": list(map(lambda c: dict(c), game_state["Table"])),
        "Players": list(map(lambda p: dict(p), game_state["Players"])),
        "Current player": dict(game_state["Current player"]),
        "Available actions": list(map(lambda a: dict(a), game_state["Available actions"])),
        "Round no": game_state["Round no"],
        "Pot": game_state["Pot"],
        "Game results": game_state["Game results"]
    }
    return jsonify(return_game_state)


@app.route('/perform_action', methods=['POST'])
def post_player_action():
    content = request.get_json()
    print(content["Action name"])
    print(content["Action params"])
    result = game_service.perform_action(content["Action name"],content["Action params"])
    return jsonify(result)
    
atexit.register(stop_server)
server_thread = threading.Thread(target=start_server)
server_thread.start()
time.sleep(1)



