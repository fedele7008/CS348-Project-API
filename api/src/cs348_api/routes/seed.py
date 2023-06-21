from flask import Blueprint
from sqlalchemy.sql import text

from cs348_api.extensions import db
from cs348_api.models.food_item import FoodItem
from cs348_api.models.restaurant import Restaurant
from cs348_api.models.food_log import FoodLog
from cs348_api.models.user import User
from cs348_api.models.goal import Goal
from datetime import datetime

seed = Blueprint("seed", __name__)

@seed.cli.command("delete")
def delete_all():
    # delete contents of all tables to reset db
    db.session.query(FoodLog).delete()
    db.session.query(FoodItem).delete()
    db.session.query(Restaurant).delete()
    db.session.query(Goal).delete()
    db.session.query(User).delete()        
    db.session.execute(text('ALTER TABLE food_log AUTO_INCREMENT=1'))
    db.session.execute(text('ALTER TABLE food_item AUTO_INCREMENT=1'))
    db.session.execute(text('ALTER TABLE restaurant AUTO_INCREMENT=1'))
    db.session.execute(text('ALTER TABLE goal AUTO_INCREMENT=1'))
    db.session.execute(text('ALTER TABLE user AUTO_INCREMENT=1'))    
    db.session.commit()

def add_food_logs(user, food_list, created_at):
    food_logs = []
    for food_item in food_list:
        fl = FoodLog(user_id=user.id, food_item_id=food_item.id)
        fl.created_at = created_at
        food_logs.append(fl)
    db.session.add_all(food_logs)
    db.session.commit()

@seed.cli.command("all")
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
    db.session.add_all([big_mac, bec, pannini, double_whopper, whopper_jr])
    db.session.commit()

    # add two sample users
    tim = User(name="Tim Cook", email="tim@email.com", password="password", registration_date=datetime.utcnow())
    jane = User(name="Jane Doe", email="jane@email.com", password="janedoe", registration_date=datetime.utcnow())
    db.session.add(tim)
    db.session.add(jane)
    db.session.commit()

    # add goals for these users
    tim_cal_goal = Goal(name="my calorie goal", user_id=tim.id, goal_type="calorie", quantity=2500, streak=0)
    tim_fat_goal = Goal(name="get gains goal", user_id=tim.id, goal_type="fat", quantity=100, streak=1)
    tim_protein_goal = Goal(name="my fat goal", user_id=tim.id, goal_type="fat", quantity=50, streak=5)
    tim_sugar_goal = Goal(name="reduce sugar!", user_id=tim.id, goal_type="sugar", quantity=20, streak=2)
    jane_cal_goal = Goal(name="reduce calorie goal", user_id=jane.id, goal_type="calorie", quantity=2000, streak=0)
    jane_fiber_goal = Goal(name="increase fiber consumption", user_id=jane.id, goal_type="fiber", quantity=2000, streak=0)
    db.session.add_all([tim_cal_goal, tim_fat_goal, tim_protein_goal, tim_sugar_goal, jane_cal_goal, jane_fiber_goal])
    db.session.commit()

    # add food logs for Tim and Jane
    add_food_logs(tim, [big_mac, bec, pannini], '2023-06-4 15:00:00')
    add_food_logs(tim, [double_whopper, whopper_jr], '2023-06-10 11:30:00')
    add_food_logs(jane, [big_mac, pannini, bec], '2023-06-10 11:30:00')
    add_food_logs(jane, [pannini], '2023-06-11 11:30:00')
    add_food_logs(jane, [pannini, double_whopper, bec, whopper_jr], '2023-06-12 11:30:00')

