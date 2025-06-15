# 📊 HeyMax Analytics Data Pipeline

This project implements a production-ready, end-to-end analytics pipeline for ingesting user event data into BigQuery, transforming it with dbt, and visualizing metrics using Superset.

## ⚙️ Stack Overview

- **Storage**: Google Cloud Storage (GCS)
- **Data Warehouse**: BigQuery
- **Transformation**: dbt (modular SQL models)
- **Orchestration**: Cloud Composer (Airflow)
- **Visualization**: Superset
- **Monitoring**: Slack/Email alerts

## 🚀 Flow

```
Local CSV → GCS → BigQuery (Staging) → dbt Models → Superset
                  ⬑ Airflow DAG every 10 mins with alerting
```

## 📁 Structure

- `dags/`: Airflow DAG with Slack alert integration
- `dbt/heymax_dbt/`: Models, tests, docs, and configs
- `scripts/`: Utility scripts for GCS/BQ
- `superset/`: Dashboard setup instructions, Sample Visualizations pdf, and View Query
- `.github/workflows/`: dbt CI
- `data/`: Sample CSV

## 🔍 Growth Metrics

- Active Users (DAU/WAU/MAU)
- New vs Retained vs Resurrected vs Churned
- Triangle Retention (cohort-based)

## ✅ Execution Steps

1. Run Airflow DAG (`daily_event_pipeline`) via Composer or UI.
```
This is scheduled to run for every 10 minutes and will run all the above scripts mentioned in the flow.
```

2. View tables in BigQuery:
- `heymax-analytics.heymax_staging.stg_events`
- `heymax-analytics.heymax_datamart.dim_users`
- `heymax-analytics.heymax_datamart.fct_events`

3. Visualize in Superset.

## 🚨 Alerting

Airflow DAG includes a Slack webhook for failure alerts. Configure it via ENV variable: `SLACK_WEBHOOK_URL`.

## 🧠 Design Tradeoffs

- **Batch vs Streaming**: Opted for micro-batch (every 10 minutes) using Airflow for cost-effectiveness and simplicity. This balances latency and infrastructure overhead while still supporting near real-time use cases.
- **Storage-first approach**: GCS is used as a landing zone to enable replayability, versioning, and future enhancements like schema validation or file-based audit trails.
- **dbt as transformation layer**: Chosen for modularity, documentation, version control, and testability.
- **Superset for BI**: Chosen for free, open-source, and extensible—but compared to commercial tools, it may have limitations around complex drill-downs and export flexibility.

## 🧪 Testing

- **Unit Testing in dbt**: dbt tests added for uniqueness, null checks, referential integrity.
- **CI via GitHub Actions**: Validates dbt model builds on every push.

## 📈 Scaling Considerations

- **Data Volume**: BigQuery is scalable; partitioned by event_date and clustered by user_id in `fct_events` for optimal query performance.
- **Orchestration**: Composer (Airflow) supports scaling with DAG concurrency and worker pools.
- **Modular dbt Models**: Allows refactoring without touching all layers; supports snapshotting and incremental loads.
- **Superset**: Can be containerized and scaled with Gunicorn and Celery workers for concurrent dashboard users.

## 📌 Assumptions

- CSVs follow a consistent schema and are UTF-8 encoded.
- Events contain a valid `user_id`, `event_type`, and `event_timestamp`.
- Airflow and Superset environments are preconfigured with appropriate service account permissions.
- dbt is connected to BigQuery via `profiles.yml` under the correct target.
- CI/CD pipelines have access to secret variables (e.g., GCP credentials, Slack webhook).
- Time zone defaults to UTC unless specified.
---
