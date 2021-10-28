#!/usr/bin/env python
import pika
import sys

credentials = pika.PlainCredentials('test', 'test')
parameters = pika.ConnectionParameters('localhost',
                                        5672,
                                        'it490',
                                        credentials)
connection = pika.BlockingConnection(parameters) 
channel = connection.channel()

channel.exchange_declare(exchange='NetworkLog', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='NetworkLog', routing_key='*', body=message)
print(" [x] Sent %r" % message)
connection.close()