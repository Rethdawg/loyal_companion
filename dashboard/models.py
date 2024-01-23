from django.db import models

# Create your models here.


class FeedEntry(models.Model):
    """
    Class used by entries in the app's feeds.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField(blank=True, null=True)
    entry_type = models.CharField(max_length=200)
    guid = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.entry_type}: {self.title}'
