from django.contrib import admin
from .models import WeatherForecast
# Register your models here.


class WeatherForecastAdmin(admin.ModelAdmin):
    """
    Class that edits WeatherForecast instances' display in the admin panel.
    """
    model = WeatherForecast
    list_display = ('city_country', 'pub_date')


admin.site.register(WeatherForecast, WeatherForecastAdmin)
