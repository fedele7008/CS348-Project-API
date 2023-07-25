from flask import Blueprint, jsonify, request

from cs348_api.extensions import db
from cs348_api.models.food_log import FoodLog
from cs348_api.models.user import User
from cs348_api.models.food_item import FoodItem
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, cast, Date

from datetime import datetime

food_log = Blueprint('food_log', __name__, url_prefix='/log')

@food_log.route('/', methods=['GET', 'POST'])
def get_food_logs():
    if request.method == "GET":
        logs = db.session.query(FoodLog, FoodItem)\
            .join(FoodItem, FoodLog.food_item_id == FoodItem.id)\
            .join(User, FoodLog.user_id == User.id).all()
        logs = [tuple(row) for row in logs]
        return jsonify(logs), 200
    elif request.method == "POST":
        # Get information from request
        if not request.json:
            return jsonify({
                'result': 'Invalid request',
                'message': 'Request must be in JSON format'
            }), 400
        
        user_id = request.json.get('user_id')
        food_item_id = request.json.get('food_item_id')
        date = request.json.get('date')
        created_at = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

        if user_id is None:
            return jsonify({
                'result': 'Invalid request',
                'message': 'User ID is required'
            }), 400
        
        if food_item_id is None:
            return jsonify({
                'result': 'Invalid request',
                'message': 'Food Item ID is required'
            }), 400
        
        if date is None:
            return jsonify({
                'result': 'Invalid request',
                'message': 'Date is required'
            }), 400 

        food_log = FoodLog(user_id=user_id, food_item_id=food_item_id, created_at=created_at)
        db.session.add(food_log)
        db.session.commit()

        # Return response
        return jsonify({
            'result': 'Food log created',
            'message': 'Added food log: {}'.format(food_log)
        }), 201

@food_log.route('/<int:id>', methods=['GET'])
def get_food_log(id):
    logs = db.session.query(FoodLog)\
        .join(FoodItem, FoodLog.food_item_id == FoodItem.id)\
        .join(User, FoodLog.user_id == User.id)\
        .filter(FoodLog.id == id).all()

    return jsonify(logs), 200


@food_log.route('/user/<int:user_id>', methods=['GET'])
def get_food_logs_of(user_id):
    logs = db.session.query(FoodLog)\
        .join(FoodItem, FoodLog.food_item_id == FoodItem.id)\
        .join(User, FoodLog.user_id == User.id)\
        .filter(User.id == user_id).all()

    return jsonify(logs), 200

@food_log.route('/consumption/<int:user_id>', methods=['GET'])
def get_food_consumption_of(user_id):
    date = datetime.strptime('2023-06-22 00:00:00', '%Y-%m-%d %H:%M:%S') 
    # date = datetime.now()
    result = db.session.query(
        FoodLog.user_id,
        func.sum(FoodItem.calories).label('calorie'),
        func.sum(FoodItem.fat).label('fat'),
        func.sum(FoodItem.carb).label('carb'),
        func.sum(FoodItem.fiber).label('fiber'),
        func.sum(FoodItem.protein).label('protein')
    ).join(FoodItem, FoodLog.food_item_id == FoodItem.id)\
     .filter(FoodLog.user_id == user_id,cast(FoodLog.created_at, Date) == date.date())\
     .group_by(FoodLog.user_id).first()
    
    if not result:
        result = (user_id, 0, 0, 0, 0, 0)
    
    data = {
        'user_id': result[0],
        'calorie': result[1],
        'fat': result[2],
        'carb': result[3],
        'fiber': result[4],
        'protein': result[5]
    }

    return jsonify(data), 200

@food_log.route('/<int:id>', methods=['PUT'])
def update_food_log(id):
    # Get information from request
    if not request.json:
        return jsonify({
           'result': 'Invalid request',
           'message': 'Request must be in JSON format'
        }), 400
    
    user_id = request.json.get('user_id')
    food_item_id = request.json.get('food_item_id')

    food_log = db.session.query(FoodLog).filter(FoodLog.id == id).first()
    if food_log is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Food log not found'
        }), 404
    
    food_log.user_id = user_id
    food_log.food_item_id = food_item_id

    db.session.commit()

    # Return response
    return jsonify({
        'result': 'Food log updated',
        'message': 'Updated food log: {}'.format(food_log)
    }), 200


@food_log.route('/<int:id>', methods=['PATCH'])
def patch_food_log(id):
    # Get information from request
    if not request.json:
        return jsonify({
           'result': 'Invalid request',
           'message': 'Request must be in JSON format'
        }), 400
    
    user_id = request.json.get('user_id')
    food_item_id = request.json.get('food_item_id')

    food_log = db.session.query(FoodLog).filter(FoodLog.id == id).first()
    if food_log is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Food log not found'
        }), 404
    
    if user_id is not None:
        food_log.user_id = user_id

    if food_item_id is not None:
        food_log.food_item_id = food_item_id

    db.session.commit()

    # Return response
    return jsonify({
        'result': 'Food log updated',
        'message': 'Updated food log: {}'.format(food_log)
    }), 200


@food_log.route('/<int:id>', methods=['DELETE'])
def delete_food_log(id):
    food_log = db.session.query(FoodLog).filter(FoodLog.id == id).first()
    
    if food_log is None:
        return jsonify({
           'result': 'Invalid request',
           'message': 'Food log not found'
        }), 404
    
    db.session.delete(food_log)
    db.session.commit()

    # Return response
    return jsonify({
       'result': 'Food log deleted',
       'message': 'Deleted food log: {}'.format(food_log)
    }), 200
