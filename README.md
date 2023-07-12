# CS348-Project-API

CS 348 Project: Introduction to Database Management

This is the backend API for a nutrition application that allows users to search for the nutritional information of different restaurant food items, log the foods that they ate, view statistics related to their eating habits, and set nutritional goals.

# Structure of project

## Structure

- Flask project is structured as a package named `cs348_api`
- **[C2-4]** SQL queries for assignment submission are stored in `doc/sql`
- Database interactions are handled with `flask-sqlalchemy` ORM
  - ORM models for data are defined in `models` subpackage
- Migrations are handled with `flask-migrate` and are stored in `/api/src/migrations`
- API endpoints are defined in `/api/src/cs348_api/routes` based on the relevant resource
  - e.g. food API endpoints are in `/api/src/cs348_api/routes/food_item.py`
  - `/api/src/cs348_api/routes/index.py` handles base route (e.g. localhost:6608/)

## Current Features (C5)

- Basic API endpoints to view contents of tables are avaliable with GET requests to `/food_item`, `/food_log`, `/restaurant`, `/user`
- **[R6]** API endpoint to fetch all food items from restaurants is avaliable from `/restaurant`, see `/routes/restaurant.py`
- **[R7]** API endpoints related to food logging are avaliable from `/log`, see `/routes/food_log.py`
- **[R10]** API endpoints related to authentication are avaliable at: POST to `/register`, POST to `/login`, GET to `/test_user_only_feature`

# Setup instructions

Download the repository to your desired location, the path shouldn't contain any space.

There are two ways to work on the project:

1. Manually set up the database and virtual environment.
2. Use docker container to run the database server and api server automatically.

You can choose either way to work on the project.

## Dependencies

### If you are manually setting up:

Ensure that you have a virtual environment setup.

```
# For MacOS/Linux
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

```
# For Windows
pip install virtualenv
python3 -m virtualenv venv
./venv/Scripts/activate.bat
```

You should see (venv) in your terminal now.

Then go to `api/` folder using `cd api` ,

Install dependencies: `pip install -r requirements.txt`

Update dependencies: `pip install pipreqs` and `pipreqs .`

### If you are using Docker:

Download Docker Desktop from https://www.docker.com/products/docker-desktop/
This will automatically install docker and docker-compose. Both are required.

Then open the 'terminal' if you are using MacOS or Linux.
For Windows users, use 'git bash' or 'wsl' or 'wsl2' (powershell and cmd will not work)

goto the project directory using `cd` and run `source env_setup.sh`. This will allow you to shortcut many docker commands
checkout the available commands using `api-server --help` or `api-server -h`.

> You should type `source env_setup.sh` everytime before using `api-server` command, or you can register `source env_setup.sh` to `~/.zprofile` file if you are using MacOS. If you are using Linux, `~/.bashrc` or `~/.bash_profile` should work.

## Database

### Initial MySQL setup

#### **For Manual setup:**

Open DB

```
brew install mysql
mysql -u root
```

Setup DB

```
# inside MySQL
CREATE DATABASE nutritrack;
USE nutritrack;
create user 'group8'@'localhost' identified by 'Password0!';
grant all on nutritrack.* to 'group8'@'localhost';
alter user 'group8'@'localhost' identified with mysql_native_password by 'Password0!';
```

#### **For Docker setup:**

Doesn't require any action

### Set up tables and data

#### **For Manual setup:**

Run migrations to create all database tables: `flask db upgrade`

Seed database with sample data: `flask seed sample`

Seed database with prod data: `flask seed prod`

Clean database (for reseed): `flask seed delete`

Note: data used to seed the prod database can be found under `/api/cs348_api/csv`

#### **For Docker setup:**

`flask db upgrade` is automatically done by Docker.

If you want to seed database using `flask seed all`, use docker-desktop -> containers -> api-1 -> terminal -> `bash` command -> `cd src` command -> `flask seed all` command.

OR

You can use `api-server connect api` -> `cd src` command -> `flask seed all` command. (in your terminal environment)

## Setup Flask

#### **For Manual setup:**

Set the Flask app environment variable.

`export FLASK_APP=cs348_api`

Ensure you are running commands in the `api/src` directory.

Run the server with `flask run -p 6608`

Run with debug mode (auto-reloading after file changes) using `flask run --debug -p 6608`

You can now try getting response by going to `http://127.0.0.1:6608`

#### **For Docker setup:**

Run `api-server up` or `api-server start`. This will automatically start flask server at `http://localhost:6608`.

You can also inspect/modify Database in GUI: goto `http://localhost:8080` and login to database:

- System: MySQL
- Server: db
- Username: group8
- Password: Password0!
- Database: nutritrack

# Development

## Updating database

To update the database schema:

1. Update `models.py` with new schema
2. Run `flask db migrate -m <message>` to create a migration for this change
3. Run `flask migrate upgrade` to run the migration

To update seed data:

1. Update `/views/seed.py` with a new function decorated with `@seed_blueprint.cli.command("cmd_name")`
2. Run new command using `flask seed <cmd_name>`
