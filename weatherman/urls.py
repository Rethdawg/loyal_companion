# urls file for the weatherman app
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='weather-index'),
    path('<int:pk>/delete', views.WeatherForecastDeleteView.as_view(), name='weather-delete')
]
