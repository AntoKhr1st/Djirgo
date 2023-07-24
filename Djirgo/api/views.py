from rest_framework import viewsets

from task.models import Task, User
from .serializers import TaskSerializer, UserSerializer
from .permissions import OwnerOrReadOnly

import pika
import json
from django.conf import settings




class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [OwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        send_to_rabbitmq(serializer.data)

    def perform_update(self, serializer):
        serializer.save(performer=self.request.user)
        send_to_rabbitmq(serializer.data)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def send_to_rabbitmq(data):
    credentials = pika.PlainCredentials(
        settings.RABBITMQ_SETTINGS['USERNAME'], settings.RABBITMQ_SETTINGS['PASSWORD'])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_SETTINGS['HOST'],
                                  port=settings.RABBITMQ_SETTINGS['PORT'],
                                  credentials=credentials))

    channel = connection.channel()
    channel.queue_declare(queue='my_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='my_queue',
        body=json.dumps(data),
        properties=pika.BasicProperties(delivery_mode=2) 
    )

    connection.close()
