package com.costco.poc.publisher;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;

import com.google.api.core.ApiFuture;
import com.google.api.gax.rpc.ApiException;
import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.pubsub.v1.Publisher;
import com.google.protobuf.ByteString;
import com.google.pubsub.v1.PubsubMessage;

public class PubSubPublisher {

    private final String projectId;
    private final String topicId;
    private final Publisher publisher;

    public PubSubPublisher(String projectId, String topicId, String jsonKeyPath) throws IOException {
        this.projectId = projectId;
        this.topicId = topicId;
        String topicName = String.format("projects/%s/topics/%s", projectId, topicId);

        GoogleCredentials credentials = GoogleCredentials.fromStream(Files.newInputStream(Paths.get(jsonKeyPath)));
        com.google.api.gax.core.CredentialsProvider credentialsProvider = () -> credentials;

        this.publisher = Publisher.newBuilder(topicName)
                .setCredentialsProvider(credentialsProvider)
                .build();
    }

    public String publishMessage(String message) {
        try {
            ByteString data = ByteString.copyFromUtf8(message);
            PubsubMessage pubsubMessage = PubsubMessage.newBuilder().setData(data).build();
            ApiFuture<String> future = publisher.publish(pubsubMessage);
            System.out.println("Published message ID: " + future.get());
        } catch (ApiException | InterruptedException | ExecutionException e) {
            System.err.println("Error publishing message: " + e.getMessage());
        }

        return "Message published successfully";
    }

    public void shutdown() throws InterruptedException {
        if (publisher != null) {
            publisher.shutdown();
            publisher.awaitTermination(1, TimeUnit.MINUTES);
        }
    }

    public static void main(String[] args) {
        String projectId    = "sales-poc-465319";
        String topicId      = "external-topic";
        String jsonKeyPath  = "C:/working/credentials/gcp/sa/gcp_service_account.json";

        try {
            PubSubPublisher pubSubPublisher = new PubSubPublisher(projectId, topicId, jsonKeyPath);
            pubSubPublisher.publishMessage("Hello, Pub/Sub!");
            pubSubPublisher.shutdown();
        } catch (IOException | InterruptedException e) {
            System.err.println("Error initializing PubSubPublisher: " + e.getMessage());
        }
    }
}