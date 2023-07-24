from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from task.models import Task, User
import datetime
    

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


class UserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = User
        fields = '__all__' #('id', 'username',)
        #ref_name = 'ReadOnlyUsers'