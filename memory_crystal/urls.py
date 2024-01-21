from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='memory-index'),
    path('all_memos/', views.MemoList.as_view(), name='memos-all'),
    path('memo_category/<str:category_name>', views.memo_by_category, name='memo-category'),
    path('memos/<str:slug>', views.MemoDetailView.as_view(), name='memo-detail'),
    path('memos/<str:slug>/edit', views.MemoUpdateView.as_view(), name='memo-edit'),
    path('memos/<str:slug>/delete', views.MemoDeleteView.as_view(), name='memo-delete')
]
