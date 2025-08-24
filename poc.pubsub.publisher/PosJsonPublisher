import json
import os
from google.cloud import pubsub_v1

# Path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/working/credentials/gcp/sa/gcp_service_account.json"

# Replace with your project ID and topic name
project_id = "sales-poc-465319"
topic_id = "external-topic"

# Create a Publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

poc_json_file_path = 'c:/working/gcp/gcp-poc/data/gcp/pos/poslog_00001.json'
# Open and read the JSON file
with open(poc_json_file_path, 'r') as file:
    data = json.load(file)


# JSON message to publish
"""message_dict = {
    "id": "00051",
    "description": "Sale 51 from International Sales on July 28",
    "value": "00051-999"
}"""

message_dict = data

# Convert dict to JSON string and encode to bytes
message_json = json.dumps(message_dict)
message_bytes = message_json.encode("utf-8")

# Publish the message
future = publisher.publish(topic_path, message_bytes)
print(f"Published message ID: {future.result()}")