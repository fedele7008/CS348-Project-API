from flask import Blueprint
from sqlalchemy import exc

from cs348_api.extensions import db

index = Blueprint('index', __name__)


@index.route('/')
def hello_cs348_project():
    return 'Welcome to CS348 Project!!'


@index.errorhandler(404)
def page_not_found(e):
    return '404 Not Found', 404


@index.errorhandler(500)
def internal_server_error(e):
    return '500 Internal Server Error', 500


@index.errorhandler(exc.SQLAlchemyError)
def sqlalchemy_error(e):
    print(e)
    return '500 SQLAlchemy Error', 500
