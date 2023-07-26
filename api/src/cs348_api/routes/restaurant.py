from flask import Blueprint, jsonify, request

import flask_jwt_extended
from cs348_api.extensions import db
from cs348_api.models.restaurant import Restaurant
from cs348_api.models.food_item import FoodItem
from cs348_api.models.user import User

restaurant = Blueprint('restaurant', __name__, url_prefix='/restaurant')


@restaurant.route('/', methods=['GET'])
def get_restaurants():
    records = db.session.query(Restaurant).all()
    return jsonify(records), 200


# TODO: change the route to /<int:id>/foods
@restaurant.route('/<string:name>/foods', methods=['GET'])
def get_restaurant_foods(name):
    foods = db.session.query(FoodItem)\
        .join(Restaurant, FoodItem.restaurant_id==Restaurant.id)\
        .filter(Restaurant.name == name).all()
    return jsonify(foods), 200


@restaurant.route('/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = db.session.query(Restaurant).filter(Restaurant.id == id).first()
    return jsonify(restaurant), 200


@restaurant.route('/', methods=['POST'])
@flask_jwt_extended.jwt_required()
def create_restaurant():
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
    
    name = request.json.get('name', None)

    if name is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Name is required'
        }), 400
    
    # TODO: restaurant name should be unique (?)

    restaurant = Restaurant(name=name)
    db.session.add(restaurant)
    db.session.commit()

    # Return response
    return jsonify({
        'result': 'Restaurant created',
        'message': 'Registered restaurant: {}'.format(restaurant)
    }), 201


@restaurant.route('/<int:id>', methods=['PUT'])
def update_restaurant(id):
    # Get information from request
    if not request.is_json:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Request must be in JSON format'
        }), 400
    
    name = request.json.get('name', None)

    restaurant = db.session.query(Restaurant).filter(Restaurant.id == id).first()
    if restaurant is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Restaurant not found'
        }), 404
    
    restaurant.name = name
    db.session.commit()

    # Return response
    return jsonify({
        'result': 'Restaurant updated',
        'message': 'Updated restaurant: {}'.format(restaurant)
    }), 200


@restaurant.route('/<int:id>', methods=['PATCH'])
def patch_restaurant(id):
    # Get information from request
    if not request.is_json:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Request must be in JSON format'
        }), 400
    
    name = request.json.get('name', None)

    restaurant = db.session.query(Restaurant).filter(Restaurant.id == id).first()
    if restaurant is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Restaurant not found'
        }), 404
    
    if name is not None:
        restaurant.name = name
    
    db.session.commit()

    # Return response
    return jsonify({
        'result': 'Restaurant patched',
        'message': 'Patched restaurant: {}'.format(restaurant)
    }), 200


@restaurant.route('/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = db.session.query(Restaurant).filter(Restaurant.id == id).first()

    if restaurant is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Restaurant not found'
        }), 404
    
    db.session.delete(restaurant)
    db.session.commit()
    
    # Return response
    return jsonify({
        'result': 'Restaurant deleted',
        'message': 'Deleted restaurant: {}'.format(restaurant)
    }), 200