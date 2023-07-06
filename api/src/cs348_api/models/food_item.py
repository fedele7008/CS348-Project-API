from dataclasses import dataclass

from cs348_api.extensions import db


@dataclass
class FoodItem(db.Model):
    # Define dataclass (to convert object to json)
    id: int
    name: str
    restaurant_id: int
    calories: int
    fat: int
    carb: int
    fiber: int
    protein: int


    # Define columns for database
    id = db.Column(db.INTEGER(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    restaurant_id = db.Column(db.ForeignKey('restaurant.id'), nullable=False)
    calories = db.Column(db.INTEGER())
    fat = db.Column(db.INTEGER())
    carb = db.Column(db.INTEGER())
    fiber = db.Column(db.INTEGER())
    protein = db.Column(db.INTEGER())


    # __repr__ is used for printing object info (debugging purposes)
    def __repr__(self):
        return '<FoodItem: id={id}, name={name}, restaurnat_id={restaurant_id}, calories={calories}, fat={fat}, carb={carb}, fiber={fiber}, protein={protein}>'.format(
            id=self.id,
            name=self.name,
            restaurant_id=self.restaurant_id,
            calories=self.calories,
            fat=self.fat,
            carb=self.carb,
            fiber=self.fiber,
            protein=self.protein
        )
    
    
    # __str__ is used for printing object info (user friendly)
    def __str__(self):
        return '<Food Item: {} (ID: {})>'.format(
            self.name, self.id
        )
