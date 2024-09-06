import json
import os
import time
import pika

from dotenv import load_dotenv


class Rabbit:
    _exchange = None
    _route = None
    _queue_name = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.channel.close()
        self._rabbit_connection.close()

    def __init__(self):
        load_dotenv()
        host = os.environ.get('RABBITMQ_DEFAULT_HOST')
        port = os.environ.get('RABBITMQ_DEFAULT_PORT')
        username = os.environ.get('RABBITMQ_DEFAULT_USER')
        password = os.environ.get('RABBITMQ_DEFAULT_PASS')
        credentials = pika.PlainCredentials(username, password)
        self.connection_params = pika.ConnectionParameters(host=host, port=int(port), credentials=credentials)
        self.refresh_connection()
        self.channel.queue_declare(queue=self._queue_name, durable=True)
        self.channel.exchange_declare(exchange=self._exchange, exchange_type='direct')
        self.channel.queue_bind(exchange=self._exchange, routing_key=self._route, queue=self._queue_name)

    def refresh_connection(self):
        try_count = 0
        while True:
            try_count += 1
            try:
                self._rabbit_connection = pika.BlockingConnection(parameters=self.connection_params)
                self.channel = self._rabbit_connection.channel()
                break
            except Exception as e:
                if try_count > 1000:
                    raise e
                time.sleep(5)

    def push(self, data):
        new_data = data
        if isinstance(data, list) or isinstance(data, dict):
            new_data = json.dumps(data, ensure_ascii=False)
        try_count = 0
        while True:
            try_count += 1
            try:
                self.channel.basic_publish(exchange=self._exchange, properties=pika.BasicProperties(delivery_mode=2),
                                           routing_key=self._route, body=new_data)
                break
            except Exception as e:
                if try_count > 100:
                    raise e
                self.refresh_connection()

    def get_count_of_message_in_queue(self):
        status = self.channel.queue_declare(queue=self._queue_name, durable=True)
        count = status.method.message_count
        return count

    def basic_get(self):
        method, properties, body = self.channel.basic_get(queue=self._queue_name)
        if method is None or properties is None:
            return None, None, None
        return method, properties, body

    def basic_ack(self, delivery_tag):
        # method.delivery
        self.channel.basic_ack(delivery_tag=delivery_tag)
