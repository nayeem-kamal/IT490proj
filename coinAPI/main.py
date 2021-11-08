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



global data_cache
data_cache = {"data": {}}
global historical_data_cache
historical_data_cache = {}


def loadData():
    global data_cache
    global historical_data_cache
    cryptocompare.cryptocompare._set_api_key_parameter(
        '4445849e8c74ebfe227262a54942daedfd50da463d3777b068c667e6d4495b2a')
    historical_data_cache = cryptocompare.get_historical_price_day(
        'BTC', 'USD', limit=1000, exchange='CCCAGG')
    with open("datahistory.json", "w+") as datafile:
        datafile.write(json.dumps(historical_data_cache))

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
    global historical_data_cache

    while True:

        cryptocompare.cryptocompare._set_api_key_parameter(
            '4445849e8c74ebfe227262a54942daedfd50da463d3777b068c667e6d4495b2a')
        historical_data_cache = cryptocompare.get_historical_price_day(
            'BTC', 'USD', limit=1000, exchange='CCCAGG')
        with open("datahistory.json", "w+") as datafile:
            datafile.write(json.dumps(historical_data_cache))

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


x = threading.Thread(target=cache_data)
x.start()
sleep(1)



def getCurrentPrices():
    global data_cache
    ret = {"BTC": data_cache["data"]["BTC"]["quote"]["USD"]["price"], "ETH":data_cache["data"]["ETH"]["quote"]["USD"]["price"]}

    return ret
def getMonthlyHistorical():
    ret={}
    return ret



un="dmz"
queuename="dmz"
credentials = pika.PlainCredentials(un,un )
parameters = pika.ConnectionParameters('192.168.194.195',5672,'it490',credentials)
connection = pika.BlockingConnection(parameters)


channel = connection.channel()

channel.queue_declare(queue=queuename,durable=True)

def on_request(ch, method, props, body):
    print(body)
    n = json.loads(body)
    print("%s" % str(n))
    if(n["function"]=="getCurrentPrices"):
        response = getCurrentPrices()
    else:
        response="not parsed"
    print(response)

    ch.basic_publish(exchange='dmz',
                     routing_key="*",
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queuename, on_message_callback=on_request)

channel_close = channel.is_closed
channel_open = channel.is_open
print("channel is_closed ", channel_close)
print("channel is_open ", channel_open)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
print("consuming")