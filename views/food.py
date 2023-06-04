from flask import Blueprint, jsonify
from app import db
from models import Restaurant, FoodItem

food_blueprint = Blueprint('food', __name__)

@food_blueprint.route("/get")
def getAll(): # get all food items
    records=db.session.query(FoodItem).all()
    return jsonify(records)

@food_blueprint.route("/get/<int:id>")
def get(id): # get food item based on id
    records=db.session.query(FoodItem).filter_by(id=id).all()
    return jsonify(records)
