from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='memory-index'),
    path('all_memos/', views.MemoList.as_view(), name='memos-all'),
    path('memo_category/<str:category_name>', views.memo_by_category, name='memo-category')
]
