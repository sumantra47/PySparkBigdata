import json
import datetime
from google.cloud import storage
from google.cloud import pubsub_v1

GCS_BUCKET = "practise-dev-data"
GCS_PATH = "events.json"

PUBSUB_PROJECT = "practise-dev"
PUBSUB_TOPIC = "practise-dev-topic"


def read_json_from_gcs(bucket_name, file_path):
    """Reads a JSON file stored in GCS."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    content = blob.download_as_text()
    return json.loads(content)


def publish_to_pubsub(data):
    """Publishes the first 10 JSON records to Pub/Sub (Standard)."""

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PUBSUB_PROJECT, PUBSUB_TOPIC)

    with publisher:
        for row in data[:10]:
            # Add event timestamp
            now = datetime.datetime.now()
            row["event_date"] = now.strftime("%Y-%m-%d %H:%M:%S")

            # Convert JSON to bytes
            message_bytes = json.dumps(row).encode("utf-8")

            # Publish
            future = publisher.publish(topic_path, message_bytes)
            message_id = future.result()

            print(f"Published: {row} → Message ID: {message_id}")


if __name__ == "__main__":
    data = read_json_from_gcs(GCS_BUCKET, GCS_PATH)
    publish_to_pubsub(data)
    