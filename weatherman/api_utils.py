# A module containing some API utilities
import requests as reqs
from .models import WeatherForecast
from .secrets import secrets
from .utils import check_and_renew_forecast_status
# Nominatim search

HOST_NOM = 'https://nominatim.openstreetmap.org/search?'
ENDPOINT_NOM_UNST = 'q='
PARAMS_NOM = {
    'limit': 1,
    'featureType': 'city',
    'format': 'json'
}


def get_latlon_from_city(city: str) -> dict[str:str] | None:
    """
    This function calls the Nominatim API to get the lattitude and longitude of a queried location. It returns None
    if no matches to a location are found.
    :param city:
    :return:
    """
    city_to_loc = reqs.get(HOST_NOM
                           + ENDPOINT_NOM_UNST
                           + city,
                           params=PARAMS_NOM).json()
    try:
        lat = city_to_loc[0].get('lat')
        lon = city_to_loc[0].get('lon')
    except IndexError:
        return None
    return {'lat': lat,
            'lon': lon}


# OpenWeatherMap search

HOST_OWM = 'https://api.openweathermap.org/data/2.5/'
ENDPOINT_OWM = 'weather?'


def call_or_retrieve_forecast(latlon: dict[str:str]) -> WeatherForecast | None:
    if check_and_renew_forecast_status(latlon):
        forecast = WeatherForecast.objects.filter(
            coordinate=(latlon['lat'], latlon['lon'])
        )
    else:
        payload = {
            'lat': latlon['lat'],
            'lon': latlon['lon'],
            'units': 'metric',
            'appid': secrets.OMW_API_KEY
        }
        r_source = reqs.get(HOST_OWM
                            + ENDPOINT_OWM,
                            params=payload)
        if r_source.ok:
            r_source = r_source.json()
            print(r_source)
            try:
                forecast = WeatherForecast(
                    city_country=r_source['name'] + ', ' + r_source['sys']['country'],
                    coordinate=(latlon['lat'], latlon['lon']),
                    temperature=r_source['main']['temp'],
                    pressure=r_source['main']['pressure'],
                    humidity=r_source['main']['humidity'],
                    type=r_source['weather'][0]['main'],
                    description=r_source['weather'][0]['description'],
                    icon=r_source['weather'][0]['icon'],
                    city_id=r_source['id']

                )
                forecast.save()
            except KeyError:
                return None
    return forecast

