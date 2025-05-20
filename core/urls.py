from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.messages_view, name='messages'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('support/', views.support_view, name='support'),

]
