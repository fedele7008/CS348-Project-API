import os
from datetime import datetime

from flask import Blueprint
from sqlalchemy.sql import text
from datetime import datetime
import csv
from faker import Faker
import random
import bcrypt

from cs348_api.extensions import db
from cs348_api.models.food_item import FoodItem
from cs348_api.models.restaurant import Restaurant
from cs348_api.models.food_log import FoodLog
from cs348_api.models.user import User
from cs348_api.models.goal import Goal

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

@seed.cli.command("sample")
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

    tim = User(name="Tim Cook", email="tim@email.com", password="$2b$12$5F7.aGK8YgErXEjnUUjw0uoYQMDq2LH/igRFpjV/8IVhw3uknxd/K", registration_date=datetime.utcnow())
    jane = User(name="Jane Doe", email="jane@email.com", password="$2b$12$UKc19ZNvWeV7Ae0CJ/vHJeVPksPGWFiJXwN3Ez5M8oeCNVODhOA2.", registration_date=datetime.utcnow())
    db.session.add(tim)
    db.session.add(jane)
    db.session.commit()

    user_data_file = f'{os.path.dirname(os.path.realpath(__file__))}/../../../user_data.md'
    try:
        open(user_data_file, 'r').close()
        with open(user_data_file, 'a') as f:
            f.write('|{name}|{email}|{password}|\n'.format(name='Tim Cook', email='tim@email.com', password='password'))
            f.write('|{name}|{email}|{password}|\n'.format(name='Jane Doe', email='jane@email.com', password='janedoe'))

    except FileNotFoundError:
        with open(user_data_file, 'w') as f:
            f.write('### This file contains user registration information for debugging purposes\n')
            f.write('These information is generated automatically by script and only show testing accounts only\n')
            f.write('|Name|Email|Password|\n')
            f.write('| :---: | :---: | :---: |\n')
            f.write('|{name}|{email}|{password}|\n'.format(name='Tim Cook', email='tim@email.com', password='password'))
            f.write('|{name}|{email}|{password}|\n'.format(name='Jane Doe', email='jane@email.com', password='janedoe'))

    # add goals for these users
    tim_cal_goal = Goal(name="my calorie goal", user_id=tim.id, goal_type="calorie", quantity=2500, streak=0)
    tim_fat_goal = Goal(name="get gains goal", user_id=tim.id, goal_type="fat", quantity=100, streak=1)
    tim_protein_goal = Goal(name="my fat goal", user_id=tim.id, goal_type="fat", quantity=50, streak=5)
    tim_carb_goal = Goal(name="my carb goal!", user_id=tim.id, goal_type="carb", quantity=200, streak=2)
    jane_cal_goal = Goal(name="reduce calorie goal", user_id=jane.id, goal_type="calorie", quantity=2000, streak=0)
    jane_fiber_goal = Goal(name="increase fiber consumption", user_id=jane.id, goal_type="fiber", quantity=2000, streak=0)
    db.session.add_all([tim_cal_goal, tim_fat_goal, tim_protein_goal, tim_carb_goal, jane_cal_goal, jane_fiber_goal])
    db.session.commit()

    # add food logs for Tim and Jane
    add_food_logs(tim, [big_mac, bec, pannini], '2023-06-4 15:00:00')
    add_food_logs(tim, [double_whopper, whopper_jr], '2023-06-10 11:30:00')
    add_food_logs(jane, [big_mac, pannini, bec], '2023-06-10 11:30:00')
    add_food_logs(jane, [pannini], '2023-06-11 11:30:00')
    add_food_logs(jane, [pannini, double_whopper, bec, whopper_jr], '2023-06-12 11:30:00')

