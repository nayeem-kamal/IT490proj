import pika
import sys
import datetime


def log(un,message1):

    # change un to urs and password too
    credentials = pika.PlainCredentials(un, un)
    parameters = pika.ConnectionParameters('192.168.194.195',
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

        message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"      "+un+': '+message1
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