from flask import Blueprint, jsonify
from sqlalchemy import func

from cs348_api.extensions import db
from cs348_api.models.restaurant import Restaurant
from cs348_api.models.food_item import FoodItem
from cs348_api.models.food_log import FoodLog

restaurant = Blueprint('restaurant', __name__, url_prefix='/restaurant')


@restaurant.route('/', methods=['GET'])
def get_restaurants():
    records = db.session.query(Restaurant).all()
    return jsonify(records)

@restaurant.route('/<string:name>/foods', methods=['GET'])
def get_restaurant_foods(name):
    foods = db.session.query(FoodItem)\
        .join(Restaurant, FoodItem.restaurant_id==Restaurant.id)\
        .filter(Restaurant.name == name).all()
    return jsonify(foods)

@restaurant.route('/<string:name>/trending', methods=['GET'])
def get_trending_foods(name):
    foods = db.session.query(FoodItem)\
        .join(Restaurant, FoodItem.restaurant_id==Restaurant.id)\
        .join(FoodLog, FoodLog.food_item_id==FoodItem.id)\
        .filter(Restaurant.name == name, FoodLog.created_at.between('2023-06-01', '2023-06-30'))\
        .group_by(FoodItem.id)\
        .order_by(func.count().desc())\
        .limit(6).all()
    return jsonify(foods)
