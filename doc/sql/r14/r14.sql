-- Active: 1684965384395@@localhost@3306@nutritrack
# Verify if a user is admin by checking the "role" column
SELECT email, role FROM User WHERE email=<email>; 

# Edit a food
UPDATE food_item SET name = <name>, calories = <calories>, carb = <carb>, fat = <fat>, fiber = <fiber>, protein = <protein>
WHERE id = <id>;

# Create a food
INSERT INTO food_item (name, restaurant_id, calories, carb, fat, fiber, protein)
VALUES (<name>, <restaurant_id>, <calories>, <carb>, <fat>, <fiber>, <protein>);

# Create a restaurant
INSERT INTO restaurant VALUES (<name>);

### Sample queries
# Verify if a user is admin by checking the "role" column
SELECT email, role FROM user WHERE email="tammy76@example.com"; 

# Edit a food
UPDATE food_item SET name = "Bacon & Cheese Whopper® Sandwich", calories = 700, carb = 50, fat = 50, fiber = 2, protein = 50
WHERE id = 2;

# Create a food
INSERT INTO food_item (name, restaurant_id, calories, carb, fat, fiber, protein)
VALUES ("new food", 2, 1000, 50, 50, 1, 25);

# Create a restaurant
INSERT INTO restaurant (name) VALUES ("My restaurant");