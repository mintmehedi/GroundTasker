from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    HomePageView,
    RegisterView,
    CustomLoginView,
    ProfileSetupView,
    EditProfileView,
    PublicProfileView,
    ChangeEmailView,
    ChangePasswordView,
    DashboardView,
    LogoutConfirmView,
    auspost_proxy,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('setup-profile/', ProfileSetupView.as_view(), name='setup_profile'),
    path('api/auspost/', auspost_proxy, name='auspost_proxy'),  # function-based for external API
    path('logout/', LogoutView.as_view(next_page='logout_confirm'), name='logout'),
    path('logout-confirm/', LogoutConfirmView.as_view(), name='logout_confirm'),
    path('profile/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', PublicProfileView.as_view(), name='public_profile'),
    path('settings/change-email/', ChangeEmailView.as_view(), name='change_email'),
    path('settings/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
