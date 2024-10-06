import random
from app import app, db
from models import db, Power, Hero, HeroPower

app.app_context().push()

print("🦸‍♀️ Seeding powers...")
powers = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
]
for power_data in powers:
    power = Power(name=power_data["name"], description=power_data["description"])
    db.session.add(power)

print("🦸‍♀️ Seeding heroes...")
heroes = [
    {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
    {"name": "Doreen Green", "super_name": "Squirrel Girl"},
    {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
    {"name": "Janet Van Dyne", "super_name": "The Wasp"},
    {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
    {"name": "Carol Danvers", "super_name": "Captain Marvel"},
    {"name": "Jean Grey", "super_name": "Dark Phoenix"},
    {"name": "Ororo Munroe", "super_name": "Storm"},
    {"name": "Kitty Pryde", "super_name": "Shadowcat"},
    {"name": "Elektra Natchios", "super_name": "Elektra"}
]
for hero_data in heroes:
    hero = Hero(name=hero_data["name"], super_name=hero_data["super_name"])
    db.session.add(hero)

print("🦸‍♀️ Adding powers to heroes...")
strengths = ["Strong", "Weak", "Average"]
heroes = Hero.query.all()
powers = Power.query.all()
for hero in heroes:
    num_powers = random.randint(1, 3)
    for _ in range(num_powers):
        power = random.choice(powers)
        strength = random.choice(strengths)
        hero_power = HeroPower(hero=hero, power=power, strength=strength)
        db.session.add(hero_power)

db.session.commit()

print("🦸‍♀️ Done seeding!")