from django.db import models

# Create your models here.


class Currency(models.Model):
    """
    Class that describes the currency model.
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name
