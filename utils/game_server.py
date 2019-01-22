from flask import Flask
from flask import request
from flask import jsonify
from utils.game_service import GameServiceLocal
import threading
import time
import atexit
import logging
from utils.jsonconvert import JsonConvert

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


@app.route('/api/game/<player_name>')
def get_game(player_name):
    game_state = game_service.get_game_state(player_name)
    result = JsonConvert.ToJSON(game_state)
    return result


@app.route('/api/game', methods=['POST'])
def post_player_action():
    content = request.get_json()
    result = game_service.player_action(content["Action params"], content["Player"])
    return jsonify(result)


@app.route('/api/tables')
def get_tables():
    tables = []
    tables.append({"Name": "test table"})
    return jsonify(tables)


@app.route('/api/tables/<table_id>')
def get_table(table_id):
    return JsonConvert.ToJSON({"Name": "test table", "Players": game_service.get_players(None)})



# @app.route('/set_player_ready', methods=['POST'])
# def set_player_ready():
#     content = request.get_json()
#     result = game_service.set_player_ready(content['Name'])
#     return jsonify(result)
#
#
# @app.route('/add_player', methods=['POST'])
# def add_player():
#     content = request.get_json()
#     result = game_service.add_player(content['Name'])
#     return JsonConvert.ToJSON(result)


atexit.register(stop_server)
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()
time.sleep(1)



