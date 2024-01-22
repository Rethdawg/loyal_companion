from django.db import models
from tinymce.models import HTMLField
# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    due_date = models.DateField(verbose_name='Due date')


class SubTask(models.Model):
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    due_date = models.DateField(verbose_name='Due date')
    content = HTMLField()
    STATUS_LIST = (
        ('O', 'Ongoing'),
        ('C', 'Complete'),
        ('N', 'Not started')
    )
    status = models.CharField(choices=STATUS_LIST, max_length=1, verbose_name='Status')
    main_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
