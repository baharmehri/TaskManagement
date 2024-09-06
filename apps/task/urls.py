from django.urls import path

from apps.task import views

urlpatterns = [
    path('', views.TaskView.as_view(), name='new-task'),
    path('<int:pk>', views.TaskUpdateView.as_view(), name='task'),
]
