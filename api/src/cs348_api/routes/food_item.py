from flask import Blueprint, jsonify, request
from sqlalchemy.orm import aliased

import flask_jwt_extended
from cs348_api.extensions import db
from cs348_api.models.food_item import FoodItem
from cs348_api.models.restaurant import Restaurant 
from cs348_api.models.user import User

food_item = Blueprint('food_item', __name__, url_prefix='/food')


@food_item.route('/', methods=['GET'])
def get_all_food_item():
    records = db.session.query(FoodItem, FoodItem)\
        .join(Restaurant, FoodItem.restaurant_id == Restaurant.id).all()

    records = [
        {
            'id': food_item.id,
            'food_name': food_item.name,
            'restaurant_id': food_item.restaurant_id,
            'restaurant_name': restaurant.name,
            'calories': food_item.calories,
            'fat': food_item.fat,
            'carb': food_item.carb,
            'fiber': food_item.fiber,
            'protein': food_item.protein
        }
        for food_item, restaurant in records
    ]

    return jsonify(records)


@food_item.route('/filter', methods=['POST'])
def get_filtered_food_item():
    if not request.is_json:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Request must be in JSON format'
        }), 400
    
    restaurants = request.json.get('restaurants', [])
    if len(restaurants) == 0:
        restaurants = db.session.query(Restaurant.id, Restaurant.name).all()
        restaurants = [
            res.id for res in restaurants
        ]
    
    search_query = request.json.get('search_query', '')
    sort_by = request.json.get('sort_by', 'name')
    if sort_by == 'name':
        sort_by = FoodItem.name
    elif sort_by == 'calories':
        sort_by = FoodItem.calories
    sort_order = request.json.get('sort_order', 'asc')

    records = db.session.query(FoodItem)\
    .join(Restaurant, FoodItem.restaurant_id == Restaurant.id)\
    .filter(Restaurant.id.in_(restaurants))
    
    if search_query != '':
        records = records.filter(FoodItem.name.like(f'%{search_query}%'))
    
    records = records.order_by(sort_by if sort_order == 'asc' else sort_by.desc())\
    .all()

    records = jsonify(records).get_json()
    for record in records:
        record['food_name'] = record.pop('name')
    print(records)

    return jsonify(records)


@food_item.route('/<int:id>', methods=['GET'])
def get_by_food_item(id):
    records = db.session.query(FoodItem, Restaurant)\
        .join(Restaurant, FoodItem.restaurant_id == Restaurant.id)\
        .filter(FoodItem.id == id).first()
    
    food_item, restaurant = records

    records = {
        'id': food_item.id,
        'food_name': food_item.name,
        'restaurant_id': food_item.restaurant_id,
        'restaurant_name': restaurant.name,
        'calories': food_item.calories,
        'fat': food_item.fat,
        'carb': food_item.carb,
        'fiber': food_item.fiber,
        'protein': food_item.protein
    }

    return jsonify(records)


@food_item.route('/', methods=['POST'])
@flask_jwt_extended.jwt_required()
def create_food_item():
    # Admin authorization checks
    current_user_id = flask_jwt_extended.get_jwt_identity()
    if current_user_id is None:
        return jsonify({
            'isAdmin': False,
            'message': 'This feature requires authentication'
        }), 401
    user = db.session.query(User).filter_by(id=current_user_id).first()
    if user.role != "admin":
        return jsonify({
            'isAdmin': False,
            'message': 'This feature requires admin authorization'
        }), 401

    # Get information from request
    if not request.is_json:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Request must be in JSON format'
        }), 400
    
    name = request.json.get('food_name', None)
    restaurant_id = request.json.get('restaurant_id', None)
    calories = request.json.get('calories', None)
    fat = request.json.get('fat', None)
    carb = request.json.get('carb', None)
    fiber = request.json.get('fiber', None)
    protein = request.json.get('protein', None)

    if name is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Name is required'
        }), 400
    
    food_item = FoodItem(name=name,
                         restaurant_id=restaurant_id,
                         calories=calories,
                         fat=fat,
                         carb=carb,
                         fiber=fiber,
                         protein=protein)
    
    db.session.add(food_item)
    db.session.commit()

    # Return response
    return jsonify({
        'result': 'Food created',
        'message': 'Registered food: {}'.format(food_item)
    }), 201


@food_item.route('/<int:id>', methods=['PUT'])
@flask_jwt_extended.jwt_required()
def update_food_item(id):
    # Admin authorization checks
    current_user_id = flask_jwt_extended.get_jwt_identity()
    if current_user_id is None:
        return jsonify({
            'isAdmin': False,
            'message': 'This feature requires authentication'
        }), 401
    user = db.session.query(User).filter_by(id=current_user_id).first()
    if user.role != "admin":
        return jsonify({
            'isAdmin': False,
            'message': 'This feature requires admin authorization'
        }), 401

    # Get information from request
    if not request.is_json:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Request must be in JSON format'
        }), 400
    
    name = request.json.get('food_name', None)
    restaurant_id = request.json.get('restaurant_id', None)
    calories = request.json.get('calories', None)
    fat = request.json.get('fat', None)
    carb = request.json.get('carb', None)
    fiber = request.json.get('fiber', None)
    protein = request.json.get('protein', None)

    if name is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Name is required'
        }), 400
    
    if restaurant_id is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Restaurant ID is required'
        }), 400

    food_item = db.session.query(FoodItem).filter(FoodItem.id == id).first()

    if food_item is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Food item not found'
        }), 404
    
    food_item.name = name
    food_item.restaurant_id = restaurant_id
    food_item.calories = calories
    food_item.fat = fat
    food_item.carb = carb
    food_item.fiber = fiber
    food_item.protein = protein

    db.session.commit()

    # Return response
    return jsonify({
        'result': 'Food updated',
        'message': 'Updated food: {}'.format(food_item)
    }), 200
    



@food_item.route('/<int:id>', methods=['PATCH'])
def patch_food_item(id):
    # Get information from request
    if not request.is_json:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Request must be in JSON format'
        }), 400
    
    name = request.json.get('name', None)
    restaurant_id = request.json.get('restaurant_id', None)
    calories = request.json.get('calories', None)
    fat = request.json.get('fat', None)
    carb = request.json.get('carb', None)
    fiber = request.json.get('fiber', None)
    protein = request.json.get('protein', None)

    food_item = db.session.query(FoodItem).filter(FoodItem.id == id).first()

    if food_item is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Food item not found'
        }), 404
    
    if name is not None:
        food_item.name = name
    
    if restaurant_id is not None:
        food_item.restaurant_id = restaurant_id
    
    if calories is not None:
        food_item.calories = calories

    if fat is not None:
        food_item.fat = fat

    if carb is not None:
        food_item.carb = carb

    if fiber is not None:
        food_item.fiber = fiber

    if protein is not None:
        food_item.protein = protein

    db.session.commit()

    # Return response
    return jsonify({
        'result': 'Food patched',
        'message': 'Patched food: {}'.format(food_item)
    }), 200


@food_item.route('/<int:id>', methods=['DELETE'])
def delete_food_item(id):
    food_item = db.session.query(FoodItem).filter(FoodItem.id == id).first()
    
    if food_item is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Food item not found'
        }), 404
    
    db.session.delete(food_item)
    db.session.commit()
    
    # Return response
    return jsonify({
        'result': 'Food deleted',
        'message': 'Deleted food: {}'.format(food_item)
    }), 200
