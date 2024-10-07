from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    hero_powers = relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Hero {self.id}>'

    def to_dict(self, **kwargs):
        hero_dict = {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name
        }
        if kwargs.get('include_hero_powers', False):
            hero_dict['hero_powers'] = [hp.to_dict() for hp in self.hero_powers]
        return hero_dict

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    hero_powers = relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return description

    def __repr__(self):
        return f'<Power {self.id}>'

    def to_dict(self, **kwargs):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = {'Strong', 'Weak', 'Average'}
        if strength not in valid_strengths:
            raise ValueError(f"Strength must be one of {valid_strengths}.")
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'

    def to_dict(self, **kwargs):
        return {
            "id": self.id,
            "strength": self.strength,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "hero": self.hero.to_dict(),
            "power": self.power.to_dict()
        }
