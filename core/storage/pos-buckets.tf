resource "google_storage_bucket" "pos-poc-json-input-bucket" {
  name          = "pos-poc-json-input-bucket"
  location      = "us"
  storage_class = "STANDARD"
}