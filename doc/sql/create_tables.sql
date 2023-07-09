CREATE TABLE restaurant (
        id INTEGER NOT NULL AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
);

CREATE TABLE food_item (
        id INTEGER NOT NULL AUTO_INCREMENT,
        name VARCHAR(255),
        restaurant_id INTEGER NOT NULL,
        calories INTEGER,
        fat INTEGER,
        carb INTEGER,
        fiber INTEGER,
        protein INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(restaurant_id) REFERENCES restaurant (id)
);

CREATE TABLE user (
        id INTEGER NOT NULL AUTO_INCREMENT,
        name VARCHAR(255),
        password VARCHAR(255),
        email VARCHAR(255),
        PRIMARY KEY (id),
        UINQUE KEY email(email)
);

CREATE TABLE food_log (
        id INTEGER NOT NULL AUTO_INCREMENT,
        user_id INTEGER NOT NULL,
        food_item_id INTEGER NOT NULL,
        created_at DATETIME DEFAULT now(),
        PRIMARY KEY (id),
        FOREIGN KEY(food_item_id) REFERENCES food_item (id),
        FOREIGN KEY(user_id) REFERENCES user (id)
);
