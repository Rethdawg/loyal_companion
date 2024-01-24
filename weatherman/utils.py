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
    old_forecasts = WeatherForecast.objects.filter(
        coordinate=(latlon['lat'], latlon['lon'])
    )
    if old_forecasts.exists():
        for old_forecast in old_forecasts:
            if old_forecast.is_outdated:
                old_forecast.delete()
                return False
            else:
                return True
    else:
        return False

