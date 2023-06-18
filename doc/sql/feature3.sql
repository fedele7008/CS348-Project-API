-- Most popular foods
WITH foods_in_date AS
(
	SELECT  *
	FROM food_log AS flog
	JOIN food_item AS fitem
	ON flog.food_item_id = fitem.id
	WHERE DATE(flog.created_at) BETWEEN before_date AND after_date
)
SELECT  fitem.id
       ,fitem.name
FROM foods_in_date
GROUP BY  fitem.id

-- Most popular restaurants
WITH foods_and_restaurants_in_date AS
(
	SELECT  *
	FROM food_log AS flog
	JOIN food_item AS fitem
	ON flog.food_item_id = fitem.id
	JOIN restaurant
	ON fitem.restaurant_id = restaurant.id
	WHERE DATE(flog.created_at) BETWEEN before_date AND after_date
)
SELECT  restaurant.id
       ,restaurant.name
FROM foods_in_date
GROUP BY  restaurant.id
