from dataclasses import dataclass

from cs348_api.extensions import db


@dataclass
class User(db.Model):
    # Define dataclass (to convert object to json)
    id: int
    name: str
    email: str


    # Define columns for database
    id = db.Column(db.INTEGER(), primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))


    # __repr__ is used for printing object info (debugging purposes)
    def __repr__(self):
        return '<User: id={id}, name={name}, password={password}, email={email}>'.format(
            id=self.id,
            name=self.name,
            password='<CREDENTIAL>',
            email=self.email
        )
    
    
    # __str__ is used for printing object info (user friendly)
    def __str__(self):
        return '<User: {} (ID: {}) [{}]>'.format(
            self.name, self.id, self.email
        )
