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
from jsonconvert import JsonConvert

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
    # return_game_state={
    #     "Table": list(map(lambda c: dict(c), game_state.table)),
    #     "Players": list(map(lambda p: dict(p), game_state.players)),
    #     "Current player": game_state.current_player,
    #     "Available actions": list(map(lambda a: dict(a), game_state.available_actions)),
    #     "Round no": game_state.round_no,
    #     "Pot": game_state.pot,
    #     "Game results": game_state.game_results
    # }
    return JsonConvert.ToJSON(game_state)
    # return jsonify(return_game_state)


@app.route('/player_action', methods=['POST'])
def post_player_action():
    content = request.get_json()
    # print(content["Action name"])
    # print(content["Action params"])
    result = game_service.player_action(content["Action params"])
    return jsonify(result)

@app.route('/set_player_ready', methods=['POST'])
def set_player_ready():
    content = request.get_json()
    result = game_service.set_player_ready(content['Name'])
    return jsonify(result)

@app.route('/add_player', methods=['POST'])
def add_player():
    content = request.get_json()
    result = game_service.add_player(content['Name'])
    return jsonify(result)
    
atexit.register(stop_server)
server_thread = threading.Thread(target=start_server)
server_thread.start()
time.sleep(1)



