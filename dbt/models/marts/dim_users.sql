{{ config(
    materialized='incremental',
    unique_key='user_id',
    schema='heymax_datamart'
) }}

SELECT
  user_id,
  platform,
  utm_source,
  country,
  MIN(event_timestamp) AS first_seen,
  MAX(event_timestamp) AS last_seen
FROM `heymax-analytics.heymax_staging.stg_events`
GROUP BY user_id,platform,utm_source,country

{% if is_incremental() %}
  HAVING MAX(event_timestamp) > (SELECT MAX(last_seen) FROM {{ this }})
{% endif %}
