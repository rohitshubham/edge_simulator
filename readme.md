## Edge Computing Node Simulator Project

A simple edge node simulator that has the following components:

* An MQTT broker exposed on port 1883
* An MQTT logger that logs all the incoming traffic in a log file.
* A mini-batcher that converts incoming stream data to a custom size batches
* A Kafka Producers that pushes the code to a Kafka broker asynchronously

## Requirements

Complete environment is dockerized and does not require any other resouces except for `docker` and `docker-compose`.

## Building/Running the project

The project can be build by:

```bash
$ docker-compose build
```

The project can be started by running

```bash
$ docker-compose up
```
It starts all the services sequentially. 

The following components need to be edited in the `docker-compose` file:
* The volume mount point in service `broker_log_writer`
* The `entrypoint converter.py`'s parameters for Kafka broker and MQTT_edge_broker_name

### Few implementation details
The project currently assumes that incoming MQTT Data is being published in JSON format.

The Kafka producer serilizes the output in `msgpack` format, however, the underlying data format being sent to Kafka is still JSON and can be directly converted back.

#### Sample incoming data being handled:

* Published to MQTT:
```json

{
   "Temperature":2.626686131843816,
   "Name":"Node 1"
}
```

* 10 seconds mini-batch produced to Kafka

```json
[
   {
      "topic":"temprature/topic",
      "qos":0,
      "broker_publish_time":"2020-06-12 08:48:09",
      "broker_name":"edge_1",
      "temperature":0.8752983696943439,
      "node_name":"Node 2"
   },
   {
      "topic":"temprature/topic",
      "qos":0,
      "broker_publish_time":"2020-06-12 08:48:10",
      "broker_name":"edge_1",
      "temperature":9.135930601472666,
      "node_name":"Node 3"
   },
   {
      "topic":"temprature/topic",
      "qos":0,
      "broker_publish_time":"2020-06-12 08:48:11",
      "broker_name":"edge_1",
      "temperature":0.04712442493770341,
      "node_name":"Node 1"
   },
   {
      "topic":"temprature/topic",
      "qos":0,
      "broker_publish_time":"2020-06-12 08:48:16",
      "broker_name":"edge_1",
      "temperature":2.0889507192486745,
      "node_name":"Node 2"
   },
   {
      "topic":"temprature/topic",
      "qos":0,
      "broker_publish_time":"2020-06-12 08:48:16",
      "broker_name":"edge_1",
      "temperature":4.461685695550899,
      "node_name":"Node 1"
   },
   {
      "topic":"temprature/topic",
      "qos":0,
      "broker_publish_time":"2020-06-12 08:48:21",
      "broker_name":"edge_1",
      "temperature":6.088665260400994,
      "node_name":"Node 3"
   },
   {
      "topic":"temprature/topic",
      "qos":0,
      "broker_publish_time":"2020-06-12 08:48:21",
      "broker_name":"edge_1",
      "temperature":1.5242612282725476,
      "node_name":"Node 1"
   },
   {
      "topic":"temprature/topic",
      "qos":0,
      "broker_publish_time":"2020-06-12 08:48:23",
      "broker_name":"edge_1",
      "temperature":2.3646060449796713,
      "node_name":"Node 2"
   },
   {
      "topic":"temprature/topic",
      "qos":0,
      "broker_publish_time":"2020-06-12 08:48:26",
      "broker_name":"edge_1",
      "temperature":3.867439414535314,
      "node_name":"Node 1"
   },
   {
      "topic":"temprature/topic",
      "qos":0,
      "broker_publish_time":"2020-06-12 08:48:30",
      "broker_name":"edge_1",
      "temperature":7.952953106158276,
      "node_name":"Node 2"
   }
]
```
---
A sample code for automatic depoloyment of sensor nodes using `docker-compose` can be found at [node-red-automatic-deployer](https://github.com/rohitshubham/node-red-automatic-deployer).