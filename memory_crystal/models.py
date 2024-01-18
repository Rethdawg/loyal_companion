from django.db import models
from tinymce.models import HTMLField

# Create your models here.


class Memo(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=20, unique=True)
    content = HTMLField()
    STATUS = (
        ('D', 'Draft'),
        ('P', 'Published'),
        ('A', 'Archived')
    )
    status = models.CharField(choices=STATUS, default=0, max_length=1)



