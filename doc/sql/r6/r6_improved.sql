-- Index Optimization
CREATE INDEX idx_food_item_restaurant_id ON food_log (restaurant_id);

SELECT food_item.name, calories, fat, carb, fiber, protein
FROM food_item 
WHERE EXISTS (
    SELECT 1 
    FROM restaurant 
    WHERE food_item.restaurant_id = restaurant.id 
    AND restaurant.name = <Restaurant Name>
); 

SELECT name, calories, fat, carb, fiber, protein
FROM food_item 
WHERE name = <foodName>;
