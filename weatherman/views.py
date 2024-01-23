from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .api_utils import get_latlon_from_city, call_or_retrieve_forecast
from django.contrib import messages
from .models import WeatherForecast
from django.views import generic
# Create your views here.


def index(request):
    """
    Index view function.
    :param request: request object
    :return: render template
    """
    if request.method == 'POST':
        city = request.POST['city']
        latlon = get_latlon_from_city(city)
        if latlon is not None:
            forecast = call_or_retrieve_forecast(latlon)
            if forecast is None:
                messages.error(request, 'OpenWeatherMap API error. Please try again later.')
        else:
            messages.error(request, 'City not found. Refine your search by adding country or region name.')
        return redirect('weather-index')
    all_forecasts = WeatherForecast.objects.all()
    context = {
        'all_forecasts': all_forecasts
    }
    return render(request, 'weatherman/index.html', context=context)


class WeatherForecastDeleteView(generic.DeleteView):
    model = WeatherForecast
    template_name = 'weatherman/index.html'
    success_url = reverse_lazy('weather-index')
