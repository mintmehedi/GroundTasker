from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),       # Handles home, login, register, initial profile setup, auspost API proxy
    path('tasks/', include('tasks.urls')),    # Handles task posting, job listing, job detail, and task management
    path('core/', include('core.urls')),      # Handles core functionality
]