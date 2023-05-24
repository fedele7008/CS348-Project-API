# CS348-Project-API

CS 348 Project: Introduction to Database Management

# Setup instructions

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
CREATE TABLE food(uid DECIMAL(3, 0) NOT NULL PRIMARY KEY, name VARCHAR(30), calories INT);
INSERT INTO food VALUES(1, 'burger' 400);
INSERT INTO food VALUES(2, 'fries', 300);
INSERT INTO food VALUES(1, 'coke', 150);
create user 'group8'@'localhost' identified by 'Password0!';
grant all on testDB.* to 'group8'@'localhost';
alter user 'group8'@'localhost' identified with mysql_native_password by 'Password0!';
```

Ensure that you have a virtual environment setup.

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

You should see (venv) in your terminal now.

Setup Flask

```
pip install flask
FLASK_APP=helloworld
FLASK_ENV=development
flask run -p 5001
```

You can now try getting response by going to `http://127.0.0.1:5001`
