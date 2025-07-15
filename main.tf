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
  name          = "pos-poc-json-input-bucket"
  location      = "US"
  storage_class = "STANDARD"
}