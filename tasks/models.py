from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        (0, 'TODO'),
        (1, 'ACTIVE'),
        (2, 'REVIEW'),
        (3, 'COMPLETE'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        (0, 'TODO'),
        (1, 'ACTIVE'),
        (2, 'REVIEW'),
        (3, 'COMPLETE'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title