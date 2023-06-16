# CS348-Project-API

CS 348 Project: Introduction to Database Management

# Setup instructions
download the repository to your disired location, the path shouldn't contain any space.

There are two ways to work on the project:
1. Manually set up the database and virtual environment.
2. Use docker container to run the database server and api server automatically.

You can choose either way to work on the project.

## Dependencies 
####If you are manually setting up:
Ensure that you have a virtual environment setup.

```
# For MacOS
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

Then goto `api/` folder using `cd api` ,

Install dependencies: `pip install -r requirements.txt`

Update dependencies: `pip install pipreqs` and `pipreqs .`

####If you are using Docker:
Download docker desktop from https://www.docker.com/products/docker-desktop/
This will automatically install docker and docker-compose. Both are required.

Then open the 'terminal' if you are using MacOS or Linux.
For Windows users, use 'git bash' or 'wsl' or 'wsl2' (powershell and cmd will not work)

goto the project directory using `cd` and run `source env_setup.sh`. This will allow you to shortcut many docker commands
checkout the available commands using `api-server --help` or `api-server -h`.

> You should type `source env_setup.sh` everytime before using `api-server` command, or you can register `source env_setup.sh` to `~/.zprofile` file if you are using MacOS. If you are using Linux, `~/.bashrc` or `~/.bash_profile` should work.

## Database
### Initial MySQL setup
#### For Manual setup:
Open DB

```
brew install mysql
mysql -u root
```

Setup DB

```
# inside MySQL
CREATE DATABASE cs348_project;
USE cs348_project;
create user 'group8'@'localhost' identified by 'Password0!';
grant all on cs348_project.* to 'group8'@'localhost';
alter user 'group8'@'localhost' identified with mysql_native_password by 'Password0!';
```

#### For Docker setup:
Doesn't require any action
### Set up tables and data
#### For Manual setup:
Run migrations to create all database tables: `flask db upgrade`

Seed database: `flask seed all`
#### For Docker setup:
`flask db upgrade` is automatically done by Docker.

If you want to seed database using `flask seed all`, use docker-desktop -> containers -> api-1 -> terminal -> `bash` command -> `cd src` command -> `flask seed all` command.

OR

You can use `api-server connect api` -> `cd src` command -> `flask seed all` command. (in your terminal environment)
## Setup Flask
#### For Manual setup:
Run the server with `python -m flask run`

Run with debug mode (auto-reloading after file changes) using `python -m flask run --debug`

You can now try getting response by going to `http://127.0.0.1:6608`

#### For Docker setup:
run `api-server up` or `api-server start`, it will automatically start flask server. Openning to `http://localhost:6608`.

You can also inspect/modify Database in GUI: goto `http://localhost:8080` and login to database:
* System: MySQL
* Server: db
* Username: group8
* Password: Password0!
* Database: cs348_project
# Development
## Structure of project
- Flask project is structured as a package named `cs348_api`
- Database interactions are handled with `flask-sqlalchemy` ORM
   - ORM models for data are defined in `models` subpackage
- Migrations are handled with `flask-migrate` and are stored in `/migrations`
- SQL queries for assignment submission are stored in `doc/sql`
- API endpoints are defined in `/routes` based on the relevant resource
   - e.g. food API endpoints are in `/routes/food_item.py`
   - `/routes/index.py` handles base route (e.g. localhost:6608/)

## Updating database
To update the database schema:
1. Update `models.py` with new schema
2. Run `flask db migrate -m <message>` to create a migration for this change
3. Run `flask migrate upgrade` to run the migration

To update seed data:
1. Update `/views/seed.py` with a new function decorated with `@seed_blueprint.cli.command("cmd_name")`
2. Run new command using `flask seed <cmd_name>`
