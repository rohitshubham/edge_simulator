import paho.mqtt.client as mqtt
import json
import sys
from datetime import datetime, timedelta
import time 
from cloud_publisher import KafkaPublisher
import logging


logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger("mini-batcher-application")
rootLogger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.DEBUG)
rootLogger.addHandler(consoleHandler)

args = sys.argv

mqtt_host = args[1] 
mqtt_port = int(args[2])
broker_name = args[3]
batch_pool_frequency = int(args[4])
kafka_broker = args[5].split(',')

class MiniBatch:
    def __init__(self):
        super().__init__()
        self._queue = []
        self.time_start = datetime.now()
        self.time_end = datetime.now()

    def formatter(self, msg, payload):
        return {
                "topic": msg.topic,
                "qos": msg.qos,
                "broker_publish_time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "broker_name" : broker_name,
                "temperature" : payload["Temperature"],
                "node_name" : payload["Name"]
            }

    def mini_cluster(self, msg, kafka_publisher):
        try:
            payload = json.loads(msg.payload)
            data_dict = self.formatter(msg, payload)
            self._queue.append(data_dict)

            if (self.time_end - self.time_start).seconds > batch_pool_frequency:
                kafka_publisher.produce(topic = f"sensors.temperature.{broker_name}", value = self._queue)
                rootLogger.info(f"Successfully published mini-batch of {len(self._queue)} values to Kafka broker")
                self._queue = []
                self.time_start = datetime.now()

            self.time_end = datetime.now()            
        except Exception as e:
            # Potential alert mechanism to put here
            print(e)

def on_connect(client, userdata, flags, rc):
    print("Connected to broker")
    client.subscribe("#")

def on_disconnect(client, userdata, rc):
    print("Disconnect, reason: " + str(client))


def on_message(mosq, obj, msg):
    batch.mini_cluster(msg, kafka_publisher)

batch = MiniBatch()
kafka_publisher = KafkaPublisher(kafka_broker) 
client = mqtt.Client("mini-batch-converter")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(mqtt_host, mqtt_port, 60)

client.loop_forever()

