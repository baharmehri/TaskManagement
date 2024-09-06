from django.db import models

from apps.base.models import BaseModel


class Task(BaseModel):
    class TaskStatus(models.TextChoices):
        TODO = 'todo'
        PENDING = 'pending'
        COMPLETED = 'completed),'
        DONE = 'done'
        FAILED = 'failed'

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.PENDING)
