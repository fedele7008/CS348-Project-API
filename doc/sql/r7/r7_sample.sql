-- Active: 1684965384395@@localhost@3306@cs348_project
SELECT food.name, food.calories, food.fat, food.carb, food.fiber, food.protein, log.created_at
FROM food_log as log
LEFT JOIN food_item as food on food.id = log.food_item_id
WHERE user_id = 1;

UPDATE food_log
SET food_item_id = 3
WHERE id = 1;

DELETE FROM food_log
WHERE id = 3;

INSERT INTO food_log (user_id, food_item_id, created_at) VALUES (1, 3, CURRENT_TIMESTAMP);
