#!/usr/bin/env python
import pika
import time

time.sleep(20)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='it490-master_messaging_1'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()