#!/usr/bin/env python
import pika
import logging
import json
import threading
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint 
import os
from time import time, sleep
global data_cache
data_cache={}

def cache_data():
    global data_cache
    while True:
        # thing to run

        pp = pprint.PrettyPrinter(indent=4)

        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        print(url)
        key = "092f78e5-80ec-4b38-8d06-c6b8b9d9d852"
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': key,
        }
        parameters = {
        'id':'1,2,3,4'

        }

        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(url, params=parameters)
            data_cache = json.loads(response.text)
            pp.pprint(data_cache)

            with open("data.json","w+") as datafile:
                datafile.write(json.dumps(data))
            

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            data = json.loads(response.text)
            pp.pprint(data)
        sleep(60 - time() % 60)


x = threading.Thread(target=cache_data)
x.start()


un='logreader'
credentials = pika.PlainCredentials(un,un )
parameters = pika.ConnectionParameters('192.168.194.195',
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


def log(body):
    with open("network.log", 'a') as file1:
        file1.write("\n%r" % body)


def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    log(body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
