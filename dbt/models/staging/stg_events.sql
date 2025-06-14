{{ config(
    materialized='table',
    schema='heymax_staging'
) }}

SELECT
  user_id,
  TIMESTAMP(event_time) AS event_timestamp,
  event_type
FROM {{ source('staging', 'raw_events') }}
