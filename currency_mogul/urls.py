from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='currency-index'),
    path('historical/', views.historical_graph, name='currency-historical')
]
