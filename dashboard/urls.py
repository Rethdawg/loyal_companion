from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('add_city/', views.CityForWeatherCreateView.as_view(), name='city-create'),
    path('del_city/<int:pk>', views.CityForWeatherDeleteView.as_view(), name='city-delete')
]
