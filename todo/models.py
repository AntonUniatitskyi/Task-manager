from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('to_do', 'Зробити'),
        ('in_progress', 'В процесі'),
        ('done', 'Готово'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Маленький'),
        ('medium', 'Середній'),
        ('high', 'Великий'),
    ]
    title = models.CharField(max_length=50)
    descriptions = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=20, default="medium", choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, default="to_do", choices=STATUS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    executers = models.ManyToManyField(User, related_name='appointed_tasks', blank=True)
    created_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}, {self.created_by}"
