import os 

class Config:
    # FLASK_DEBUG = 1
    # DEVELOPMENT = True
    # FLASK_ENV='development'
    SECRET_KEY = 'temporary'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True