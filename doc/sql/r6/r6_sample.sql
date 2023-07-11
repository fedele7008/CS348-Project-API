SELECT food_item.name, calories, fat, carb, fiber, protein
FROM food_item 
INNER JOIN restaurant on food_item.restaurant_id = restaurant.id
WHERE restaurant.name = 'McDonalds';

SELECT food_item.name, calories, fat, carb, fiber, protein
FROM food_item 
WHERE EXISTS (
    SELECT 1 
    FROM restaurant 
    WHERE food_item.restaurant_id = restaurant.id 
    AND restaurant.name = 'McDonalds'
); 