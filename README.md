# GitHub Events Monitor

Using the [GH Archive](https://www.gharchive.org/) dataset of events on the public GitHub timeline, the goal of this project is to build real-time ingestion and processing application with Kafka to monitor topics, contributions, repositories, and collaborations of interest.

## Ingestion
The [GH Archive](https://www.gharchive.org/) is available for download via an API, however to mitigate the risk of the streaming directly from the API during my Kafka ingestion, I'm also storing all of this data in an S3 bucket. This process is done with `api_to_s3.py` which takes dates as command line date arguments. This is so that it can be run across different subsets of dates from the shell on multiple EC2 instances in parallel to speed up ingestion. The only requirements are that the `awscli` is configured with your credentials on each instance and python3 is installed with the necessary packages (e.g. `boto3`). Additionally, a file `logs/gh-events.log` in your directory and an S3 bucket already built and named `git-events` will allow the script to be run without modifications.

## Kafka Cluster

- Set up w/ Peg **EXPAND ON THIS**

### Creating Topics
`kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor <rep-factor> --partitions <num-partitions> --topic <topic-name>`
### Confirming creation on other brokers
`kafka-topics.sh --describe --zookeeper localhost:2181 --topic <topic-name>`
### Producing Message from Node
`kafka-console-producer.sh --broker-list localhost:9092 --topic topic <topic-name>`
- Enter Message in console
### Viewing Consumed Messages from Node
`kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic <topic-name>`
- Note optional `--from-beginning` tag

### Producers + Kafka-Python
`pip3 install kafka-python`

### Producing from API to git-events topic
`./kafka_producer.py <ip-address>:9092 <start-year> <start-month> <start-day> <end-year> <end-month> <end-day>`
