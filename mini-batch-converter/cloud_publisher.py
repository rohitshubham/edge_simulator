from kafka import KafkaProducer
from kafka.errors import KafkaError
from threading import Thread
import msgpack


def on_send_success(record_metadata):
    print("Published to Kafka")
def on_send_error(excp):
    print('I am an errback', exc_info=excp)

class KafkaProducer:
    def __init__(self, config):
        super().__init__()
        self._producer = KafkaProducer(bootstrap_servers = config, value_serializer=msgpack.dumps)


    # Produce Async and handle exception
    def produce(self, topic, value):
        self._producer.send(topic, value).add_callback(on_send_success).add_errback(on_send_error)
        