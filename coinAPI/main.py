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
import cryptocompare
import datetime
import log
un="dmz"
queuename="dmz"
credentials = pika.PlainCredentials(un,un )
parameters = pika.ConnectionParameters('192.168.194.195',5672,'midterm',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange='dmz', exchange_type='direct',durable=True)

channel.queue_declare(queue='dmz',durable=True)

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


global data_cache
data_cache = {"data": {}}
global btc_historical_data_cache
btc_historical_data_cache = []
global eth_historical_data_cache
eth_historical_data_cache = []


def loadData():
    global data_cache
    global btc_historical_data_cache
    global eth_historical_data_cache

    cryptocompare.cryptocompare._set_api_key_parameter('b2e6d01a5d0c607ed2cb72d6e619734279aa87973d098da4c0029ba6c5f8c96a')
        # 'f3bfa32806d8a4514f7264b0f1effe2bdd13067f8cafd597de0d6567cd4a2393')
        # '4445849e8c74ebfe227262a54942daedfd50da463d3777b068c667e6d4495b2a')
    btc_historical_data_cache = cryptocompare.get_historical_price_day(
        'BTC', 'USD', limit=1000, exchange='CCCAGG')
    eth_historical_data_cache=cryptocompare.get_historical_price_day(
        'ETH', 'USD', limit=1000, exchange='CCCAGG')

    with open("datahistory.json", "w+") as datafile:
        datafile.write(json.dumps(btc_historical_data_cache))

    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    key =  "26c42ee6-305a-4631-a7b2-5ebccf594257"
    #"092f78e5-80ec-4b38-8d06-c6b8b9d9d852"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': key,
    }
    parameters = {'symbol': 'BTC,ETH'}

    session = Session()
    session.headers.update(headers)
    try:
            response = session.get(url, params=parameters)
            data_cache = json.loads(response.text)

            with open("data.json", "w+") as datafile:
                datafile.write(json.dumps(data_cache))

    except (ConnectionError, Timeout, TooManyRedirects) as e:
            data = json.loads(response.text)


loadData()
log.log("dmz","data loaded")
# print(data_cache)

def cache_data():
    global data_cache
    global btc_historical_data_cache
    global eth_historical_data_cache

    while True:

        
        # cryptocompare.cryptocompare._set_api_key_parameter('f3bfa32806d8a4514f7264b0f1effe2bdd13067f8cafd597de0d6567cd4a2393')
        # # '4445849e8c74ebfe227262a54942daedfd50da463d3777b068c667e6d4495b2a')
        # btc_historical_data_cache = cryptocompare.get_historical_price_day(
        # 'BTC', 'USD', limit=1000, exchange='CCCAGG')
        # eth_historical_data_cache=cryptocompare.get_historical_price_day(
        # 'ETH', 'USD', limit=1000, exchange='CCCAGG')
        # with open("datahistory.json", "w+") as datafile:
        #     datafile.write(json.dumps(btc_historical_data_cache))
        #     datafile.write(json.dumps(eth_historical_data_cache))

        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        key =  "26c42ee6-305a-4631-a7b2-5ebccf594257"
    #"092f78e5-80ec-4b38-8d06-c6b8b9d9d852"
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': key,
        }
        parameters = {'symbol': 'BTC,ETH'}

        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(url, params=parameters)
            data_cache = json.loads(response.text)

            with open("data.json", "w+") as datafile:
                datafile.write(json.dumps(data_cache))

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            data = json.loads(response.text)
            log.log("dmz","error loading data")
        sleep(60 - time() % 60)

try:
    x = threading.Thread(target=cache_data)
    x.start()
    sleep(1)
except os.error as e:
    print(False)
    log.log("dmz","thread error")

def getCurrentPrices():
    global data_cache
    ret = {"BTC": data_cache["data"]["BTC"]["quote"]["USD"]["price"],
        "ETH": data_cache["data"]["ETH"]["quote"]["USD"]["price"]}

    return ret


def getBTCDailyHistoricalWeek():
    global btc_historical_data_cache
    ret = {}
    for i in range(len(btc_historical_data_cache)-1, len(btc_historical_data_cache)-8, -1):
        ret.update({str(datetime.datetime.fromtimestamp(
            btc_historical_data_cache[i]["time"])): str(btc_historical_data_cache[i]["high"])})

    return ret


def getBTCDailyHistoricalYears():
    global btc_historical_data_cache
    ret={}
    for i in range(len(btc_historical_data_cache)-1,len(btc_historical_data_cache)-(31*37),-31):
        ret.update({""+str(datetime.datetime.fromtimestamp(btc_historical_data_cache[i]["time"])):str(btc_historical_data_cache[i]["high"])})

    
    return ret

def getBTCDailyHistoricalTwelveMonth():
    global btc_historical_data_cache
    ret={}
    for i in range(len(btc_historical_data_cache)-1,len(btc_historical_data_cache)-(31*13),-31):
        ret.update({""+str(datetime.datetime.fromtimestamp(btc_historical_data_cache[i]["time"])):str(btc_historical_data_cache[i]["high"])})

    
    return ret


def getETHDailyHistoricalWeek():
    global eth_historical_data_cache
    ret = {}
    for i in range(len(eth_historical_data_cache)-1, len(eth_historical_data_cache)-8, -1):
        ret.update({str(datetime.datetime.fromtimestamp(
            eth_historical_data_cache[i]["time"])): str(eth_historical_data_cache[i]["high"])})

    return ret


def getETHDailyHistoricalYears():
    global eth_historical_data_cache
    ret={}
    for i in range(len(eth_historical_data_cache)-1,len(eth_historical_data_cache)-(31*37),-31):
        ret.update({""+str(datetime.datetime.fromtimestamp(eth_historical_data_cache[i]["time"])):str(eth_historical_data_cache[i]["high"])})

    
    return ret

def getETHDailyHistoricalTwelveMonth():
    global eth_historical_data_cache
    ret={}
    for i in range(len(eth_historical_data_cache)-1,len(eth_historical_data_cache)-(31*13),-31):
        ret.update({""+str(datetime.datetime.fromtimestamp(eth_historical_data_cache[i]["time"])):str(eth_historical_data_cache[i]["high"])})

    
    return ret

def on_request(ch, method, props, body):
    n = json.loads(body)
    print(str(n)+" "+props.reply_to)
    if(n['function']=="getCurrentPrices"):
        response = getCurrentPrices()
    elif(n['function']=="getBTCDailyHistoricalWeek"):
        response = getBTCDailyHistoricalWeek()
    elif(n['function']=="getBTCDailyHistoricalYears"):
        response = getBTCDailyHistoricalYears()
    elif(n['function']=="getBTCDailyHistoricalTwelveMonth"):
        response = getBTCDailyHistoricalTwelveMonth()
    elif(n['function']=="getETHDailyHistoricalWeek"):
        response = getETHDailyHistoricalWeek()
    elif(n['function']=="getETHDailyHistoricalYears"):
        response = getETHDailyHistoricalYears()
    elif(n['function']=="getETHDailyHistoricalTwelveMonth"):
        response = getETHDailyHistoricalTwelveMonth()
    else:    
        response="not parsed"
        log.log("dmz","Invalid Function Request ")

    ch.basic_publish(exchange='dmz',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='dmz', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()