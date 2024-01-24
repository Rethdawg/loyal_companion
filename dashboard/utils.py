from weatherman.api_utils import get_latlon_from_city, call_or_retrieve_forecast
from weatherman.models import WeatherForecast
from django.contrib import messages
from .models import CitiesForWeather


# Utility functions for the dashboard module


def add_or_renew_tracked_forecast(request, city: CitiesForWeather):
    latlon = get_latlon_from_city(city.city_country)
    print(latlon)
    if latlon is None:
        messages.error(request, f'City name/code {city.city_country} invalid. Try another search.')
        city.delete()
    forecast = call_or_retrieve_forecast(latlon)
    print(forecast)
    return forecast
