#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    return (
        jsonify([hero.to_dict(only=("id", "name", "super_name")) for hero in heroes]),
        200,
    )


@app.route("/heroes/<int:id>", methods=["GET"])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    return jsonify(hero.to_dict(only=("id", "name", "super_name", "hero_powers"))), 200


@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    return (
        jsonify(
            [power.to_dict(only=("id", "name", "description")) for power in powers]
        ),
        200,
    )


@app.route("/powers/<int:id>", methods=["GET"])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    return jsonify(power.to_dict(only=("id", "name", "description"))), 200


@app.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    try:
        data = request.get_json()
        power.description = data["description"]
        db.session.commit()
        return jsonify(power.to_dict(only=("id", "name", "description"))), 200
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    try:
        data = request.get_json()
        hero_power = HeroPower(
            strength=data["strength"],
            hero_id=data["hero_id"],
            power_id=data["power_id"],
        )
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(hero_power.to_dict()), 200
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
