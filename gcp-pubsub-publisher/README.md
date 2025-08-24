# gcp-pubsub-publisher

This project is a Java Maven application that demonstrates how to publish messages to a Google Cloud Pub/Sub topic using a JSON key for authentication.

## Project Structure

```
gcp-pubsub-publisher
├── src
│   ├── main
│   │   ├── java
│   │   │   └── com
│   │   │       └── example
│   │   │           └── publisher
│   │   │               └── PubSubPublisher.java
│   │   └── resources
│   │       └── application.properties
│   └── test
│       └── java
│           └── com
│               └── example
│                   └── publisher
│                       └── PubSubPublisherTest.java
├── pom.xml
└── README.md
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd gcp-pubsub-publisher
   ```

2. **Configure your Google Cloud credentials**:
   - Create a service account in the Google Cloud Console.
   - Download the JSON key file and place it in a secure location.
   - Update the `application.properties` file with the path to your JSON key file.

3. **Build the project**:
   ```
   mvn clean install
   ```

4. **Run the application**:
   - You can run the `PubSubPublisher` class to start publishing messages to your specified Pub/Sub topic.

## Usage Example

To publish a message, instantiate the `PubSubPublisher` class and call the `publishMessage` method with the desired message content.

## Dependencies

This project uses the Google Cloud Pub/Sub library. Ensure that your `pom.xml` file includes the necessary dependencies for Google Cloud services.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.