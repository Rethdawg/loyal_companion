from weatherman.api_utils import get_latlon_from_city, create_or_retrieve_forecast
from weatherman.models import WeatherForecast
from django.contrib import messages
from .models import CitiesForWeather
import logging

# Utility functions for the dashboard module


def retrieve_all_tracked_forecasts() -> list | None:
    """
    Function retrieves or creates fresh forecasts for tracked cities within the database. Returns None if there is an
    error retrieving latlon data.
    :return: list or None
    """
    list_of_forecasts = []
    for tracked_city in CitiesForWeather.objects.all():
        latlon = get_latlon_from_city(tracked_city.city_country)
        if latlon is None:
            logging.error('Failed retrieving latlon for a tracked city.')
            return None
        list_of_forecasts.append(create_or_retrieve_forecast(latlon))
    return list_of_forecasts
