# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from kafka import KafkaProducer, KafkaConsumer
import json
from configs import kafka
from configs import admin


if admin.use_kafka is True:
    producer = KafkaProducer(bootstrap_servers=kafka.bootstrap_servers)

def insert_message_to_kafka(msg):
    producer.send(topic=kafka.kafka_topic,value=json.dumps(msg).encode())


kafka_offset_reset = 'earliest' #latest,earliest,none 首次拉取kafka订阅的模式

def get_message_from_kafka():
    consumer=KafkaConsumer(kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=kafka.client_group_id,auto_offset_reset=kafka_offset_reset,client_id='get_message_from_kafka')
    return consumer

def get_message_from_kafka_independent_listener():
    consumer=KafkaConsumer(kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=admin.independent_listener_kafka_client_group_id,auto_offset_reset=kafka_offset_reset,client_id='get_message_from_kafka_independent_listener')
    return consumer

if __name__ == "__main__":
    insert_message_to_kafka(msg={'msg': 'test'})