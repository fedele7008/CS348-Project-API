from dataclasses import dataclass

from cs348_api.extensions import db


@dataclass
class Restaurant(db.Model):
    # Define dataclass (to convert object to json)
    id: int
    name: str


    # Define columns for database
    id = db.Column(db.INTEGER(), primary_key=True)
    name = db.Column(db.String(255), nullable=False) # restaurant must have name


    # __repr__ is used for printing object info (debugging purposes)
    def __repr__(self):
        return '<Restaurant: id={}, name={}>'.format(
            self.id, self.name
        )
    
    
    # __str__ is used for printing object info (user friendly)
    def __str__(self):
        return '<Restaurant: {} (ID: {})>'.format(
            self.name, self.id
        )
