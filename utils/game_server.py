from flask import Flask
from flask import request
from flask import jsonify, abort, make_response
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
    if game_state['result'] == 'OK':
        return JsonConvert.ToJSON(game_state["payload"])
    else:
        abort(make_response(jsonify(game_state), 404))


@app.route('/api/game', methods=['POST'])
def post_player_action():
    content = request.get_json()
    result = game_service.player_action(content["Action params"], content["Player"])

    if result['result'] == 'OK':
        return JsonConvert.ToJSON(result)
    else:
        abort(make_response(jsonify(result), 400))


@app.route('/api/tables')
def get_tables():
    tables = []
    tables.append({"Name": "test table"})
    return jsonify(tables)


@app.route('/api/tables/<int:table_id>')
def get_table(table_id):
    print(table_id)
    if table_id == 1:
        return JsonConvert.ToJSON({"Name": "test table", "Players": game_service.get_players(None)})
    else:
        error = {'result': 'ERROR', 'error_message': 'This table does not exist.'}
        abort(make_response(jsonify(error), 404))


@app.route('/api/tables/<table_id>', methods=['POST'])
def add_player_to_table(table_id):
    content = request.get_json()
    result = game_service.add_player(content["Name"])

    if result['result'] == 'OK':
        return JsonConvert.ToJSON(result)
    else:
        abort(make_response(jsonify(result), 400))

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



