WITH user_foods AS
(
        SELECT  fitem.calories, fitem.fat, fitem.carb, fitem.fiber, fitem.protein
               ,flog.created_at
        FROM food_log AS flog
        JOIN food_item AS fitem
        ON flog.food_item_id = fitem.id
        WHERE flog.user_id = 2
)
SELECT  DATE(created_at) as foodDate
       ,SUM(calories) as calorieSum
       ,SUM(fat) as fatSum
       ,SUM(carb) as carbSum
       ,SUM(fiber) as fiberSum
       ,SUM(protein) as proteinSum
FROM user_foods
GROUP BY  DATE(created_at);
