from django.db import models
from django.utils import timezone
# Create your models here.


class WeatherForecast(models.Model):
    """
    Class that describes a retrieved weather forecast.
    """
    city_country = models.CharField(max_length=100)
    coordinate = models.CharField(max_length=200)
    temperature = models.IntegerField()
    pressure = models.IntegerField()
    humidity = models.IntegerField()
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=20)
    city_id = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.city_country} at {self.pub_date}'

    @property
    def is_outdated(self):
        time_difference = timezone.now() - self.pub_date
        if time_difference > timezone.timedelta(minutes=59, seconds=59):
            return True
        else:
            return False

