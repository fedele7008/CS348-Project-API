WITH T1 as (
    SELECT user_id, sum(calories) as calories, sum(fat) as fat, sum(carb) as carb, sum(fiber) as fiber, sum(protein) as protein
    FROM food_log
    INNER JOIN food_item on food_item.id = food_log.food_item_id
    WHERE user_id = 1
    AND created_at = '2023-06-04 15:00:00'
    GROUP BY user_id
),

T2 as (
    SELECT T1.user_id, goal.name, goal.goal_type, goal.quantity, goal.streak,
    CASE 
    WHEN goal.goal_type = 'Calorie' THEN T1.calories 
    WHEN goal.goal_type = 'Fat' THEN T1.fat
    WHEN goal.goal_type = 'Carb' THEN T1.carb
    WHEN goal.goal_type = 'Fiber' THEN T1.fiber
    WHEN goal.goal_type = 'Protein' THEN T1.protein
    END as consumption
    FROM goal INNER JOIN T1 on T1.user_id = goal.user_id
    WHERE goal.user_id = 1
)

SELECT name, goal_type, quantity, consumption,
    CASE
    WHEN consumption > quantity THEN 'Goal Achieved'
    ELSE 'Goal not Achieved'
    END as status,
    streak
    from T2;

# Streak Counting
WITH T1 as (
    SELECT user_id, sum(calories) as calories, sum(fat) as fat, sum(carb) as carb, sum(fiber) as fiber, sum(protein) as protein
    FROM food_log
    INNER JOIN food_item on food_item.id = food_log.food_item_id
    WHERE created_at = '2023-06-04 15:00:00'
    GROUP BY user_id
),

T2 as (
    SELECT T1.user_id, goal.id, goal.name, goal.goal_type, goal.quantity, goal.streak,
    CASE 
    WHEN goal.goal_type = 'Calorie' THEN T1.calories 
    WHEN goal.goal_type = 'Fat' THEN T1.fat
    WHEN goal.goal_type = 'Carb' THEN T1.carb
    WHEN goal.goal_type = 'Fiber' THEN T1.fiber
    WHEN goal.goal_type = 'Protein' THEN T1.protein
    END as consumption
    FROM goal INNER JOIN T1 on T1.user_id = goal.user_id
)

UPDATE
    goal,
    T2
SET goal.streak = CASE
    WHEN T2.consumption >= T2.quantity THEN goal.streak + 1
    ELSE 0
    END 
WHERE
    goal.id = T2.id;
