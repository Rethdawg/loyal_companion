from django import forms
from .models import CitiesForWeather
# Forms dashboard models


class CitiesForWeatherForm(forms.ModelForm):
    """
    Class describing forms for the CitiesForWeather model.
    """
    class Meta:
        model = CitiesForWeather
        fields = ('city_country',)

