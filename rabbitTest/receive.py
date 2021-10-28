#!/usr/bin/env python
import pika
credentials = pika.PlainCredentials('test', 'test')
parameters = pika.ConnectionParameters('localhost',
                                        5672,
                                        'it490',
                                        credentials)
connection = pika.BlockingConnection(parameters) 
channel = connection.channel()

channel.exchange_declare(exchange='NetworkLog', exchange_type='fanout')

result = channel.queue_declare(queue='NetworkLog', exclusive=False)
queue_name = result.method.queue

channel.queue_bind(exchange='NetworkLog', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()