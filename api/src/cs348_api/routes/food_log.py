from flask import Blueprint, jsonify

from cs348_api.extensions import db
from cs348_api.models.food_log import FoodLog

food_log = Blueprint('food_log', __name__, url_prefix='/log')


@food_log.route('/', methods=['GET'])
def get_food_logs():
    records = db.session.query(FoodLog).all()
    return jsonify(records)
