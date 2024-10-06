#!/usr/bin/env python3
from flask import Flask, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse, abort
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Request parser for PATCH /powers/:id
power_patch_parser = reqparse.RequestParser()
power_patch_parser.add_argument('description', type=str, required=True)

class HeroesResource(Resource):
    def get(self):
        heroes = Hero.query.all()
        return [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]


class HeroResource(Resource):
    def get(self, hero_id):
        hero = Hero.query.get(hero_id)
        if not hero:
            abort(404, error="Hero not found")
        powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.superpowers]
        return {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers}


class PowersResource(Resource):
    def get(self):
        powers = Power.query.all()
        return [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]


class PowerResource(Resource):
    def get(self, power_id):
        power = Power.query.get(power_id)
        if not power:
            abort(404, error="Power not found")
        return {'id': power.id, 'name': power.name, 'description': power.description}

    def patch(self, power_id):
        power = Power.query.get(power_id)
        if not power:
            abort(404, error="Power not found")

        args = power_patch_parser.parse_args()
        power.description = args['description']

        try:
            db.session.commit()
            return {'id': power.id, 'name': power.name, 'description': power.description}
        except Exception as e:
            db.session.rollback()
            abort(400, errors=[str(e)])


class HeroPowersResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('strength', type=str, required=True)
        parser.add_argument('power_id', type=int, required=True)
        parser.add_argument('hero_id', type=int, required=True)
        args = parser.parse_args()

        power = Power.query.get(args['power_id'])
        hero = Hero.query.get(args['hero_id'])

        if not power or not hero:
            abort(404, error="Power or Hero not found")

        hero_power = HeroPower(strength=args['strength'], hero=hero, power=power)

        try:
            db.session.add(hero_power)
            db.session.commit()
            powers = [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.superpowers]
            return {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers}
        except Exception as e:
            db.session.rollback()
            abort(400, errors=[str(e)])


api.add_resource(HeroesResource, '/heroes')
api.add_resource(HeroResource, '/heroes/<int:hero_id>')
api.add_resource(PowersResource, '/powers')
api.add_resource(PowerResource, '/powers/<int:power_id>')
api.add_resource(HeroPowersResource, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5565)