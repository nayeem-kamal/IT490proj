import log
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

un="dmz"
queuename="dmz"
credentials = pika.PlainCredentials(un,un )
parameters = pika.ConnectionParameters('192.168.194.195',5672,'it490',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_purge("dmz")
#channel.queue_declare(queue='dmz',durable=True)


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

    cryptocompare.cryptocompare._set_api_key_parameter(
        '4445849e8c74ebfe227262a54942daedfd50da463d3777b068c667e6d4495b2a')
    btc_historical_data_cache = cryptocompare.get_historical_price_day(
        'BTC', 'USD', limit=1000, exchange='CCCAGG')
    eth_historical_data_cache=cryptocompare.get_historical_price_day(
        'ETH', 'USD', limit=1000, exchange='CCCAGG')

    with open("datahistory.json", "w+") as datafile:
        datafile.write(json.dumps(btc_historical_data_cache))

    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    key = "092f78e5-80ec-4b38-8d06-c6b8b9d9d852"
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


def cache_data():
    global data_cache
    global btc_historical_data_cache
    global eth_historical_data_cache

    while True:

        
        cryptocompare.cryptocompare._set_api_key_parameter(
        '4445849e8c74ebfe227262a54942daedfd50da463d3777b068c667e6d4495b2a')
        btc_historical_data_cache = cryptocompare.get_historical_price_day(
        'BTC', 'USD', limit=1000, exchange='CCCAGG')
        eth_historical_data_cache=cryptocompare.get_historical_price_day(
        'ETH', 'USD', limit=1000, exchange='CCCAGG')
        with open("datahistory.json", "w+") as datafile:
            datafile.write(json.dumps(btc_historical_data_cache))
            datafile.write(json.dumps(eth_historical_data_cache))

        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        key = "092f78e5-80ec-4b38-8d06-c6b8b9d9d852"
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
            # logger.log("dmz",json.dumps(data))
        sleep(60 - time() % 60)

try:
    x = threading.Thread(target=cache_data)
    x.start()
    sleep(1)
except os.error as e:
    log.log("dmz","{}".format(e))

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
    # print(body)
    n = json.loads(body)
   
    print("%s" % str(n))
    if(n["function"]=="getCurrentPrices"):
        response = getCurrentPrices()
    elif(n["function"]=="getBTCDailyHistoricalWeek"):
        response = getBTCDailyHistoricalWeek()
    elif(n["function"]=="getBTCDailyHistoricalYears"):
        response = getBTCDailyHistoricalYears()
    elif(n["function"]=="getBTCDailyHistoricalTwelveMonth"):
        response = getBTCDailyHistoricalTwelveMonth()
    elif(n["function"]=="getETHDailyHistoricalWeek"):
        response = getETHDailyHistoricalWeek()
    elif(n["function"]=="getETHDailyHistoricalYears"):
        response = getETHDailyHistoricalYears()
    elif(n["function"]=="getETHDailyHistoricalTwelveMonth"):
        response = getETHDailyHistoricalTwelveMonth()
    else:    
        response="not parsed"

    print(" %r" % response)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=json.dumps(response))
    #ch.basic_ack(delivery_tag=method.delivery_tag)
try:
    channel.basic_consume(queue='dmz', on_message_callback=on_request)

    log.log("dmz"," [x] Awaiting RPC requests")
    channel.start_consuming()
except pika.exceptions.AMQPError as e:
    log.log("dmz","{}".format(e))