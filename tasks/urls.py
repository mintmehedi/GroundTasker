# tasks/urls.py
from django.urls import path
from . import views
from .views import manage_tasks

urlpatterns = [
    path('post/', views.post_task, name='post_task'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:task_id>/', views.job_detail, name='job_detail'),
    path('manage/', manage_tasks, name='manage_tasks'),
    


    
]
