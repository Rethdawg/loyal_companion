from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='memory-index'),
    path('memo/all', views.MemoList.as_view(), name='memos-all'),
    path('memo/category/<str:category_name>', views.memo_by_category, name='memo-category'),
    path('memo/<str:slug>', views.MemoDetailView.as_view(), name='memo-detail'),
    path('memo/<str:slug>/edit', views.MemoUpdateView.as_view(), name='memo-edit'),
    path('memo/<str:slug>/delete', views.MemoDeleteView.as_view(), name='memo-delete'),
    path('birthday/all', views.BirthdayListView.as_view(), name='birthdays-all'),
    path('birthday/<int:pk>', views.BirthdayDetailView.as_view(), name='birthday-detail')
]
