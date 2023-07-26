SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
WITH user_foods AS
(
        SELECT  fitem.calories
               ,flog.created_at
        FROM food_log AS flog
        JOIN food_item AS fitem
        ON flog.food_item_id = fitem.id
        WHERE flog.user_id = <id>
)
SELECT  DATE(created_at) as foodDate
       ,SUM(calories) as calorieSum
FROM user_foods
GROUP BY  DATE(created_at);
