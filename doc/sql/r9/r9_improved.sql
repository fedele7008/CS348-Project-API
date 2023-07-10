-- Index Optimization
CREATE INDEX idx_food_log_user_id ON food_log (user_id);

SELECT DATE(flog.created_at) as foodDate, SUM(fitem.calories) as calorieSum
FROM food_log AS flog
JOIN food_item AS fitem ON flog.food_item_id = fitem.id
WHERE flog.user_id = <id>
GROUP BY DATE(flog.created_at);

-- Sample Prod SQL
SELECT DATE(flog.created_at) as foodDate, SUM(fitem.calories) as calorieSum
FROM food_log AS flog
JOIN food_item AS fitem ON flog.food_item_id = fitem.id
WHERE flog.user_id = 2
GROUP BY DATE(flog.created_at);
