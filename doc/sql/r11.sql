WITH T1 as (
    SELECT uid, sum(calories) as calories, sum(protein) as protein, ...
    FROM log
    GROUP BY uid
),

T2 as (
    SELECT uid, goal.type, goal.goal_value
    CASE 
    WHEN goal.type = 'Calories' THEN T1.calories 
    ...
    END as achieved
    FROM T1 INNER JOIN goal on uid
)

