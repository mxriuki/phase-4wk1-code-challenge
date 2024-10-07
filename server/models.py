from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = "heroes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # add relationship
    hero_powers = db.relationship("HeroPower", backref="hero", cascade="all, delete")

    # add serialization rules
    def to_dict(self, only=None):
        hero_dict = {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
            "hero_powers": [
                {
                    "id": hero_power.id,
                    "power": hero_power.power.to_dict(
                        only=("id", "name", "description")
                    ),
                    "strength": hero_power.strength,
                }
                for hero_power in self.hero_powers
            ],
        }
        if only:
            return {key: hero_dict[key] for key in only}
        return hero_dict

    def __repr__(self):
        return f"<Hero {self.id}>"


class Power(db.Model, SerializerMixin):
    __tablename__ = "powers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # add relationship
    hero_powers = db.relationship("HeroPower", backref="power", cascade="all, delete")

    # add serialization rules
    def to_dict(self, only=None):
        power_dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
        if only:
            return {key: power_dict[key] for key in only}
        return power_dict

    # add validation
    @validates("description")
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError("validation errors")
        return value

    def __repr__(self):
        return f"<Power {self.id}>"


class HeroPower(db.Model):
    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"), nullable=False)

    @validates("strength")
    def validate_strength(self, key, value):
        if value not in ["Strong", "Weak", "Average"]:
            raise ValueError("validation errors")
        return value

    def to_dict(self, only=None):
        hero_power_dict = {
            "id": self.id,
            "strength": self.strength,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "hero": {
                "id": self.hero.id,
                "name": self.hero.name,
                "super_name": self.hero.super_name,
            },
            "power": {
                "id": self.power.id,
                "name": self.power.name,
                "description": self.power.description,
            },
        }
        if only:
            return {key: hero_power_dict[key] for key in only}
        return hero_power_dict

    def __repr__(self):
        return f"<HeroPower {self.id}>"
