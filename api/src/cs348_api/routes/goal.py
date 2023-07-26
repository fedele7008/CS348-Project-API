from flask import Blueprint, jsonify, request

from cs348_api.extensions import db
from cs348_api.models.food_log import FoodLog
from cs348_api.models.user import User
from cs348_api.models.food_item import FoodItem
from cs348_api.models.goal import Goal

import flask_jwt_extended

from datetime import datetime

goal = Blueprint('goal', __name__, url_prefix='/goal')

@goal.route('/', methods=['GET'])
@flask_jwt_extended.jwt_required()
def get_goals_of_user():
    user_id = flask_jwt_extended.get_jwt_identity()
    if user_id is None:
        return jsonify({
            'result': 'Unauthorized',
            'message': 'This feature requires authentication'
        }), 401
    goals = db.session.query(Goal)\
        .join(User, Goal.user_id == User.id)\
        .filter(User.id == user_id).all()

    return jsonify(goals), 200

@goal.route('/', methods=['POST'])
@flask_jwt_extended.jwt_required()
def create_goal():
    # Get data from the request JSON
    data = request.get_json()
    user_id = flask_jwt_extended.get_jwt_identity()
    name = data.get('name')
    goal_type = data.get('goal_type')
    quantity = data.get('quantity')
    streak = data.get('streak', 0)  # Default streak to 0 if not provided

    # Validate user_id
    if user_id is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'User ID is required'
        }), 400

    # Validate goal_type and quantity
    if goal_type is None or quantity is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Goal type and quantity are required'
        }), 400

    # Validate that quantity is a positive integer
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError()
    except ValueError:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Quantity must be a positive integer'
        }), 400

    # Check if the user exists in the database
    user = User.query.get(user_id)
    if user is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'User not found'
        }), 404

    # Create a new Goal object
    new_goal = Goal(user_id=user_id, name=name, goal_type=goal_type, quantity=quantity, streak=streak)

    # Add the new goal to the database
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({
        'result': 'Goal created',
        'message': 'Added new goal: {}'.format(new_goal)
    }), 201
    