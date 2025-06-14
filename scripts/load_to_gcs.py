import os
import traceback
from google.cloud import storage

def upload_to_gcs(bucket_name, source_file_path, destination_blob_path):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_path)
        blob.upload_from_filename(source_file_path)
        print(f"Uploaded {source_file_path} to gs://{bucket_name}/{destination_blob_path}")
    except Exception as e:
        print("Error uploading to GCS:")
        print(f"Message: {str(e)}")
        traceback.print_exc()
        raise  # So Airflow knows to mark task as failed

if __name__ == "__main__":
    try:
        # This is the Composer DAGs mount path
        source_file_path = "/home/airflow/gcs/dags/data/event_stream.csv"

        # Use your raw bucket and blob destination
        upload_to_gcs(
            bucket_name="heymax-raw",
            source_file_path=source_file_path,
            destination_blob_path="events/event_stream.csv"
        )
    except Exception as e:
        print("Unhandled error in main:")
        print(f"Message: {str(e)}")
        traceback.print_exc()
        raise
