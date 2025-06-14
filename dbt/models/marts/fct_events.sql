{{ config(
    materialized='incremental',
    unique_key='user_id||event_date||event_type',
    schema='heymax_datamart'
) }}

SELECT * FROM {{ ref('staging_events') }}

{% if is_incremental() %}
  HAVING MAX(DATE(event_timestamp)) > (SELECT MAX(event_date) FROM {{ this }})
{% endif %}
