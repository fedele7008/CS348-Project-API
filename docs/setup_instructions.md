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

Start Flask server

```
flask run -p 5001
```

Try getting response by going to `http://127.0.0.1:5001`
