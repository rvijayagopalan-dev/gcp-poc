terraform {
  backend "gcs" {
    bucket = "terraform-state-jb-cicdproject-gpc-poc"
    prefix = "prod"
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

resource "google_storage_bucket" "pos-poc-json-input-bucket" {
  name          = "pos-poc-json-input-bucket-2"
  location      = "us-east1"
  storage_class = "STANDARD"
}