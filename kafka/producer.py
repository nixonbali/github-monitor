#!/usr/bin/env python3
import sys
sys.path.insert(1,'../ingestion')
from api_ingestor import Destination, EventsIngestor
from helpers import date_reader
from kafka.client import KafkaClient
from kafka.producer import KafkaProducer
import json
import secrets


class EventsProducer(Destination):
    """
    Kafka Producer
    Sets Destination of API Ingestion to Kafka Cluster
    """
    def __init__(self, addr, topic="git-events"):
        """Initializes with Broker Address and Topic Name"""
        self.producer = KafkaProducer(bootstrap_servers=addr,
                                        value_serializer=lambda m: json.dumps(m).encode('ascii'),
                                        api_version=(0,1,0))
        self.topic = topic

    ######## PRODUCE TO TOPIC
    def move_to_dest(self, filename, datestring):
        """Sends Local File to Kafka Topic"""
        with open(filename, 'r') as file:
            for line in file:
                d = json.loads(line)
                self.producer.send(self.topic, d).get()

if __name__ == "__main__":
    ## Parse Arguments
    ip_addr = sys.argv[1] if (len(sys.argv) > 1 and sys.argv[1] != "broker1") else secrets.BROKER1
    start_date, end_date = date_reader(sys.argv[2:])
    ## run with nohup to print to nohup.out
    print("IP Address: {}\nTopic: git-events\nStart Date: {}\nEnd Date: {}".format(ip_addr, start_date, end_date))
    ## Define destination and ingestion objects
    Producer = EventsProducer(ip_addr)
    Ingestor = EventsIngestor(start_date, end_date, Producer)
    ### RUN
    try:
        Ingestor.hourly_events()
    except KeyboardInterrupt:
        None
    sys.exit(0)
