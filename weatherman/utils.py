# Module that contains some utility function for the Weatherman app
from .models import WeatherForecast
from django.utils import timezone


def check_and_renew_forecast_status(latlon: dict[str:str]) -> bool:
    """
    This function checks if a WeatherForecast instance with a matching coordinate exists
    and if it is outdated. If it is outdated, it deletes the forecast.
    :param latlon: dictionary of lattitude and longitude
    :return: bool
    """
    old_forecast = WeatherForecast.objects.filter(
        coordinate=(latlon['lat'], latlon['lon'])
    )
    if old_forecast.exists():
        if old_forecast.is_outdated:
            old_forecast.delete()
            return False
        else:
            return True
    else:
        return False

