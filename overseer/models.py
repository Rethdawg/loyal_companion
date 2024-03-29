from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone
# Create your models here.


class Task(models.Model):
    """
    Class describing the Task model.
    """
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    due_date = models.DateTimeField(verbose_name='Due date')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['due_date']

    @property
    def severity(self) -> str:
        """
        This property function determines the tasks severity by calculating the difference in days between its due date
        and current server time. The less days, the more severe.
        :return: str
        """
        remaining_days = self.due_date - timezone.now()
        if remaining_days <= timezone.timedelta(days=0):
            return 'danger'
        elif remaining_days <= timezone.timedelta(days=7):
            return 'warning'
        elif remaining_days <= timezone.timedelta(days=14):
            return 'info'
        else:
            return 'light'

    @property
    def progress(self) -> int:
        """
        This property function assigns a numerical 'progress' value based on how many child Subtask instances are
        marked with the status Complete.
        :return: int
        """
        progress = 0
        for subtask in self.subtasks.all():
            progress += 1 if subtask.status == 'C' else 0
        return progress

    @property
    def progress_percentage(self) -> str:
        """
        This property function determines the completion percentage based on Subtask instance amount and status.
        :return: str
        """
        subtask_num = self.subtasks.all().count() if self.subtasks.all().count() != 0 else 1
        return str(round(100 / subtask_num * self.progress, 2)) + '%'


class SubTask(models.Model):
    """
    Class descriving the Subtask model.
    """
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    due_date = models.DateTimeField(verbose_name='Due date')
    content = HTMLField(null=True, blank=True)
    STATUS_LIST = (
        ('O', 'Ongoing'),
        ('C', 'Complete'),
        ('N', 'Not started')
    )
    status = models.CharField(choices=STATUS_LIST, max_length=1, verbose_name='Status')
    main_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')

    @property
    def severity(self) -> str:
        """
        This property function determines the Subtask's severity by calculating the difference in days between its due
        date and current server time. The less days, the more severe.
        :return: str
        """
        remaining_days = self.due_date - timezone.now()
        if remaining_days <= timezone.timedelta(days=0):
            return 'danger'
        elif remaining_days <= timezone.timedelta(days=7):
            return 'warning'
        elif remaining_days <= timezone.timedelta(days=14):
            return 'info'
        else:
            return 'light'

    def __str__(self):
        return f'{self.title}, due on {self.due_date}'

    class Meta:
        ordering = ['due_date']
