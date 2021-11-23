import pika
import uuid

class RpcClient(object):

    def __init__(self,q):
        un=q
        self.queuename=q
        credentials = pika.PlainCredentials(un,un )
        parameters = pika.ConnectionParameters('192.168.194.195',5672,'midterm',credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True,auto_delete=True)
        self.callback_queue = result.method.queue
        print(self.callback_queue)
        self.channel.queue_bind(self.callback_queue,self.queuename)

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange=self.queuename,
            routing_key='*',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


# fibonacci_rpc = RpcClient()

# print(" [x] Requesting fib(30)")
# response = fibonacci_rpc.call(30)
# print(" [.] Got %r" % response)