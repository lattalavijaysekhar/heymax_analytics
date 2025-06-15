# dbt Models

This folder contains all dbt models for the HeyMax analytics project.

## Structure

- `marts/`: Contains business-facing tables such as `fct_events` and `dim_users`.
- `staging/`: (Removed) Previously used for loading `stg_events`, which is now loaded directly via Python.

## Notes

- dbt `marts` models are built incrementally.
- Staging data is handled via the Airflow DAG (`load_to_bigquery.py`) and not via dbt anymore.
