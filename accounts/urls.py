from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    HomePageView,
    RegisterView,
    CustomLoginView,
    profile_setup,
    auspost_proxy,
    LogoutConfirmView,
    edit_profile,
    public_profile_view,
    change_email, 
    change_password,
    dashboard,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('setup-profile/', profile_setup, name='setup_profile'),
    path('api/auspost/', auspost_proxy, name='auspost_proxy'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('logout-confirm/', LogoutConfirmView.as_view(), name='logout_confirm'),
    path('profile/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/', public_profile_view, name='public_profile'),
    path('settings/change-email/', change_email, name='change_email'),
    path('settings/change-password/', change_password, name='change_password'),
    path('dashboard/', dashboard, name='dashboard'),


]
