# core/urls.py
from django.urls import path
from .views import MessagesView, NotificationsView, SupportView

urlpatterns = [
    path('messages/', MessagesView.as_view(), name='messages'),
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('support/', SupportView.as_view(), name='support'),
]
