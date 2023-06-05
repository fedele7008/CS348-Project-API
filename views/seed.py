import click
from flask import Blueprint
from app import db, app
from models import FoodItem, Restaurant, User, FoodLog

seed_blueprint = Blueprint("seed", __name__)


@seed_blueprint.cli.command("all")
def seed_all():
    restaurant1 = Restaurant(name='McDonalds')
    restaurant2 = Restaurant(name='Burger King')
    db.session.add(restaurant1)
    db.session.add(restaurant2)
    db.session.commit()

    big_mac = FoodItem(
        name='Big Mac', restaurant_id=restaurant1.id, calories=530, fat=27)
    bec = FoodItem(name='Bacon, Egg & Cheese Bagel',
                   restaurant_id=restaurant1.id, calories=620, fat=27, carb=10, fiber=5)
    pannini = FoodItem(name='Ham & Swiss Panini', restaurant_id=restaurant2.id,
                       calories=360, fat=9, carb=43, fiber=2, protein=2)
    double_whopper = FoodItem(name='Double Whopper Sandwich',
                              restaurant_id=restaurant2.id, calories=360, fat=9, carb=43, protein=37)
    whopper_jr = FoodItem(name='Whopper Jr. Sandwich', restaurant_id=restaurant2.id,
                          calories=310, fat=160, carb=18, fiber=2, protein=2)
    db.session.add(big_mac)
    db.session.add(bec)
    db.session.add(pannini)
    db.session.add(double_whopper)
    db.session.add(whopper_jr)
    db.session.commit()

    # add a user
    tim = User(name="Tim", email="tim@gmail.com")
    db.session.add(tim)
    db.session.commit()

    # add food logs
    food_items = [big_mac, bec, pannini, double_whopper, whopper_jr]
    tim_food_logs = []
    for food_item in food_items:
        tim_food_logs.append(
            FoodLog(user_id=tim.id, food_item_id=food_item.id))
    db.session.add_all(tim_food_logs)
    db.session.commit()
