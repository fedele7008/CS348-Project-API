import datetime
from dataclasses import dataclass

from cs348_api.extensions import db


@dataclass
class FoodLog(db.Model):
    # Define dataclass (to convert object to json)
    id: int
    user_id: int
    food_item_id: int
    created_at: datetime


    # Define columns for database
    id = db.Column(db.INTEGER(), primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    food_item_id = db.Column(db.ForeignKey('food_item.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())


    # __repr__ is used for printing object info (debugging purposes)
    def __repr__(self):
        return '<FoodLog: id={id}, user_id={user_id}, food_item_id={food_item_id}, created_at={created_at}>'.format(
            id=self.id,
            user_id=self.user_id,
            food_item_id=self.food_item_id,
            created_at=self.created_at
        )
    
    
    # __str__ is used for printing object info (user friendly)
    def __str__(self):
        return '<FoodLog: food_log={id}, user({user}) loged food({food_item_id}) at {created_at}>'.format(
            id=self.id,
            user=self.user_id,
            food_item_id=self.food_item_id,
            created_at=self.created_at
        )
