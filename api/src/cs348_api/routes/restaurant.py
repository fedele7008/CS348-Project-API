from flask import Blueprint, jsonify

from cs348_api.extensions import db
from cs348_api.models.restaurant import Restaurant

restaurant = Blueprint('restaurant', __name__, url_prefix='/restaurant')


@restaurant.route('/', methods=['GET'])
def get_food_logs():
    records = db.session.query(Restaurant).all()
    return jsonify(records)
