{{ config(
    materialized='incremental',
    unique_key='user_id||event_date||event_type',
    partition_by={
        "field": "event_date",
        "data_type": "date"
    },
    cluster_by=["user_id"]
) }}

WITH base AS (
  SELECT
    user_id,
    event_type,
    event_time,
    DATE(event_time) AS event_date,
    transaction_category,
    miles_amount,
    platform,
    utm_source,
    country
  FROM `heymax-analytics.heymax_staging.stg_events`
)

SELECT *
FROM base
{% if is_incremental() %}
WHERE DATE(event_time) > (SELECT MAX(event_date) FROM {{ this }})
{% endif %}
