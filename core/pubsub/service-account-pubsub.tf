resource "google_service_account" "external_publisher" {
  account_id   = "external-publisher"
  display_name = "Service Account for external Pub/Sub publisher"
  project      = var.project_id
}

resource "google_project_iam_member" "pubsub_publisher" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.external_publisher.email}"
}