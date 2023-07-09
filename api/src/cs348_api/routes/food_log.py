from flask import Blueprint, jsonify, request

from cs348_api.extensions import db
from cs348_api.models.food_log import FoodLog
from cs348_api.models.user import User
from cs348_api.models.food_item import FoodItem 

food_log = Blueprint('food_log', __name__, url_prefix='/log')


@food_log.route('/', methods=['GET'])
def get_food_logs():
    logs = db.session.query(FoodLog)\
        .join(FoodItem, FoodLog.food_item_id == FoodItem.id)\
        .join(User, FoodLog.user_id == User.id).all()

    return jsonify(logs), 200


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


@food_log.route('/', methods=['POST'])
def add_food_log():
    # Get information from request
    if not request.json:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Request must be in JSON format'
        }), 400
    
    user_id = request.json.get('user_id')
    food_item_id = request.json.get('food_item_id')

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
    
    food_log = FoodLog(user_id=user_id, food_item_id=food_item_id)
    db.session.add(food_log)
    db.session.commit()

    # Return response
    return jsonify({
        'result': 'Food log created',
        'message': 'Added food log: {}'.format(food_log)
    }), 201


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