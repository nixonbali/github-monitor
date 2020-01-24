import unittest
import sys
sys.path.insert(1, 'kafka')
from kafka_producer import EventsProducer
import secrets

class TestStream(unittest.TestCase):
    def test_production(self):
        Producer.move_to_dest("testing/test.json", "")


if __name__ == "__main__":
    Producer = EventsProducer(secrets.BROKER1, "test")
    unittest.main()
