resource "google_pubsub_topic" "json-input-test" {
  name = "ace-pos-json-input-topic-test"
}


resource "google_pubsub_topic" "core_topic" {
  name = var.topic_name
}

resource "google_pubsub_subscription" "core_subscription" {
  name  = var.subscription_name
  topic = google_pubsub_topic.core_topic.name
}
