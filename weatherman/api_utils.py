# A module containing some API utilities
import requests as reqs
# Nominatim search

HOST_NOM = 'https://nominatim.openstreetmap.org/search?'
ENDPOINT_NOM_UNST = 'q='
PARAMS_NOM = {
    'limit': 1,
    'featureType': 'city',
    'format': 'json'
}


def get_lon_lat_from_city(city):
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
OMW_API_KEY = '4e99e672008000305d3ed6adc81e4b65'
