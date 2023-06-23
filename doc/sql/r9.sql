# View log
SELECT food.name, food.calories, food.fat, food.carb, food.fiber, food.protein, log.created_at
FROM food_log as log
LEFT JOIN food_item as food on food.id = log.food_item_id
WHERE user_id = current_user_id;

# update log
UPDATE food_log
SET food_item_id = newID
WHERE id = log_id;

# Delete log
DELETE FROM food_log
WHERE id = log_id;


