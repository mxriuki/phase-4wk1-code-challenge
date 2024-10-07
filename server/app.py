#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

# GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict(include_hero_powers=True))
    return jsonify({"error": "Hero not found"}), 404

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict())
    return jsonify({"error": "Power not found"}), 404

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.json
    description = data.get('description')
    
    if description:
        try:
            power.description = description
            db.session.commit()
            return jsonify(power.to_dict())
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400

    return jsonify({"errors": ["validation errors"]}), 400

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    strength = data.get('strength')
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')

    # Validate strength value
    if strength not in {"Strong", "Weak", "Average"}:
        return jsonify({"errors": ["validation errors"]}), 400

    try:
        hero_power = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(hero_power.to_dict())
    except (ValueError, KeyError) as e:
        return jsonify({"errors": ["validation errors"]}), 400



if __name__ == '__main__':
    app.run(port=5555, debug=True)
