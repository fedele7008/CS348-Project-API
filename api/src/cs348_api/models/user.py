from dataclasses import dataclass, field
from datetime import datetime

from cs348_api.extensions import db


@dataclass
class User(db.Model):
    # Define dataclass (to convert object to json)
    id: int
    name: str
    email: str
    registration_date: datetime = field(default_factory=datetime.utcnow)
    role: str


    # Define columns for database
    id = db.Column(db.INTEGER(), primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    registration_date = db.Column(db.DateTime(), nullable=False)
    role = db.Column(db.String(255), default="user")

    # __repr__ is used for printing object info (debugging purposes)
    def __repr__(self):
        return '<User: id={id}, name={name}, password={password}, email={email}, registration_date={registration_date}>'.format(
            id=self.id,
            name=self.name,
            password='<CREDENTIAL>',
            email=self.email,
            registration_date=self.registration_date
        )
    
    
    # __str__ is used for printing object info (user friendly)
    def __str__(self):
        return '<User: {} (ID: {}) [{}] - REGISTERED: {}>'.format(
            self.name, self.id, self.email, self.registration_date, self.role
        )
