from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='memory-index'),
    path('memo/all', views.MemoList.as_view(), name='memos-all'),
    path('memo/category/<str:category_name>', views.memo_by_category, name='memo-category'),
    path('memo/<str:slug>', views.MemoDetailView.as_view(), name='memo-detail'),
    path('memo/<str:slug>/edit', views.MemoUpdateView.as_view(), name='memo-edit'),
    path('memo/<str:slug>/delete', views.MemoDeleteView.as_view(), name='memo-delete'),
    path('birthday/all', views.birthday_list_view, name='birthdays-all'),
    path('birthday/<int:pk>', views.BirthdayDetailView.as_view(), name='birthday-detail'),
    path('birthday/<int:pk>/edit', views.BirthdayUpdateView.as_view(), name='birthday-edit'),
    path('birthday/<int:pk>/delete', views.BirthdayDeleteView.as_view(), name='birthday-delete'),
    path('birthdaynotes/<int:pk>/edit', views.BirthdayNoteUpdateView.as_view(), name='birthdaynote-edit'),
    path('birthdaynotes/<int:pk>/delete', views.BirthdayNoteDeleteView.as_view(), name='birthdaynote-delete')
]
