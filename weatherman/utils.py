# Module that contains some utility function for the Weatherman app
from .models import WeatherForecast
from django.utils import timezone


def check_forecast_presence(latlon: dict[str:str]) -> bool:
    """
    Checks if a forecast with a provided lattitude and longitude setting exists within the database. Returns True if it
    does, False if it does not.
    :param latlon: dict[str:str]
    :return: bool
    """
    old_forecasts = WeatherForecast.objects.filter(
        coordinate=(latlon['lat'], latlon['lon'])
    )
    if old_forecasts.exists():
        return True
    else:
        return False
