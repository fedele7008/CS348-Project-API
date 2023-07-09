from dataclasses import dataclass

from cs348_api.extensions import db


@dataclass
class Goal(db.Model):
    # Define dataclass (to convert object to json)
    id: int
    user_id: int
    name: str
    goal_type: str
    quantity: int
    streak: int

    # Define columns for database
    id = db.Column(db.INTEGER(), primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False) # restaurant must have name
    goal_type = db.Column(db.String(255))
    quantity = db.Column(db.INTEGER())
    streak = db.Column(db.INTEGER())

    # __repr__ is used for printing object info (debugging purposes)
    def __repr__(self):
        return '<Goal: id={id}, name={name}, goal_type={goal_type}, quantity={quantity}, streak={streak}>'.format(
            id=self.id,
            name=self.name,
            goal_type=self.goal_type,
            quantity=self.quantity,
            streak=self.streak
        )
    
    
    # __str__ is used for printing object info (user friendly)
    def __str__(self):
        return '<Goal: {} (ID: {})>'.format(
            self.name, self.id
        )
