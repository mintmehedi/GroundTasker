# core/urls.py
from django.urls import path
from .views import MessagesView, NotificationsView, SupportView, SubscriptionView
from . import views

urlpatterns = [
    path('messages/', MessagesView.as_view(), name='messages'),
    path('messages/<int:thread_id>/', MessagesView.as_view(), name='messages_with_thread'),
    path('messages/<int:thread_id>/api/', views.message_api, name='message_api'),
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('support/', SupportView.as_view(), name='support'),
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
]