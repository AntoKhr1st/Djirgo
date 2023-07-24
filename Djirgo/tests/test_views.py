from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from task.models import Task, User
from api.serializers import TaskSerializer, UserSerializer
from api.views import TaskViewSet, UserViewSet

class TaskViewSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner = User.objects.create_user(username='test_owner', password='password')
        cls.performer = User.objects.create_user(username='test_performer', password='password')
        cls.task1 = Task.objects.create(
            text='Task 1',
            owner=cls.owner,
            performer=None,
            task_status='New',
        )
        cls.task2 = Task.objects.create(
            text='Task 2',
            owner=cls.owner,
            performer=None,
            task_status='New',
        )

    def setUp(self):
        self.client = APIClient()

    def test_task_list(self):
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_task_detail(self):
        response = self.client.get(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task1.id)
        serializer = TaskSerializer(task)
        self.assertEqual(response.data, serializer.data)

    def test_task_create(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'text': 'New Task'
        }
        response = self.client.post('/api/tasks/', data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.last()
        self.assertEqual(task.text, data['text'])
        self.assertEqual(task.owner, self.owner)

    def test_task_update(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'text': 'Updated Task',
            'task_status': 'In_Progress'
        }
        response = self.client.put(f'/api/tasks/{self.task1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task1.id)
        self.assertEqual(task.text, data['text'])
        self.assertEqual(task.task_status, data['task_status'])

    def test_task_partial_update(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'task_status': 'Completed'
        }
        response = self.client.patch(f'/api/tasks/{self.task1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task1.id)
        self.assertEqual(task.task_status, data['task_status'])

    def test_task_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

class UserViewSetTestCase(TestCase):
    @classmethod
    
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner = User.objects.create_user(username='test_owner', password='password')
        cls.performer = User.objects.create_user(username='test_performer', password='password')
        cls.user = User.objects.create_user(username='test_user', password='password')

    def setUp(self):
        self.client = APIClient()

    def test_user_list(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get('/api/users/')        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_user_detail(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=self.user.id)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
