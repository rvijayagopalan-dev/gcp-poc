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