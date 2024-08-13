from flask import Flask, request, jsonify
from celery import Celery
import pandas as pd
import uuid
import difflib
import time
import json

# Initialize Flask application
app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Load Pokémon data from a CSV file into a DataFrame
df = pd.read_csv('pokemon.csv')

# Battle storage
battle_results = {}

def get_pokemon_stats(pokemon_name):
    pokemon_data = df[df['name'].str.lower() == pokemon_name.lower()].iloc[0]
    return {
        'type1': pokemon_data['type1'],
        'type2': pokemon_data['type2'],
        'attack': pokemon_data['attack']
    }

def get_against_stats(pokemon_name, type1, type2):
    against_stats = {}
    if type1:
        against_stats[f'against_{type1}'] = df[df['name'].str.lower() == pokemon_name.lower()][f'against_{type1}'].iloc[0]
    if type2:
        against_stats[f'against_{type2}'] = df[df['name'].str.lower() == pokemon_name.lower()][f'against_{type2}'].iloc[0]
    return against_stats

def battle_round(pokemon_a, pokemon_b):
    a_stats = get_pokemon_stats(pokemon_a)
    b_stats = get_pokemon_stats(pokemon_b)
    b_against_stats = get_against_stats(pokemon_b, a_stats['type1'], a_stats['type2'])
    return {
        'pokemon_a': a_stats,
        'pokemon_b': {
            'against_type1': b_against_stats.get(f'against_{a_stats["type1"]}'),
            'against_type2': b_against_stats.get(f'against_{a_stats["type2"]}')
        }
    }

def calculate_damage_percent(round_stats):
    a_attack = round_stats['pokemon_a']['attack']
    b_against_type1 = round_stats['pokemon_b']['against_type1']
    b_against_type2 = round_stats['pokemon_b']['against_type2']
    damage_a = (a_attack / 200) * 100 - (((b_against_type1 / 4) * 100) + ((b_against_type2 / 4) * 100))
    return damage_a, None

@celery.task(bind=True)
def run_battle(self, pokemon_a, pokemon_b):
    try:
        round1 = battle_round(pokemon_a, pokemon_b)
        round2 = battle_round(pokemon_b, pokemon_a)
        damage_a_round1, damage_b_round1 = calculate_damage_percent(round1)
        damage_a_round2, damage_b_round2 = calculate_damage_percent(round2)
        total_damage_a = damage_a_round1 + damage_a_round2
        total_damage_b = damage_b_round1 + damage_b_round2
        if total_damage_a > total_damage_b:
            result = {"winnerName": pokemon_a, "wonByMargin": total_damage_a - total_damage_b}
        elif total_damage_a < total_damage_b:
            result = {"winnerName": pokemon_b, "wonByMargin": total_damage_b - total_damage_a}
        else:
            result = {"winnerName": "Draw", "wonByMargin": 0}
        battle_results[self.request.id] = {"status": "BATTLE_COMPLETED", "result": result}
    except Exception as e:
        battle_results[self.request.id] = {"status": "BATTLE_FAILED", "result": None}

@app.route('/pokemons', methods=['GET'])
def list_pokemons():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    start = (page - 1) * per_page
    end = start + per_page
    pokemons = df['name'].tolist()
    return jsonify(pokemons[start:end])

@app.route('/battle', methods=['POST'])
def battle():
    data = request.get_json()
    pokemon_a = data['pokemon_a']
    pokemon_b = data['pokemon_b']
    battle_id = str(uuid.uuid4())
    run_battle.apply_async((pokemon_a, pokemon_b), task_id=battle_id)
    return jsonify({"battle_id": battle_id})

@app.route('/battle/<battle_id>', methods=['GET'])
def battle_status(battle_id):
    if battle_id in battle_results:
        return jsonify(battle_results[battle_id])
    else:
        return jsonify({"status": "BATTLE_INPROGRESS", "result": None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
