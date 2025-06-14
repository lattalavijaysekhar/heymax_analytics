from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import subprocess
import os
import requests

def notify_slack(context):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if webhook_url:
        task = context.get('task_instance')
        msg = f":red_circle: DAG `{task.dag_id}` Task `{task.task_id}` failed"
        requests.post(webhook_url, json={"text": msg})

def run_script(script_name):
    subprocess.run(["python3", f"/home/airflow/gcs/dags/scripts/{script_name}"], check=True)

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

with DAG(
    dag_id="daily_event_pipeline",
    default_args=default_args,
    catchup=False,
    tags=["heymax", "analytics"]
) as dag:

    upload_csv = PythonOperator(
        task_id="upload_csv_to_gcs",
        python_callable=run_script,
        op_args=["load_to_gcs.py"]
    )

    load_bq = PythonOperator(
        task_id="load_csv_to_bigquery",
        python_callable=run_script,
        op_args=["load_to_bigquery.py"]
    )

    run_dbt = BashOperator(
        task_id="run_dbt_models",
        bash_command="cd /home/airflow/gcs/dags/dbt/heymax_dbt && dbt run --profiles-dir ."
    )

    test_dbt = BashOperator(
        task_id="test_dbt_models",
        bash_command="cd /home/airflow/gcs/dags/dbt/heymax_dbt && dbt test --profiles-dir ."
    )

    upload_csv >> load_bq >> run_dbt >> test_dbt
