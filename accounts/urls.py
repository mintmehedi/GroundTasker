from django.urls import path
from .views import (
    HomePageView,
    RegisterView,
    CustomLoginView,
    profile_setup,
    auspost_proxy,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('setup-profile/', profile_setup, name='setup_profile'),
    path('api/auspost/', auspost_proxy, name='auspost_proxy'),
]
