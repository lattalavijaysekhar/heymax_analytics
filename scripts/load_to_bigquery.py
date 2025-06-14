from google.cloud import bigquery

def load_from_gcs_to_bq():
    client = bigquery.Client()
    uri = "gs://heymax-raw/events/sample_events.csv"
    table_id = "your-project.heymax_staging.raw_events"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE"
    )
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()
    print(f"Loaded data to {table_id}")

load_from_gcs_to_bq()
