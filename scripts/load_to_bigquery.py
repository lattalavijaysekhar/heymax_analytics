import os
import traceback
from google.cloud import bigquery

def load_to_bigquery(dataset_id, table_id, source_uri, project_id):
    try:
        client = bigquery.Client(project=project_id)
        table_ref = client.dataset(dataset_id).table(table_id)

        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        load_job = client.load_table_from_uri(
            source_uri,
            table_ref,
            job_config=job_config,
        )

        print("Waiting for load job to complete...")
        load_job.result()

        print(f"Loaded data to {dataset_id}.{table_id}")
    except Exception as e:
        print("Error loading to BigQuery:")
        print(f"Message: {str(e)}")
        traceback.print_exc()
        raise

if __name__ == "__main__":
    try:
        # Replace these with your actual values
        load_to_bigquery(
            dataset_id="heymax_staging",
            table_id="stg_events",
            source_uri="gs://heymax-raw/event_stream.csv",
            project_id="heymax-analytics"
        )
    except Exception as e:
        print("Unhandled error in main:")
        print(f"Message: {str(e)}")
        traceback.print_exc()
        raise
