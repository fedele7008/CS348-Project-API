from flask import Flask
from flask_cors import CORS

from cs348_api.extensions import db, migrate
import cs348_api.routes as blueprints
from cs348_api import config

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = config.alchemy_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.alchemy_track_modifications()
    app.config['SQLALCHEMY_ECHO'] = config.alchemy_echo()

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(blueprints.food_item)
    app.register_blueprint(blueprints.food_log)
    app.register_blueprint(blueprints.index)
    app.register_blueprint(blueprints.restaurant)
    app.register_blueprint(blueprints.seed_blueprints)
    app.register_blueprint(blueprints.user)

    return app
