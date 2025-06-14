from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.hooks.base import BaseHook
from airflow.operators.http_operator import SimpleHttpOperator
from datetime import datetime
import os
import requests
from google.cloud import bigquery

def load_to_bigquery():
    client = bigquery.Client()
    uri = "gs://heymax-raw/events/sample_events.csv"
    table_id = "heymax-analytics.heymax_staging.raw_events"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE"
    )
    client.load_table_from_uri(uri, table_id, job_config=job_config).result()

def notify_slack(context):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if webhook_url:
        task = context.get('task_instance')
        message = f":rotating_light: Task Failed: {task.task_id} in DAG {task.dag_id}"
        requests.post(webhook_url, json={"text": message})

with DAG("daily_event_pipeline",
         start_date=days_ago(1),
         schedule_interval="*/10 * * * *",
         catchup=False,
         on_failure_callback=notify_slack) as dag:

    load_bq = PythonOperator(
        task_id="load_csv_to_bigquery",
        python_callable=load_to_bigquery
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="cd /home/airflow/gcs/dags/dbt/heymax_dbt && dbt run"
    )

    test_dbt = BashOperator(
        task_id="test_dbt",
        bash_command="cd /home/airflow/gcs/dags/dbt/heymax_dbt && dbt test"
    )

    load_bq >> run_dbt >> test_dbt
