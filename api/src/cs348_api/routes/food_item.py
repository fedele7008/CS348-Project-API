from flask import Blueprint, jsonify, request
from sqlalchemy.orm import aliased

from cs348_api.extensions import db
from cs348_api.models.food_item import FoodItem
from cs348_api.models.restaurant import Restaurant 

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
def create_food_item():
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
def update_food_item(id):
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
