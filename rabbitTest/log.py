#!/usr/bin/env python
import pika
import sys


def log(message1):

    # change un to urs and password too
    un = 'logreader'
    credentials = pika.PlainCredentials('logreader', 'logreader')
    parameters = pika.ConnectionParameters('localhost',
                                           5672,
                                           'it490',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    if(connection.is_open):
        channel = connection.channel()
    else:
        return False
    try:
        

        channel.exchange_declare(exchange='NetworkLog', exchange_type='fanout')

        message = un+': '+message1
        channel.basic_publish(exchange='NetworkLog',
                              routing_key='*', body=message)
        print(" [x] Sent %r" % message)
        if(connection.is_open):
            connection.close()
        return True
    except:
        if(connection.is_open):
            connection.close()
        return False


