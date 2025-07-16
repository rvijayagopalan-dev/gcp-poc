terraform {
  backend "gcs" {
    bucket = "terraform-state-jb-cicdproject-gpc-poc"
    prefix = "prod"
  }
}