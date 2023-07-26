from flask import Flask
from flask_cors import CORS
from flask_apscheduler import APScheduler

from cs348_api.extensions import db, migrate, jwt
import cs348_api.routes as blueprints
from cs348_api import config
from cs348_api.models.food_log import FoodLog
from cs348_api.models.food_item import FoodItem
from cs348_api.models.goal import Goal
from cs348_api.models.restaurant import Restaurant
from cs348_api.models.user import User

from datetime import datetime

def update_streaks():
    # Get the current date in the format 'YYYY-MM-DD'
    current_date = datetime.today().date()

    # Create the first CTE (T1) to find today's consumption of each nutrition of each user
    subquery_t1 = db.session.query(FoodLog.user_id,
                                   db.func.sum(FoodItem.calories).label('calories'),
                                   db.func.sum(FoodItem.fat).label('fat'),
                                   db.func.sum(FoodItem.carb).label('carb'),
                                   db.func.sum(FoodItem.fiber).label('fiber'),
                                   db.func.sum(FoodItem.protein).label('protein')) \
        .join(FoodItem, FoodItem.id == FoodLog.food_item_id) \
        .filter(db.func.DATE(FoodLog.created_at) == current_date) \
        .group_by(FoodLog.user_id) \
        .subquery()
    
    # Create the second CTE (T2) to attach the consumption from T1 to the goal table by its goal_type
    subquery_t2 = db.session.query(subquery_t1.c.user_id, Goal.id, Goal.name, Goal.goal_type,
                                   Goal.quantity, Goal.streak,
                                   db.case(
                                       [(Goal.goal_type == 'calorie', subquery_t1.c.calories),
                                        (Goal.goal_type == 'fat', subquery_t1.c.fat),
                                        (Goal.goal_type == 'carb', subquery_t1.c.carb),
                                        (Goal.goal_type == 'fiber', subquery_t1.c.fiber),
                                        (Goal.goal_type == 'protein', subquery_t1.c.protein)],
                                       else_=0).label('consumption')) \
        .join(Goal, Goal.user_id == subquery_t1.c.user_id) \
        .subquery()
    
    # Perform the UPDATE based on the second CTE (T2)
    db.session.query(Goal) \
        .outerjoin(subquery_t2, Goal.id == subquery_t2.c.id) \
        .filter(Goal.id == subquery_t2.c.id) \
        .update({Goal.streak: db.case(
            [(subquery_t2.c.consumption >= subquery_t2.c.quantity, Goal.streak + 1)],
            else_=0
        )}, synchronize_session=False)

    # Commit the changes to the database
    db.session.commit()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = config.alchemy_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.alchemy_track_modifications()
    app.config['SQLALCHEMY_ECHO'] = config.alchemy_echo()
    app.config['JWT_SECRET_KEY'] = config.jwt_secret_key()
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.jwt_access_token_expires()

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Configure the Flask APScheduler
    app.config['SCHEDULER_API_ENABLED'] = True
    scheduler = APScheduler()
    scheduler.init_app(app)

    # Add the job to run the update_streaks function once a day
    @scheduler.task('interval', id='update_streaks_job', days=1, max_instances=1, misfire_grace_time=900)
    def scheduled_job():
        update_streaks()

    app.register_blueprint(blueprints.food_item)
    app.register_blueprint(blueprints.food_log)
    app.register_blueprint(blueprints.index)
    app.register_blueprint(blueprints.restaurant)
    app.register_blueprint(blueprints.seed)
    app.register_blueprint(blueprints.user)
    app.register_blueprint(blueprints.auth)
    app.register_blueprint(blueprints.goal)
    app.register_blueprint(blueprints.statistics)

    return app
