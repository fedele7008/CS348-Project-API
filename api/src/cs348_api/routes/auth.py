from datetime import datetime
from flask import Blueprint, jsonify, request
import flask_jwt_extended
import bcrypt

from cs348_api.extensions import db, jwt
from cs348_api.models.user import User

auth = Blueprint('auth', __name__)


# Called when token given is already expired
@jwt.expired_token_loader
def expired_token_callback(header, payload):
    user = db.session.query(User).filter_by(id=payload['sub']).first()
    return jsonify({
        'result': 'Expired token',
        'message': 'The {} token for {} has expired'.format(payload['type'], user)
    }), 401


# Called when token is corrupted
@jwt.invalid_token_loader
def invalid_token_callback(e):
    return jsonify({
        'result': 'Invalid token',
        'message': '{}'.format(e)
    }), 401


# Called when something is wrong in authorization in general
@jwt.unauthorized_loader
def unauthorized_callback(e):
    return jsonify({
        'result': 'Unauthorized',
        'message': '{}'.format(e)
    }), 401


@auth.route('/register', methods=['POST'])
def register():
    # Get information from request
    if not request.is_json:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Request must be in JSON format'
        }), 400
    
    name = request.json.get('name', None)
    email = request.json.get('email', None)
    password = request.json.get('hashed_password', None) # password should be hashed from front-end

    if name is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Name is required'
        }), 400
    
    if email is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Email is required'
        }), 400
    
    if password is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'hashed_password is required'
        }), 400

    # Check if user with same email already exists
    search = db.session.query(User).filter_by(email=email).first()
    if search is not None:
        return jsonify({
            'result': 'User already exists',
            'message': 'user with given email ({}) already exists'.format(email),
        }), 404
    
    # Encrypt the password internally from the back-end and store it to the db
    password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
    new_user = User(name=name, email=email, password=password, registration_date=datetime.utcnow())
    db.session.add(new_user)
    db.session.commit()

    # Return response
    return jsonify({
        'result': 'User created',
        'message': 'user registered: {}'.format(new_user),
        'access_token': flask_jwt_extended.create_access_token(identity=new_user.id)
    }), 201
        

@auth.route('/login', methods=['POST'])
def login():
    # Get information from request
    if not request.is_json:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Request must be in JSON format'
        }), 400
    
    email = request.json.get('email', None)
    password = request.json.get('hashed_password', None) # password should be hashed from front-end
    
    if email is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'Email is required'
        }), 400
    
    if password is None:
        return jsonify({
            'result': 'Invalid request',
            'message': 'hashed_password is required'
        }), 400

    # Check if user exists
    user = db.session.query(User).filter_by(email=email).first()
    if user is None:
        return jsonify({
            'result': 'User not found',
            'message': 'user with given email ({}) is not found'.format(email)
        }), 404
    
    # Return response with access token
    if bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8')):
        return jsonify({
            'result': 'Login successful',
            'message': 'Logged in as {}'.format(user),
            'access_token': flask_jwt_extended.create_access_token(identity=user.id)
        }), 200
    else:
        return jsonify({
            'result': 'Login failed',
            'message': 'Wrong credentials'
        }), 401
    

# Sample endpoint
@auth.route('/test_user_only_feature', methods=['POST', 'GET'])
@flask_jwt_extended.jwt_required()
def test_user_only_feature():
    current_user_id = flask_jwt_extended.get_jwt_identity()
    if current_user_id is None:
        return 'This feature requires authentication', 401
    else:
        user = db.session.query(User).filter_by(id=current_user_id).first()
        return 'Welcome! {}'.format(user.name), 200