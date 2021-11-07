import pika
import uuid
import datetime
from time import time,sleep 
import json
class RpcClient(object):

    def __init__(self,inqueue):
        un="apache"
        innqueue=inqueue
        credentials = pika.PlainCredentials(un,un )
        parameters = pika.ConnectionParameters('192.168.194.195',
                                       5672,
                                       'it490',
                                       credentials)
        self.connection = pika.BlockingConnection(parameters)

        self.channel = self.connection.channel()
        channel_close = self.channel.is_closed
        channel_open = self.channel.is_open
        print("channel is_closed ", channel_close)
        print("channel is_open ", channel_open)
        result = self.channel.queue_declare(queue=innqueue, exclusive=False,durable=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        self.response=body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='dmz',
            routing_key='*',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            
            self.connection.process_data_events()
        return self.response


fibonacci_rpc = RpcClient("dmz")

print(" [x] Requesting current prices")
response = fibonacci_rpc.call(json.dumps({"function":"getCurrentPrices"}))
print(" [.] Got %r" % response)