{{ config(
    materialized='incremental',
    unique_key='user_id||event_time||event_type'
) }}

SELECT * FROM `heymax-analytics.heymax_staging.stg_events`

{% if is_incremental() %}
  WHERE event_time > (SELECT MAX(event_time) FROM {{ this }})
{% endif %}
