from flask import Blueprint, jsonify, request
from sqlalchemy import func, desc

from cs348_api.extensions import db
from cs348_api.models.food_log import FoodLog
from cs348_api.models.food_item import FoodItem
from cs348_api.models.restaurant import Restaurant

statistics = Blueprint('stat', __name__, url_prefix='/stat')


@statistics.route('/logged-food-stat-pie/<int:year>/<int:month>', methods=['GET'])
def get_logged_food_statistics_pie(year, month):
    nextmonth = month + 1 if month < 12 else 1
    records = db.session.query(Restaurant.id, Restaurant.name, func.count().label('count'))\
        .join(FoodItem, Restaurant.id == FoodItem.restaurant_id)\
        .join(FoodLog, FoodItem.id == FoodLog.food_item_id)\
        .filter(FoodLog.created_at >= f'{year}-{month}-1',
                FoodLog.created_at < f'{year}-{nextmonth}-1')\
        .group_by(Restaurant.id, Restaurant.name)\
        .order_by(Restaurant.id)\
        .all()
    
    records = [
        {
            'id': record[0],
            'restaurant': record[1],
            'count': record[2]
        }
        for record in records
    ]
    return jsonify(records), 200


@statistics.route('/average-calories-per-restaurant/<int:top_rank>', methods=['GET'])
def get_average_calories_per_restaurant(top_rank):
    top_restaurant = db.session.query(Restaurant.id, Restaurant.name, func.count(FoodLog.id).label('count'))\
        .join(FoodItem, Restaurant.id == FoodItem.restaurant_id)\
        .join(FoodLog, FoodItem.id == FoodLog.food_item_id)\
        .group_by(Restaurant.id, Restaurant.name)\
        .order_by(desc('count'))\
        .limit(top_rank)\
        .all()

    top_restaurant = [
        record[0] for record in top_restaurant
    ]

    records = db.session.query(Restaurant.id, Restaurant.name, func.avg(FoodItem.calories).label('avg_calories'))\
        .join(FoodItem, Restaurant.id == FoodItem.restaurant_id)\
        .filter(Restaurant.id.in_(top_restaurant))\
        .group_by(Restaurant.id, Restaurant.name)\
        .all()
    
    records = [
        {
            'id': record[0],
            'restaurant': record[1],
            'avg_calories': float(record[2])
        } for record in records
    ]

    return jsonify(records), 200