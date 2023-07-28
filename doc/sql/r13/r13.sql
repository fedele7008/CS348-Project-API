# Streak Counting Query
WITH T1 as (
    SELECT user_id, sum(calories) as calories, sum(fat) as fat, sum(carb) as carb, sum(fiber) as fiber, sum(protein) as protein
    FROM food_log
    INNER JOIN food_item on food_item.id = food_log.food_item_id
    WHERE DATE(created_at) = CURDATE()
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

# Scheduled streak updating event
CREATE EVENT IF NOT EXISTS `goal_streaks`
ON SCHEDULE
  EVERY '1' DAY
  DO
        WITH T1 as (
        SELECT user_id, sum(calories) as calories, sum(fat) as fat, sum(carb) as carb, sum(fiber) as fiber, sum(protein) as protein
        FROM food_log
        INNER JOIN food_item on food_item.id = food_log.food_item_id
        WHERE DATE(created_at) = CURDATE()
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