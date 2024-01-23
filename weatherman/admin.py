from django.contrib import admin
from .models import WeatherForecast
# Register your models here.


class WeatherForecastAdmin(admin.ModelAdmin):
    model = WeatherForecast
    list_display = ('city_country', 'pub_date')


admin.site.register(WeatherForecast, WeatherForecastAdmin)
