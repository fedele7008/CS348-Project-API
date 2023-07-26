from flask import Flask
from flask_cors import CORS

from cs348_api.extensions import db, migrate, jwt
import cs348_api.routes as blueprints
from cs348_api import config
from cs348_api.models.food_log import FoodLog
from cs348_api.models.food_item import FoodItem
from cs348_api.models.goal import Goal
from cs348_api.models.restaurant import Restaurant
from cs348_api.models.user import User

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = config.alchemy_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.alchemy_track_modifications()
    app.config['SQLALCHEMY_ECHO'] = config.alchemy_echo()
    app.config['JWT_SECRET_KEY'] = config.jwt_secret_key()
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.jwt_access_token_expires()

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(blueprints.auth)
    app.register_blueprint(blueprints.food_item)
    app.register_blueprint(blueprints.food_log)
    app.register_blueprint(blueprints.index)
    app.register_blueprint(blueprints.restaurant)
    app.register_blueprint(blueprints.seed)
    app.register_blueprint(blueprints.user)
    app.register_blueprint(blueprints.statistics)

    return app
