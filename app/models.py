from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    #relationship 
    superpowers = db.relationship('Power', secondary='hero_powers', backref='superheroe')
    
    
    def __repr__(self):
        return f"Hero(id={self.id}, name='{self.name}', super_name='{self.super_name}', created_at='{self.created_at}', updated_at='{self.updated_at}')"
    
class HeroPower(db.Model):
    __tablename__ = "hero_powers"
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 
    hero = db.relationship('Hero', backref=db.backref('hero_powers', cascade='all, delete-orphan'))
    power = db.relationship('Power', backref=db.backref('power_heroes', cascade='all, delete-orphan'))
    
    @validates('strength')
    def validate_strength(self, key, value):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError("Invalid strength value")
        return value

    def __repr__(self):
        return f"HeroPower(id={self.id}, strength='{self.strength}', hero_id={self.hero_id}, power_id={self.power_id}, created_at='{self.created_at}', updated_at='{self.updated_at}')"
    
class Power(db.Model):
    __tablename__ = "powers"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
     #relationship 
    superheroes = db.relationship('Hero', secondary='hero_powers', backref='powers')
    
    @validates('description')
    def validate_description(self, key, value):
        if not value:
            raise ValueError("Description must be present")
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value
    
    def __repr__(self):
        return f"Power(id={self.id}, name='{self.name}', description='{self.description}', created_at='{self.created_at}', updated_at='{self.updated_at}')"