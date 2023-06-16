from flask import Blueprint, jsonify

from cs348_api.extensions import db
from cs348_api.models.food_item import FoodItem

food_item = Blueprint('food_item', __name__, url_prefix='/food')


@food_item.route('/', methods=['GET'])
def get_all():
    records = db.session.query(FoodItem).all()
    return jsonify(records)


@food_item.route('/<int:id>', methods=['GET'])
def get_by(id):
    records=db.session.query(FoodItem).filter_by(id=id).all()
    return jsonify(records)
