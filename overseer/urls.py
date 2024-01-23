from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='overseer-index'),
    path('tasks/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/create', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/edit', views.TaskUpdateView.as_view(), name='task-edit'),
    path('tasks/<int:pk>/delete', views.TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/subtask/<int:pk>/edit', views.SubtaskUpdateView.as_view(), name='subtask-edit'),
    path('tasks/subtask/<int:pk>/delete', views.SubtaskDeleteView.as_view(), name='subtask-delete'),
]
