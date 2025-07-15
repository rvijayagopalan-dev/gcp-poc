project_id       = "sales-pos-456319"
region           = "us-east1"
location         = "us"
environment      = "prod"

# Cloud Storage
bucket_name      = "pos-poc-json-input-bucket"
bucket_class     = "STANDARD"
bucket_force_destroy = true

# Pub/Sub
topic_name       = "pos-poc-json-input-topic"
subscription_name = "pos-poc-json-input-subscription"