@seed.cli.command("prod")
def seed_prod():   
    # Add restaurants 
    burger_king = Restaurant(name='Burger King')
    mcdonalds = Restaurant(name='McDonalds')
    starbucks = Restaurant(name='Starbucks')
    db.session.add_all([burger_king, mcdonalds, starbucks])
    db.session.commit()

    # Load food items from csv
    burger_king_food = []
    with open("./cs348_api/csv/burger-king-menu.csv",encoding='utf8') as f:
        reader = csv.DictReader(f)
        next(reader)
        for row in reader:
            new_entry = FoodItem(
                restaurant_id=burger_king.id,
                name=row["Item"],
                calories=row["Calories"],
                fat=row["Fat (g)"],
                carb=row["Total Carb (g)"],
                fiber=row["Dietary Fiber (g)"],
                protein=row["Protein (g)"]
            )
            burger_king_food.append(new_entry)
        db.session.add_all(burger_king_food)
        db.session.commit()
    
    mcdonalds_food = []
    with open("./cs348_api/csv/mcdonalds.csv",encoding='utf8') as f:
        reader = csv.DictReader(f)
        next(reader)
        for row in reader:
            new_entry = FoodItem(
                restaurant_id=mcdonalds.id,
                name=row["Item"],
                calories=row["Calories"],
                fat=row["Total Fat"],
                carb=row["Carbohydrates"],
                fiber=row["Dietary Fiber"],
                protein=row["Protein"]
            )
            mcdonalds_food.append(new_entry)
        db.session.add_all(mcdonalds_food)
        db.session.commit()
    
    starbucks_food = []
    with open("./cs348_api/csv/starbucks.csv",encoding='utf8') as f:
        reader = csv.DictReader(f)
        next(reader)
        for row in reader:
            new_entry = FoodItem(
                restaurant_id=starbucks.id,
                name=row["item"],
                calories=row["calories"],
                fat=row["fat"],
                carb=row["carb"],
                fiber=row["fiber"],
                protein=row["protein"]
            )
            starbucks_food.append(new_entry)
        db.session.add_all(starbucks_food)
        db.session.commit()
    
    # Randomly generate 50 users    
    faker = Faker()    
    Faker.seed(0) # ensure deterministic output
    users = []
    for i in range(50):
        name=faker.name(),
        email=faker.email(),
        password=faker.slug(), # random slug as password (e.g. "of-street-fight")
        registration_date=faker.date_time_this_year() # random registration date from current year
        if i == 0:
            role = "admin" # first user is an admin
        else:
            role = "user"
        new_user = User(
            name=name,
            email=email,
            password=bcrypt.hashpw("password".encode('UTF-8'), bcrypt.gensalt()),
            role=role,
            registration_date=registration_date
        )
        users.append(new_user)
    db.session.add_all(users)
    db.session.commit()

    # Randomly generate food logs for users
    random.seed(0) # ensure deterministic output
    all_foods = mcdonalds_food + burger_king_food + starbucks_food
    for user in users:
        # Generate the days that they have logged food
        days_logged_may = random.sample(range(1, 32), faker.random_int(0, 31))
        days_logged_june = random.sample(range(1, 31), faker.random_int(0, 30))
        # Generate the logs for each day
        for day in days_logged_may:
            date = datetime(2023, 5, day, 0, 0)    
            foods_logged = random.sample(all_foods, faker.random_int(1, 5)) # log 1-5 random foods for that day     
            add_food_logs(user, foods_logged, date.strftime('%Y-%m-%d %H:%M:%S'))
        for day in days_logged_june:
            date = datetime(2023, 6, day, 0, 0)    
            foods_logged = random.sample(all_foods, faker.random_int(1, 5)) # log 1-5 random foods for that day     
            add_food_logs(user, foods_logged, date.strftime('%Y-%m-%d %H:%M:%S'))

    # Randomly generate goals for users
    # List the type of goals and the range of quantities to randomly generate from
    goal_types = ["calorie", "fat", "carb", "fiber", "protein"]
    goal_quantities = {"calorie": [1500, 5000], "fat": [20, 200], "carb": [50, 500], "fiber": [10, 100], "protein": [30, 200]}
    # For each user, randomly generate between 0 to 5 goals
    for i, user in enumerate(users):
        num_goals = faker.random_int(0, 5)
        if i == 0:
            num_goals = 3 # choose 3 goals for first user
        goals = random.sample(goal_types, num_goals) # choose num_goals goal types
        for goal_type in goals:
            # Generate a goal with quantity within the goal type's specified range
            new_goal = Goal(
                name='{}\'s {} goal'.format(user.name, goal_type),
                user_id=user.id,
                goal_type=goal_type,
                quantity=faker.random_int(goal_quantities[goal_type][0], goal_quantities[goal_type][1], 10),
                streak=0
            )
            db.session.add(new_goal)
        db.session.commit()
