-- Index Optimization
CREATE INDEX idx_food_log_created_at ON food_log (created_at);

-- Most popular foods
SELECT fitem.id, fitem.name, COUNT(*) AS purchase_count
FROM food_log AS flog
JOIN food_item AS fitem ON flog.food_item_id = fitem.id
WHERE DATE(flog.created_at) BETWEEN <start_date> AND <end_date>
GROUP BY fitem.id, fitem.name
HAVING COUNT(*) > <min_count>
ORDER BY purchase_count <choice>;

-- Most popular restaurants
SELECT restaurant.id, restaurant.name, COUNT(*) AS purchase_count
FROM food_log AS flog
JOIN food_item AS fitem ON flog.food_item_id = fitem.id
JOIN restaurant ON fitem.restaurant_id = restaurant.id
WHERE flog.created_at >= <start_date> AND flog.created_at <= <end_date>
GROUP BY restaurant.id, restaurant.name
HAVING COUNT(*) > <min_count>
ORDER BY purchase_count <choice>;

-- Most popular foods in restaurants
SELECT fitem.id, fitem.name, COUNT(*) AS purchase_count
FROM food_log AS flog
JOIN food_item AS fitem ON flog.food_item_id = fitem.id
WHERE DATE(flog.created_at) BETWEEN <start_date> AND <end_date>
AND restaurant.id = <id> 
GROUP BY fitem.id, fitem.name
HAVING COUNT(*) > <min_count>
ORDER BY purchase_count <choice>;

-- Sample Production SQL
SELECT restaurant.id, restaurant.name, COUNT(*) AS purchase_count
FROM food_log AS flog
JOIN food_item AS fitem ON flog.food_item_id = fitem.id
JOIN restaurant ON fitem.restaurant_id = restaurant.id
WHERE DATE(flog.created_at) BETWEEN '2023-04-17' AND now()
GROUP BY restaurant.id, restaurant.name
HAVING COUNT(*) > 2
ORDER BY purchase_count DESC;
