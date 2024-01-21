from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='memory-index'),
    path('all-memos/', views.MemoList.as_view(), name='memos-all'),
]
