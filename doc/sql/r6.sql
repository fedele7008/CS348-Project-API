SELECT name, calories, fat, carb, fiber, protein
FROM food_item 
INNER JOIN restaurant on food_item.restaunrant_id = restaurant.id
WHERE restaurant.name = inputName;
