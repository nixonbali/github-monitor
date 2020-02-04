import json
import sys
from kafka.consumer import KafkaConsumer
from collab_graph import CollabGraph
import secrets
import redis


class EventsConsumer():
    def __init__(self, topic, addr, auto_commit=False, auto_offset_reset="earliest"):
        self.consumer = KafkaConsumer(topic,
                                        bootstrap_servers=addr,
                                        value_deserializer=lambda m: json.loads(m.decode('ascii')),
                                        enable_auto_commit=auto_commit,
                                        auto_offset_reset=auto_offset_reset,
                                        api_version=(0,1,0))

# class PREventsConsumer(EventsConsumer):
#     def consume_and_write(self):
#         for event in self.consumer:
#             print("Unimplemented")

class PRClosedConsumer(EventsConsumer):
    def consume_and_write(self):
        client = redis.StrictRedis(host="localhost", port=6379)
        for pr_id in self.consumer:
            print(pr_id.value)
            pr_len = client.llen(pr_id.value)
            full_pr = client.lrange(pr_id.value, 0, pr_len)
            print(full_pr)


class GraphConsumer(EventsConsumer):
    def consume_and_write(self):
        for event in self.consumer:
            Graph = CollabGraph(secrets.NEO4J_BROKER, secrets.NEO4J_USER, secrets.NEO4J_PASSWORD)
            Graph.add_action(event)

consumers = {
    "collab":GraphConsumer,
    #"pr-events3":PREventsConsumer,
    "pr-closed-ids":PRClosedConsumer
}

def new_consumer(topic, ip_addr, auto_commit, auto_offset_reset):
    if topic in consumers:
        return consumers[topic](topic, ip_addr, auto_commit, auto_offset_reset)
    else:
        print("Invalid topic. Must be from (collab, pr-events, pr-closed)")
        sys.exit(0)


if __name__ == "__main__":
    topic = sys.argv[1]
    ip_addr = sys.argv[2] if len(sys.argv) > 2 else secrets.BROKER1
    auto_commit = bool(sys.argv[3]) if len(sys.argv) > 3 else False
    auto_offset_reset = sys.argv[4] if len(sys.argv) > 4 else "earliest"
    Consumer = new_consumer(topic, ip_addr, auto_commit, auto_offset_reset)
    Consumer.consume_and_write()
