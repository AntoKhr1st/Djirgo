from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from task.models import Task, User
import datetime
import pika
import json
from django.conf import settings

    

class TaskSerializer(serializers.ModelSerializer):
    perform_time = serializers.SerializerMethodField()
    owner = SlugRelatedField(slug_field='username', read_only=True)
    performer = SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        model = Task
        fields = ('id','task_status', 'owner', 'text', 'pub_date','performer', 'perform_time',)
        #fields = '__all__'

    def get_perform_time(self, obj):
        perform_time = obj.update_date - obj.pub_date
        total_seconds = perform_time.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        formatted_age = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        return formatted_age
    

    # def create(self, validated_data):
    #     task = Task.objects.create(**validated_data)
    #     credentials = pika.PlainCredentials(
    #         settings.RABBITMQ_SETTINGS['USERNAME'], settings.RABBITMQ_SETTINGS['PASSWORD'])
    #     rabbitmq_connection = pika.BlockingConnection(
    #         pika.ConnectionParameters(host=settings.RABBITMQ_SETTINGS['HOST'],
    #                                   port=settings.RABBITMQ_SETTINGS['PORT'],
    #                                   credentials=credentials))
    #     rabbitmq_channel = rabbitmq_connection.channel()

    #     rabbitmq_channel.queue_declare(queue='my_queue', durable=True)
    #     message = {
    #         'task_id': task.id,
    #         'task_status': task.task_status,
    #         'owner': task.owner.username,
    #         # Add any additional information you want to include in the message
    #     }
    #     rabbitmq_channel.basic_publish(
    #         exchange='',
    #         routing_key='my_queue',
    #         body=json.dumps(message),
    #         properties=pika.BasicProperties(
    #             delivery_mode=2,  # Make message persistent
    #         )
    #     )
    #     rabbitmq_connection.close()

    #     return task




class UserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = User
        fields = '__all__' #('id', 'username',)
        #ref_name = 'ReadOnlyUsers'