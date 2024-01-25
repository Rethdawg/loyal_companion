from django.test import TestCase
from .api_utils import create_or_retrieve_forecast
from .models import WeatherForecast
from django.test import Client
# Create your tests here.
client = Client()


class WeatherForecastTest(TestCase):
    def test_if_new_forecast_call_works(self):
        """
        Test to see if a WeatherForecast instance is created successfully using tested and working coordinates.
        :return:
        """
        latlon = {'lat': 54.6870458,
                  'lon': 25.2829111}
        test_obj = create_or_retrieve_forecast(latlon)
        self.assertIsInstance(test_obj, WeatherForecast)
