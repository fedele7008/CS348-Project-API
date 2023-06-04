from dataclasses import dataclass
from app import db, app

@dataclass
class Restaurant(db.Model):
    # Define dataclass (to convert object to JSON)
    id: int
    name: str

    # Define columns for database
    id = db.Column(db.INTEGER(), primary_key=True)
    name = db.Column(db.String(255), nullable=False) # restaurant must have a name

    def __repr__(self): # used by print()
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

    def __repr__(self): # used by print()
        return '<FoodItem id={id}, name={id}>'.format(id=self.id, name=self.name)
