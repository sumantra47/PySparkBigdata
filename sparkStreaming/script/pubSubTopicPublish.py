from google.cloud import storage
from google.cloud import pubsub_v1
import json

GCS_BUCKET = "practise-dev-data"
GCS_PATH = "events.json"
PUBSUB_PROJECT = "practise-dev"
PUBSUB_TOPIC = "practise-dev-topic"

def read_json_from_gcs(bucket, path):
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(path)
    content = blob.download_as_text()
    return json.loads(content)

def publish_messages(messages, project_id, topic_name):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    for msg in messages:
        message_json = json.dumps(msg)
        publisher.publish(topic_path, message_json.encode("utf-8"))
        print(f"Published: {message_json}")

def main():
    data = read_json_from_gcs(GCS_BUCKET, GCS_PATH)
    first_10 = data[:10]
    publish_messages(first_10, PUBSUB_PROJECT, PUBSUB_TOPIC)

if __name__ == "__main__":
    main()