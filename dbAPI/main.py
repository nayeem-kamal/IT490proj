#!/usr/bin/env python
import pika
import logging
import json
import threading
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from time import time, sleep

from sqlpython import DBTransactor
un="mysql"
queuename="mysql"
credentials = pika.PlainCredentials(un,un )
parameters = pika.ConnectionParameters('192.168.194.195',5672,'midterm',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange='mysql', exchange_type='direct',durable=True)


channel.queue_declare(queue='mysql',durable=True)
global db
db = DBTransactor()

def register(firstName,lastName,email,password):
    global db
    ret = db.register(firstName,lastName,email,password)
    return ret
def login(email,pw):
    global db
    ret = db.login(email,pw)
    return ret
def get_accounts(email):
    global db
    ret = db.get_accounts(email)
    return ret
def trade(s,d,a):
    global db
    ret = db.trade(s,d,a)
    return ret
def history(un):
    global db
    ret = db.tradeHistory(un)
    return ret

def on_request(ch, method, props, body):
    # print(body)
    n = json.loads(body)
    print(str(n)+" "+props.reply_to)
    print(n)

    if(n['function']=="register"):
        response = register(n["firstName"],n["lastName"],n["email"],n["password"])
    elif(n['function']=="login"):
        response = login(n["email"],str(n["password"]))
    elif(n['function']=="get_accounts"):
        response = get_accounts(str(n["email"]))
    elif(n['function']=="trade"):
        response =trade(n["src"],n["dst"],n["amt"])
    elif(n['function']=="history"):
        response = history(n["email"])
    else:    
        response="not parsed"

    print(" %r" % response)
    ch.basic_publish(exchange='mysql',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='mysql', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()