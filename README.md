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
- `superset/`: Dashboard setup instructions
- `.github/workflows/`: dbt CI
- `data/`: Sample CSV

## 🔍 Growth Metrics

- Active Users (DAU/WAU/MAU)
- New vs Retained vs Resurrected vs Churned
- Triangle Retention (cohort-based)

## ✅ Execution Steps

1. Upload file to GCS:
```bash
python scripts/load_to_gcs.py
```

2. Load from GCS to BigQuery:
```bash
python scripts/load_to_bigquery.py
```

3. Run Airflow DAG (`daily_event_pipeline`) via Composer or UI.

4. View tables in BigQuery:
- `heymax_analytics.dim_users`
- `heymax_analytics.fct_events`

5. Visualize in Superset.

## 🚨 Alerting

Airflow DAG includes a Slack webhook for failure alerts. Configure it via ENV variable: `SLACK_WEBHOOK_URL`.

---
