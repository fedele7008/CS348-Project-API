# From generated sqlalchemy call
CREATE TABLE restaurant (
        id INTEGER NOT NULL AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
)

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
)