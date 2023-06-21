from flask import Blueprint, jsonify

from cs348_api.extensions import db
from cs348_api.models.restaurant import Restaurant
from cs348_api.models.food_item import FoodItem

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
