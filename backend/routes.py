from flask import Flask, jsonify
from dotenv import load_dotenv

import db

app = Flask(__name__)

@app.route('/players/<name>', methods=['GET'])
def player_stats_page(name):
    load_dotenv()

    player = db.players_collection.find_one({'name': name})

    if player == None:
        return jsonify({'Error': 'Player not found'}), 404

    player.pop('_id')

    return jsonify(player), 200

@app.route('/teams/<name>', methods=['GET'])
def team_stats_page(name):
    load_dotenv()


    team = db.teams_collection.find_one({'name': name})

    if team == None:
        return jsonify({'Error': 'Team not found'}), 404

    team.pop('_id')


    return jsonify(team), 200

@app.route('/all-teams')
def list_all_teams():

    return jsonify(db.teams_collection.distinct('name')), 200


@app.route('/all-players')
def list_all_players():

    return jsonify(db.players_collection.distinct('name')), 200