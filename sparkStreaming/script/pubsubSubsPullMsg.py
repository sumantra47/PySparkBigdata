from pyspark.sql import SparkSession
from google.cloud import pubsub_v1
import json

# -------------------------------
# Spark session
# -------------------------------
spark = SparkSession.builder \
    .appName("PubSubReader") \
    .getOrCreate()

# -------------------------------
# Subscription path
# -------------------------------
PROJECT_ID = "practise-dev"
SUBSCRIPTION_ID = "practise-dev-sub-test"
subscription_path = f"projects/{PROJECT_ID}/subscriptions/{SUBSCRIPTION_ID}"

# -------------------------------
# Define the foreachBatch function
# -------------------------------
def read_from_pubsub(batch_df, batch_id):
    """
    This function runs for each micro-batch.
    Pulls messages from Pub/Sub using the Python client and prints them.
    """
    subscriber = pubsub_v1.SubscriberClient()

    # Pull messages from Pub/Sub (max 10 per batch)
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 10}
    )

    if not response.received_messages:
        print(f"Batch {batch_id}: No new messages.")

    for msg in response.received_messages:
        # Decode message data
        message_data = msg.message.data.decode("utf-8")
        try:
            # If message is JSON, parse it
            json_data = json.loads(message_data)
            print(f"Batch {batch_id} - Message: {json_data}")
        except json.JSONDecodeError:
            print(f"Batch {batch_id} - Message: {message_data}")

        # Acknowledge message
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": [msg.ack_id]}
        )

# -------------------------------
# Create an empty streaming DataFrame
# -------------------------------
# We just need a dummy stream to trigger foreachBatch
df = spark.readStream \
    .format("rate") \
    .option("rowsPerSecond", 1) \
    .load()

# -------------------------------
# Apply foreachBatch to process Pub/Sub messages
# -------------------------------
query = df.writeStream \
    .foreachBatch(read_from_pubsub) \
    .outputMode("append") \
    .start()

query.awaitTermination()