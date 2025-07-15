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

# Cloud SQL
db_instance_name = "core-db-instance"
db_tier          = "db-f1-micro"
db_version       = "POSTGRES_15"
db_user          = "admin"
db_password      = "securepassword123"
db_name          = "coredb"
