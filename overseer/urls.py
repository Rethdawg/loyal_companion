from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='overseer-index'),
    # path('tasks/<pk:id>',),
    # path('tasks/edit',),
    # path('tasks/delete',),
    # path('tasks/renewable',)
]
