import json
import sys
from kafka.consumer import KafkaConsumer
import secrets
from collab_graph import CollabGraph

class EventsConsumer():
    def __init__(self, addr, topic="collab", auto_commit=False):
        self.consumer = KafkaConsumer(topic,
                                        bootstrap_servers=addr,
                                        value_deserializer=lambda m: json.loads(m.decode('ascii')),
                                        enable_auto_commit=auto_commit,
                                        auto_offset_reset="earliest")

    def build_graph(self):
        for event in self.consumer:
            Graph = CollabGraph(secrets.NEO4J_BROKER, secrets.NEO4J_USER, secrets.NEO4J_PASSWORD)
            Graph.add_action(event)

if __name__ == "__main__":
    ip_addr = sys.argv[1] if len(sys.argv) > 1 else secrets.BROKER1
    topic = sys.argv[2] if len(sys.argv) > 2 else "collab"
    auto_commit = bool(sys.argv[3]) if len(sys.argv) > 3 else False
    Consumer = EventsConsumer(ip_addr, topic, auto_commit)
    Consumer.build_graph()
