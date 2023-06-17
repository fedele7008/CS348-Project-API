from flask import Blueprint, jsonify

from cs348_api.extensions import db
from cs348_api.models.user import User

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/', methods=['GET'])
def get_users():
    records = db.session.query(User).all()
    return jsonify(records)
