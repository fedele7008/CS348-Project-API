from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from sqlalchemy import exc

db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

migrate = Migrate(app, db)

from views.food import food_blueprint
from views.seed import seed_blueprint
app.register_blueprint(seed_blueprint)
app.register_blueprint(food_blueprint, url_prefix='/food')


@app.route('/')
def hello():
    return "Hello world!"


@app.errorhandler(404)
def page_not_found(e):
    return "404 Not Found", 404


@app.errorhandler(500)
def internal_server_error(e):
    return "500 Internal Server Error", 500


@app.errorhandler(exc.SQLAlchemyError)
def sql_alchemy_error(e):
    print(e)
    return "500 SQLAlchemy Error", 500


if __name__ == '__main__':
    app.run()
