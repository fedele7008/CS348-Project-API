CREATE FUNCTION delete_food(foodName varchar(20))
	BEGIN
	DELETE FROM FoodItem
WHERE ItemName=foodName
END

UPDATE food_log

