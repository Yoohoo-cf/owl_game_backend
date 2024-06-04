import json
import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS

import config
from game import Game

load_dotenv()

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

config.conn = mysql.connector.connect(
         host=os.environ.get('HOST'),
         port=3306,
         database=os.environ.get('DB_NAME'),
         user=os.environ.get('DB_USER'),
         password=os.environ.get('DB_PASS'),
         autocommit=True
         )

def fly(id, dest, consumption=0, player=None):
    if id == 0:
        game = Game(0, dest, consumption, player)
    else:
        game = Game(id, dest, consumption)

    game.location[0].fetch_magics(game)
    magicLoc = game.location[0].set_magic_airports()
    for m in magicLoc:
        game.location.append(m)
    json_data = json.dumps(game, default=lambda o: o.__dict__, indent=4)
    return json_data

# http://127.0.0.1:7000/flyto?game=VAFyWkaMC4H1jWxR44Tl&dest=ESCF&consumption=246
@app.route('/flyto')
def flyto():
    args = request.args
    id = args.get("game")
    dest = args.get("dest")
    consumption = args.get("consumption")
    json_data = fly(id, dest, consumption)
    print("Called flyto endpoint at http:localhost:7000/flyto/")
    return json_data

# http://127.0.0.1:7000/newgame?player=Remy&loc=LFDZ
@app.route('/newgame')
def newgame():
    args = request.args
    player = args.get("player")
    dest = args.get("loc")
    json_data = fly(0, dest, 0, player)
    return json_data

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=7000)


