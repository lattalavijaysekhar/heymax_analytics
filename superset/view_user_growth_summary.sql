CREATE OR REPLACE VIEW `heymax-analytics.heymax_datamart.view_user_growth_summary` AS
WITH active_users AS (
  SELECT 
    DATE(event_time) AS event_date,
    user_id
  FROM `heymax-analytics.heymax_datamart.fct_events`
  GROUP BY event_date, user_id
),

user_status AS (
  SELECT 
    curr.event_date,
    curr.user_id,
    CASE WHEN DATE(d.first_seen) = curr.event_date THEN 1 ELSE 0 END AS is_new,
    CASE 
      WHEN DATE(d.first_seen) < curr.event_date AND EXISTS (
        SELECT 1 FROM active_users prev
        WHERE prev.user_id = curr.user_id
        AND prev.event_date = DATE_SUB(curr.event_date, INTERVAL 1 DAY)
      ) THEN 1 ELSE 0 
    END AS is_retained,
    CASE 
      WHEN DATE(d.first_seen) < curr.event_date AND NOT EXISTS (
        SELECT 1 FROM active_users prev
        WHERE prev.user_id = curr.user_id
        AND prev.event_date = DATE_SUB(curr.event_date, INTERVAL 1 DAY)
      ) THEN 1 ELSE 0 
    END AS is_resurrected
  FROM active_users curr
  JOIN `heymax-analytics.heymax_datamart.dim_users` d USING(user_id)
),

churned_users AS (
  SELECT 
    DATE_SUB(curr.event_date, INTERVAL 1 DAY) AS event_date,
    COUNT(DISTINCT curr.user_id) AS churned_users
  FROM active_users curr
  WHERE NOT EXISTS (
    SELECT 1 FROM active_users next
    WHERE next.user_id = curr.user_id
      AND next.event_date = DATE_ADD(curr.event_date, INTERVAL 1 DAY)
  )
  GROUP BY event_date
)

-- Final UNION output with additional grain fields
SELECT 
  event_date,
  DATE_TRUNC(event_date, MONTH) AS event_month,
  COUNT(DISTINCT user_id) AS active_users,
  SUM(is_new) AS new_users,
  SUM(is_retained) AS retained_users,
  SUM(is_resurrected) AS resurrected_users,
  0 AS churned_users
FROM user_status
GROUP BY event_date, event_month

UNION ALL

SELECT
  churned_users.event_date,
  DATE_TRUNC(event_date, MONTH) AS event_month,
  0 AS active_users,
  0 AS new_users,
  0 AS retained_users,
  0 AS resurrected_users,
  IFNULL(churned_users.churned_users, 0) AS churned_users
FROM churned_users;