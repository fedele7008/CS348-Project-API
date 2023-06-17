from datetime import datetime
from flask import Blueprint, jsonify, request
import flask_jwt_extended
import bcrypt

from cs348_api.extensions import db, jwt
from cs348_api.models.user import User

auth = Blueprint('auth', __name__)


@jwt.expired_token_loader
def expired_token_callback(header, payload):
    user = db.session.query(User).filter_by(id=payload['sub']).first()
    return jsonify({
        'result': 'Expired token',
        'message': 'The {} token for {} has expired'.format(payload['type'], user)
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(e):
    return jsonify({
        'result': 'Invalid token',
        'message': '{}'.format(e)
    })


@auth.route('/register', methods=['POST'])
def register():
    # Get information from request body
    body = request.get_json()
    name = body['name']
    email = body['email']
    password = body['hashed_password'] # password should be hashed from front-end

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
    # Get information from request body
    body = request.get_json()
    email = body['email']
    password = body['hashed_password']

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
    

@auth.route('/test_user_only_feature', methods=['POST', 'GET'])
@flask_jwt_extended.jwt_required()
def test_user_only_feature():
    current_user_id = flask_jwt_extended.get_jwt_identity()
    if current_user_id is None:
        return 'This feature requires authentication', 401
    else:
        user = db.session.query(User).filter_by(id=current_user_id).first()
        return 'Welcome! {}'.format(user.name), 200
