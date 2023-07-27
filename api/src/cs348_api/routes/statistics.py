from calendar import monthrange

from flask import Blueprint, jsonify, request
from sqlalchemy import func, desc
from sqlalchemy.sql import text

from cs348_api.extensions import db
from cs348_api.models.food_log import FoodLog
from cs348_api.models.food_item import FoodItem
from cs348_api.models.restaurant import Restaurant

statistics = Blueprint('stat', __name__, url_prefix='/stat')

def set_read_uncommitted_level():
    transaction_sql = text("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;")
    db.session.execute(transaction_sql)


@statistics.route('/logged-food-stat-pie/<int:year>/<int:month>', methods=['GET'])
def get_logged_food_statistics_pie(year, month):
    nextmonth = month + 1 if month < 12 else 1

    set_read_uncommitted_level()
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
    set_read_uncommitted_level()
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


@statistics.route('/trending_food/<int:year>/<int:month>/<int:rank>', methods=['GET'])
def get_most_trending_food(year, month, rank):
    nextmonth = month + 1 if month < 12 else 1

    set_read_uncommitted_level()
    record = db.session.query(FoodItem, func.count(FoodLog.id).label('count'))\
        .join(FoodLog, FoodLog.food_item_id == FoodItem.id)\
        .filter(FoodLog.created_at >= f'{year}-{month}-1',
                FoodLog.created_at < f'{year}-{nextmonth}-1')\
        .group_by(FoodLog.food_item_id)\
        .order_by(desc('count'))\
        .all()
    
    upperlimit = len(record)
    if record == []:
        return jsonify({'food': {}, 'count': 0, 'isEmpty': True, 'rank': 1, 'upperlimit': upperlimit}), 200  
    
    record = record[rank - 1]
    food, count = record

    food = jsonify(food).get_json()
    food['food_name'] = food.pop('name')

    result = {
        'food': food,
        'count': count,
        'isEmpty': False,
        'upperlimit': upperlimit,
    }

    return jsonify(result), 200


@statistics.route('/restaurant-trend/<int:year>/<int:month>', methods=['GET'])
def get_restaurant_trend(year, month):
    nextmonth = month + 1 if month < 12 else 1
    last_day = monthrange(year, month)[1]
    
    set_read_uncommitted_level()
    records = db.session.query(FoodItem.restaurant_id, FoodLog.created_at, func.count(FoodLog.id).label('count'))\
        .join(FoodItem, FoodLog.food_item_id == FoodItem.id)\
        .filter(FoodLog.created_at >= f'{year}-{month}-1',
                FoodLog.created_at < f'{year}-{nextmonth}-1')\
        .group_by(FoodItem.restaurant_id, FoodLog.created_at)\
        .order_by(FoodLog.created_at)\
        .all()

    restaurants = db.session.query(Restaurant).all()
    restaurants_dict = dict()
    for r in restaurants:
        if r.id not in restaurants_dict:
            restaurants_dict[r.id] = r.name

    days = [day for day in range(1, last_day + 1)]

    data = dict()

    for id in restaurants_dict.keys():
        data[id] = [0 for _ in range(last_day)]    

    for id, day, count in records:
        if id not in data:
            data[id] = [0 for _ in range(last_day)]
        
        data[id][day.day - 1] = count

    dataset = [
        {
            'label': restaurants_dict[id],
            'data': data[id],
        } for id in data.keys()
    ]

    result = {
        'labels': days,
        'datasets': dataset
    }

    return jsonify(result), 200
    