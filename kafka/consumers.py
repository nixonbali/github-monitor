import json
import sys
from kafka.consumer import KafkaConsumer
from collab_graph import CollabGraph
import secrets
import redis


class EventsConsumer():
    """
    Kafka Events Consumer
    Any new consumers can inherit from this class
    """
    def __init__(self, topic, addr, auto_commit=False, auto_offset_reset="earliest"):
        """Initializes with Topic Name, Broker Address, and Consumer Settings"""
        self.consumer = KafkaConsumer(topic,
                                        bootstrap_servers=addr,
                                        value_deserializer=lambda m: json.loads(m.decode('ascii')),
                                        enable_auto_commit=auto_commit,
                                        auto_offset_reset=auto_offset_reset,
                                        api_version=(0,1,0))


class GraphConsumer(EventsConsumer):
    """Consumer Class for Neo4j Collaboration Graph Population"""
    def consume_and_write(self):
        """Consumes from topic and writes to graph"""
        for event in self.consumer:
            Graph = CollabGraph(secrets.NEO4J_BROKER, secrets.NEO4J_USER, secrets.NEO4J_PASSWORD)
            Graph.add_action(event)


if __name__ == "__main__":
    topic = sys.argv[1]
    ip_addr = sys.argv[2] if len(sys.argv) > 2 else secrets.BROKER1
    auto_commit = bool(sys.argv[3]) if len(sys.argv) > 3 else False
    auto_offset_reset = sys.argv[4] if len(sys.argv) > 4 else "earliest"
    Consumer = GraphConsumer(topic, ip_addr, auto_commit, auto_offset_reset)
    Consumer.consume_and_write()
