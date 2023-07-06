from flask import Blueprint, jsonify, request

from cs348_api.extensions import db
from cs348_api.models.user import User

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/', methods=['GET'])
def get_users():
    records = db.session.query(User).all()
    return jsonify(records), 200


@user.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    record = db.session.query(User).filter_by(id=user_id).first()
    return jsonify(record), 200


@user.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Get information from request
    if not request.is_json:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Request must be in JSON format'
        }), 400
    
    name = request.json.get('name', None)
    email = request.json.get('email', None)

    # change the name and email of the user with given user_id
    user = db.session.query(User).filter_by(id=user_id).first()
    if user is None:
        return jsonify({
           'result': 'Invalid request',
           'message': 'User not found'
        }), 404
    
    user.name = name
    user.email = email
    db.session.commit()

    # Return response
    return jsonify({
        'result': 'User updated successfully',
        'message': 'updated user: {}'.format(user)
    }), 200


@user.route('/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    # Get information from request
    if not request.is_json:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Request must be in JSON format'
        }), 400
    
    name = request.json.get('name', None)
    email = request.json.get('email', None)

    # change the name and email of the user with given user_id
    user = db.session.query(User).filter_by(id=user_id).first()
    if user is None:
        return jsonify({
           'result': 'Invalid request',
           'message': 'User not found'
        }), 404
    
    if name is not None:
        user.name = name
    
    if email is not None:
        user.email = email
    
    db.session.commit()

    # Return response
    return jsonify({
        'result': 'User patched successfully',
        'message': 'Patched user: {}'.format(user)
    }), 200


@user.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    
    if user is None:
        return jsonify({
          'result': 'Invalid request',
          'message': 'User not found'
        }), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
      'result': 'User deleted successfully',
      'message': 'deleted user: {}'.format(user)
    }), 200


# To create a new user, use /register route in auth.py instead