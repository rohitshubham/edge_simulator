import paho.mqtt.client as mqtt
import json
import sys

args = sys.argv

host = "localhost"#args[1] 
port = 1883 #int(args[2])

def on_connect(client, userdata, flags, rc):
    print("Connected to broker")
    client.subscribe("#")

def on_disconnect(client, userdata, rc):
    print("Disconnect, reason: " + str(rc))
    print("Disconnect, reason: " + str(client))


def on_message(mosq, obj, msg):
    print("Recevied message")
    print(str(msg.payload))

def logger(msg):
    log_string = f"Topic: {}"

client = mqtt.Client("testclient")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(host, port, 60)

client.loop_forever()

