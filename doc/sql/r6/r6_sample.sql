-- Sample data query
SELECT food_item.name, calories, fat, carb, fiber, protein
FROM food_item 
INNER JOIN restaurant on food_item.restaurant_id = restaurant.id
WHERE restaurant.name = 'McDonalds';
