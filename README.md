# Real-Time-Data-Pipeline
## Introduction :
In a rapidly evolving world where data is often referred to as the new currency, the ability to process, analyze, and make informed decisions based on real-time data is crucial for businesses and organizations. The Real-Time Data Pipeline project provides a practical solution for data professionals seeking to implement end-to-end data pipelines that can handle streaming data in real-time.

Whether you're a data engineer, data scientist, or developer, this project offers hands-on experience in building a data pipeline that combines various technologies and components, including PySpark, Kafka, Cassandra, MongoDB, and data visualization tools. Through this project, you'll learn how to set up a real-time data processing environment, transform and aggregate data, and gain valuable insights that can drive decision-making.

## Planning :

<img width="667" alt="image" src="https://github.com/aminelfaquiri/Real-Time-Data-Pipeline/assets/81482544/735b5bc1-9079-4820-8d18-c0d022e6e63c">

## Requirements Expression :
Before you begin with the Real-Time Data Pipeline project, ensure that you have the following requirements and dependencies in place:

- **Apache Spark (PySpark):** Make sure you have Apache Spark installed and configured. You can download Spark from the official website: [Apache Spark](https://spark.apache.org/downloads.html).

- **Kafka:** Set up a Kafka broker or cluster for data streaming. You can install Kafka using the official documentation: [Apache Kafka](https://kafka.apache.org/quickstart).

- **Cassandra:** Install and configure Cassandra for storing and retrieving data. You can get Cassandra from the official website: [Apache Cassandra] (https://cassandra.apache.org/download/).

- **MongoDB:** Set up MongoDB to store data for real-time analytics. Download MongoDB from the official website: [MongoDB](https://www.mongodb.com/try/download/community).

- **Docker (Optional):** Consider using Docker to simplify the setup of Kafka, Cassandra, and MongoDB. You can find Docker images for these services on [Docker Hub](https://hub.docker.com).

- **Java Dependencies:** Some components may require Java dependencies. Ensure that Java is installed and properly configured on your system.

- **Python Dependencies:** Install the necessary Python libraries for data processing, visualization, and interaction with Spark and databases. You can use Python package managers like `pip` to install the required packages.

## RGPD Compliance

The Real-Time Data Pipeline project respects data protection regulations, including the General Data Protection Regulation (GDPR). We ensure that sensitive and personal information, such as phone numbers, login credentials, and coordinates, are not stored, processed, or shared within the project. Here's how we achieve GDPR compliance:

- **Data Minimization:** We collect only the data necessary for the project's objectives, avoiding the inclusion of sensitive information.

- **Data Anonymization:** Personal information, such as names and addresses, is anonymized or transformed during data processing, ensuring that the data cannot be used to identify individuals.

- **Consent:** We only use data from sources for which consent has been obtained or data is publicly available and not subject to privacy restrictions.

- **Data Security:** We take measures to ensure the security of data storage and transmission. Access to data is restricted to authorized personnel only.

- **Data Retention:** Data is retained for the minimum time necessary to achieve the project's objectives. Data that is no longer needed is deleted or anonymized.

- **Right to Erasure:** Users have the right to request the removal of their data from the project. Data will be promptly erased upon such requests.

- **Documentation:** We maintain a detailed record of data processing activities, including the types of data collected, the purposes of processing, and security measures in place.

- **Data Cleansing:** Regular procedures for data cleansing and removal of personal data are implemented to ensure ongoing compliance.

By following these GDPR-compliant practices, we prioritize data protection and privacy while working with real-time data in our project.

## Creating a Kafka Topic

Before you can start streaming data with Kafka in your real-time data pipeline, you need to create a Kafka topic. Follow these steps to set up the "messages" topic:

**1. Start ZooKeeper:**
   - Ensure ZooKeeper is installed and configured on your system.
   - Open a terminal window and navigate to the Kafka directory.

**2. Start Kafka Server:**
   - In the same terminal, start the Kafka server by running the following command:
     ```shell
     bin\windows\kafka-server-start.bat config\server.properties
     ```
     Adjust the command based on your operating system if necessary.

**3. Create the "messages" Topic:**
   - To create the "messages" topic, use the following command:
     ```shell
     bin\windows\kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic messages
     ```
     You can adjust the replication factor and the number of partitions based on your requirements.

**4. Verify the Topic Creation:**
   - To verify that the "messages" topic has been successfully created, run:
     ```shell
     bin\windows\kafka-topics.bat --list --zookeeper localhost:2181
     ```
     You should see "messages" listed as one of the topics.

With the "messages" topic in place, you're ready to start streaming data into your real-time data pipeline. Make sure that you have Kafka up and running before proceeding with your project.

## Creating a Producer Script :

To populate your real-time data pipeline with user data, you will need a producer script that generates user data and sends it to the Kafka topic. Follow these steps to create the producer script:

**1. Generate User Data from Random User API:**
   - Start by fetching user data from the Random User API. You can use Python libraries like `requests` to make API requests.
   - Extract relevant attributes from the API response. Customize the attributes you want to send to the Kafka topic.

**2. Set Up a Kafka Producer:**
   - Use the Kafka Python library (e.g., `confluent-kafka-python`) to set up a Kafka producer.
   - Configure the producer to connect to your Kafka broker and target the "messages" topic.

**3. Send User Data to Kafka:**
   - For each user data entry obtained from the Random User API, send the data as a message to the "messages" topic using the Kafka producer.

Here's a simplified Python code snippet as an example of creating a producer script:

```python
from confluent_kafka import Producer
import requests
import json

# Configure Kafka producer settings
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Fetch user data from the Random User API
api_url = 'https://randomuser.me/api/?results=1'
response = requests.get(api_url)
user_data = json.loads(response.text)

# Extract and customize attributes
customized_data = {
    "gender": user_data['results'][0]['gender'],
    "name": user_data['results'][0]['name']['first'],
    "custom_attribute": "your_custom_value_here"
}

# Send data to Kafka topic
producer.produce('messages', key='user_key', value=json.dumps(customized_data))

```
<img width="952" alt="image" src="https://github.com/aminelfaquiri/Real-Time-Data-Pipeline/assets/81482544/4be97ada-ce98-477f-ba54-55a94bc83a20">

## Creating a Consumer Script :

To consume and process data from the Kafka topic within your real-time data pipeline, you'll need a consumer script. This script reads messages from the "messages" topic and performs the desired processing. Follow these steps to create the consumer script:

**1. Set Up a Kafka Consumer:**
   - Use the Kafka Python library (e.g., `confluent-kafka-python`) to set up a Kafka consumer.
   - Configure the consumer to connect to your Kafka broker and subscribe to the "messages" topic.

**2. Consume Data from Kafka:**
   - Continuously poll for messages from the Kafka topic and process each message as it arrives.
     
**3. Process the Data:**
   - Define the processing logic for the data you receive from Kafka. This can include transformations, aggregations, or other operations specific to your project's requirements.

**4. Store Processed Data:**
   - After processing, store the data in the appropriate data storage systems, such as Cassandra or MongoDB.
   - 
      <img width="925" alt="image" src="https://github.com/aminelfaquiri/Real-Time-Data-Pipeline/assets/81482544/f9f6214b-09fd-4c34-8705-5f726738ff33">
      <img width="948" alt="image" src="https://github.com/aminelfaquiri/Real-Time-Data-Pipeline/assets/81482544/9e285c3d-b063-494c-8ba1-59f1e36b6403">

Here's a simplified Python code snippet as an example of creating a consumer script:

```python
from confluent_kafka import Consumer, KafkaError

# Configure Kafka consumer settings
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'  # Set the offset to the beginning of the topic
})

# Subscribe to the "messages" topic
consumer.subscribe(['messages'])

# Continuously poll for messages
while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # Reached the end of the topic
            pass
        else:
            print(f"Error: {msg.error()}")
    else:
        # Process the received message
        data = json.loads(msg.value())
        
        # Implement your custom processing logic here
        # For example, you can perform aggregations or data transformations
```
## Creating Data Visualizations with Dash

This project incorporates real-time data visualizations to provide valuable insights into your data stream. Here are the key visualizations created using Dash, Plotly, and Python:

### 1. Number of Users by Nationality :

The "Number of Users by Nationality" visualization is a bar chart that illustrates the distribution of users by their nationality. Each nationality is represented on the x-axis, and the y-axis displays the number of users from each nationality. This chart provides a quick overview of the most prevalent nationalities in your data stream.

### 2. Average Age of Users :

The "Average Age of Users" visualization is a line chart that tracks the average age of users over time. The x-axis represents time, while the y-axis shows the average age. As new data arrives in real-time, this chart updates to reflect changes in the age distribution of users within your dataset.

### 3. Most Common Email Domains :

The "Most Common Email Domains" visualization is a bar chart that highlights the email domains most frequently used by users in your dataset. Email domains are listed on the x-axis, and the y-axis displays the count of users with email addresses from each domain. This chart helps identify the popular email service providers among your users.

These interactive visualizations empower you to gain actionable insights from your real-time data stream. You can monitor and analyze data as it flows through your pipeline, enabling data-driven decision-making and trend identification
![newplot (1)](https://github.com/aminelfaquiri/Real-Time-Data-Pipeline/assets/81482544/148f6e27-5451-4830-bd59-284f0c8ca0f4)
![newplot (2)](https://github.com/aminelfaquiri/Real-Time-Data-Pipeline/assets/81482544/1ca4b70a-3112-488b-8b0d-3efbb2979e28)
![newplot (3)](https://github.com/aminelfaquiri/Real-Time-Data-Pipeline/assets/81482544/01f162cf-5185-493e-ab3d-843d037420b4)

## Conclusion :
In an era where data reigns supreme, the ability to process and analyze information in real-time is a game-changer. This project serves as a practical guide for data professionals, offering hands-on experience in building robust real-time data pipelines. By setting up key dependencies, streaming data, and storing it in databases, you've learned how to harness the power of data. Additionally, real-time visualizations provide dynamic insights, while considerations like GDPR compliance ensure responsible data management. We invite you to explore and adapt this project, making it a valuable resource for those seeking to leverage real-time data for data-driven decision-making.
