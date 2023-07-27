-- Most popular foods
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
WITH foods_in_date AS
(
	SELECT  fitem.id
	       ,name
	FROM food_log AS flog
	JOIN food_item AS fitem
	ON flog.food_item_id = fitem.id
	WHERE DATE(flog.created_at) BETWEEN '2023-04-17' AND now()
)
SELECT  id
       ,name
       ,COUNT(*) AS purchase_count
FROM foods_in_date
GROUP BY  id
HAVING purchase_count > 2
ORDER BY purchase_count DESC;

-- Most popular restaurants
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
WITH foods_and_restaurants_in_date AS
(
	SELECT  restaurant.id
	       ,restaurant.name
	FROM food_log AS flog
	JOIN food_item AS fitem
	ON flog.food_item_id = fitem.id
	JOIN restaurant
	ON fitem.restaurant_id = restaurant.id
	WHERE DATE(flog.created_at) BETWEEN '2023-04-17' AND now()
)
SELECT  id
       ,name
       ,COUNT(*) AS purchase_count
FROM foods_and_restaurants_in_date
GROUP BY  id
HAVING purchase_count > 2
ORDER BY purchase_count DESC;

-- Most popular foods at a restaurant
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
WITH foods_at_restaurant_in_date AS
(
	SELECT  fitem.id
	       ,fitem.name
	FROM food_log AS flog
	JOIN food_item AS fitem
	ON flog.food_item_id = fitem.id
	JOIN restaurant
	ON fitem.restaurant_id = restaurant.id
	WHERE DATE(flog.created_at) BETWEEN '2022-04-17' AND now()
	AND restaurant.id = 1
)
SELECT  id
       ,name
       ,COUNT(*) AS purchase_count
FROM foods_at_restaurant_in_date
GROUP BY  id
HAVING purchase_count > 2
ORDER BY purchase_count DESC;
