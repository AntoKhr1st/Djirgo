import pika
import json
from django.conf import settings


class RabbitMQConsumer:
    def __init__(self):
        self.credentials = pika.PlainCredentials(
            settings.RABBITMQ_SETTINGS['USERNAME'], settings.RABBITMQ_SETTINGS['PASSWORD'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_SETTINGS['HOST'],
                                      port=settings.RABBITMQ_SETTINGS['PORT'],
                                      credentials=self.credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='my_queue', durable=True)

    def consume(self):
        self.channel.basic_consume(queue='my_queue', on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        message = json.loads(body.decode('utf-8'))
        print(f"New Task: {message}")

    def start_rabbitmq_consumer():
        credentials = pika.PlainCredentials(
            settings.RABBITMQ_SETTINGS['USERNAME'], settings.RABBITMQ_SETTINGS['PASSWORD'])
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_SETTINGS['HOST'],
                                    port=settings.RABBITMQ_SETTINGS['PORT'],
                                    credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='my_queue', durable=True)
        channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()


consumer = RabbitMQConsumer()


consumer.consume()