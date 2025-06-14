from google.cloud import storage
import os

def upload_to_gcs(bucket_name, source_file_path, destination_blob_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/service_account.json"
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_path)
    blob.upload_from_filename(source_file_path)
    print(f"Uploaded {source_file_path} to gs://{bucket_name}/{destination_blob_path}")

upload_to_gcs('heymax-raw', 'data/sample_events.csv', 'events/sample_events.csv')
