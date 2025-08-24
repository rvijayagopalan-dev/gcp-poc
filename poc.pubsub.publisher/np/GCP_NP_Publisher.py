import json
import os
from google.cloud import pubsub_v1

# Path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/working/credentials/gcp/np/p-600-np-whse-sales.json"

# Replace with your project ID and topic name
project_id = "p-600-np-whse-sales"
topic_id = "external-json-topic"

# Create a Publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# JSON message to publish
message_dict = {
    "id": "00051",
    "description": "Sale 51 from International Sales on July 28",
    "value": "00051-999"
}

# Convert dict to JSON string and encode to bytes
message_json = json.dumps(message_dict)
message_bytes = message_json.encode("utf-8")

# Publish the message
future = publisher.publish(topic_path, message_bytes)
print(f"Published message ID: {future.result()}")