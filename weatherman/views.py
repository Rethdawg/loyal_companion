from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
import requests as reqs
from .api_utils import *
import json
from django.contrib import messages

# Create your views here.


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        latlon = get_lon_lat_from_city(city)
        if latlon is not None:
            payload = {
                'lat': latlon['lat'],
                'lon': latlon['lon'],
                'units': 'metric',
                'appid': OMW_API_KEY
            }
            r_source = reqs.get(HOST_OWM
                                + ENDPOINT_OWM,
                                params=payload).json()
            print(r_source)
            data = {
                'city_country': r_source['name'] + ', ' + r_source['sys']['country'],
                'coordinate': str(r_source['coord']['lat']) + ', ' + str(r_source['coord']['lon']),
                'temp': str(r_source['main']['temp']) + ' °C',
                'pressure': r_source['main']['pressure'],
                'humidity': r_source['main']['humidity'],
                'weather_type': r_source['weather'][0]['main'],
                'description': r_source['weather'][0]['description'],
                'icon': r_source['weather'][0]['icon'],
                'city_id': r_source['id']
            }
            print(data)
        else:
            messages.error(request, 'City not found. Refine your search by adding country or region name.')
            data = {}
    else:
        data = {}
    return render(request, 'weatherman/index.html', data)
