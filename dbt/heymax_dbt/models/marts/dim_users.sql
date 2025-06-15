{{ config(
    materialized='incremental',
    unique_key='user_id'
) }}

SELECT
  user_id,
  country,
  MIN(event_time) AS first_seen,
  MAX(event_time) AS last_seen
FROM `heymax-analytics.heymax_staging.stg_events`
GROUP BY user_id,country

{% if is_incremental() %}
  HAVING MAX(event_time) > (SELECT MAX(last_seen) FROM {{ this }})
{% endif %}
