resource "google_storage_bucket" "pos-poc-json-input-bucket-2" {
  name          = "pos-poc-json-input-bucket-2"
  location      = "us-east1"
  storage_class = "STANDARD"
}