# Goal View
WITH T1 as (
    SELECT user_id, sum(calories) as calories, sum(fat) as fat, sum(carb) as carb, sum(fiber) as fiber, sum(protein) as protein
    FROM food_log
    INNER JOIN food_item on food_item.id = food_log.food_item_id
    WHERE user_id = <User ID>
    AND DATE(created_at) = CURDATE()
    GROUP BY user_id
),

T2 as (
    SELECT T1.user_id, goal.name, goal.goal_type, goal.quantity,
    CASE 
    WHEN goal.goal_type = 'Calorie' THEN T1.calories 
    WHEN goal.goal_type = 'Fat' THEN T1.fat
    WHEN goal.goal_type = 'Carb' THEN T1.carb
    WHEN goal.goal_type = 'Fiber' THEN T1.fiber
    WHEN goal.goal_type = 'Protein' THEN T1.protein
    END as consumption
    FROM goal INNER JOIN T1 on T1.user_id = goal.user_id
    WHERE goal.user_id = <User ID>
)

SELECT name, goal_type, quantity, consumption,
    CASE
    WHEN consumption > quantity THEN 'Goal Achieved'
    ELSE 'Goal not Achieved'
    END as status
    from T2;
