from dataclasses import dataclass
from app import db, app
import datetime


@dataclass
class Restaurant(db.Model):
    # Define dataclass (to convert object to JSON)
    id: int
    name: str

    # Define columns for database
    id = db.Column(db.INTEGER(), primary_key=True)
    # restaurant must have a name
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):  # used by print()
        return '<User id={id}, name={id}>'.format(id=self.id, name=self.name)


@dataclass
class FoodItem(db.Model):
    # Define dataclass (to convert object to JSON)
    id: int
    name: str
    restaurant_id: int
    calories: int
    fat: int
    carb: int
    fiber: int
    protein: int

    id = db.Column(db.INTEGER(), primary_key=True)
    name = db.Column(db.String(255))
    restaurant_id = db.Column(db.ForeignKey('restaurant.id'), nullable=False)
    calories = db.Column(db.INTEGER())
    fat = db.Column(db.INTEGER())
    carb = db.Column(db.INTEGER())
    fiber = db.Column(db.INTEGER())
    protein = db.Column(db.INTEGER())

    def __repr__(self):  # used by print()
        return '<FoodItem id={id}, name={id}>'.format(id=self.id, name=self.name)


@dataclass
class User(db.Model):
   # Define dataclass (to convert object to JSON)
    id: int
    name: str
    email: str

    id = db.Column(db.INTEGER(), primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def __repr__(self):  # used by print()
        return '<User id={id}, name={name}>'.format(id=self.id, name=self.name)


@dataclass
class FoodLog(db.Model):
    id: int
    user_id: int
    food_item_id: int
    created_at: datetime

    id = db.Column(db.INTEGER(), primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    food_item_id = db.Column(db.ForeignKey('food_item.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
