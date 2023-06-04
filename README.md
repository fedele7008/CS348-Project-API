# CS348-Project-API

CS 348 Project: Introduction to Database Management

# Setup instructions


## Dependencies 
Ensure that you have a virtual environment setup.

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

You should see (venv) in your terminal now.

Install dependencies: `pip install -r requirements.txt`

Update dependencies: `pip install pipreqs` and `pipreqs .`

## Database
### Initial MySQL setup
Open DB

```
brew install mysql
mysql -u root
```

Setup DB

```
# inside MySQL
CREATE DATABASE testDB;
USE testDB;
create user 'group8'@'localhost' identified by 'Password0!';
grant all on testDB.* to 'group8'@'localhost';
alter user 'group8'@'localhost' identified with mysql_native_password by 'Password0!';
```

### Set up tables and data
Run migrations to create all database tables: `flask db upgrade`

Seed database: `flask seed all`

## Setup Flask

Run the server with `python -m flask run`

Run with debug mode (auto-reloading after file changes) using `python -m flask run --debug`

You can now try getting response by going to `http://127.0.0.1:5000`

# Development
## Structure of project
- Database interactions are handled with `flask-sqlalchemy` ORM
   - ORM models for data are defined in `models.py`
- Migrations are handled with `flask-migrate` and are stored in `/migrations`
- SQL queries for assignment submission are stored in `/sql`
- API endpoints are defined in `/views` based on the relevant resource
   - e.g. food API endpoints are in `/views/food.py`

## Updating database
To update the database schema:
1. Update `models.py` with new schema
2. Run `flask db migrate -m <message>` to create a migration for this change
3. Run `flask migrate upgrade` to run the migration

To update seed data:
1. Update `/views/seed.py` with a new function decorated with `@seed_blueprint.cli.command("cmd_name")`
2. Run new command using `flask seed <cmd_name>`