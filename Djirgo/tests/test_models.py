from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from task.models import Task

class TaskModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner = User.objects.create_user(username='test_owner', password='password')
        cls.performer = User.objects.create_user(username='test_performer', password='password')
        cls.task = Task.objects.create(
            text='Test Task',
            pub_date=timezone.now(),
            owner=cls.owner,
            performer=cls.performer,
            task_status='In_Progress'
        )

    def test_task_text(self):
        task = Task.objects.get(id=self.task.id)
        expected_text = 'Test Task'
        self.assertEqual(task.text, expected_text)

    def test_task_owner(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.owner, self.owner)

    def test_task_performer(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.performer, self.performer)

    def test_task_status(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.task_status, 'In_Progress')

    def test_task_str(self):
        task = Task.objects.get(id=self.task.id)
        expected_str = 'Test Task'
        self.assertEqual(str(task), expected_str)
