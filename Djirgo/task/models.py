from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

CHOICES = (
    ('New', 'Создана'),
    ('In_Progress', 'В работе'),
    ('Completed', 'Ответ'),
)

User = get_user_model()

class Task(models.Model):
    text = models.TextField(
        'Текст поста'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner_tasks'
        )
    performer = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='performer_tasks') 
    task_status = models.CharField(max_length=12, choices=CHOICES,
                                 default='New')


    def __str__(self):
        return self.text
