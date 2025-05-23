from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),       # Handles home, login, register, initial profile setup, auspost API proxy
    path('tasks/', include('tasks.urls')),    # Handles task posting, job listing, job detail, and task management
    path('core/', include('core.urls')),      # Handles message, support, notification functionality
    path('admin-dashboard/', include('adminpanel.urls')),  # Handles admin dashboard and management functionality
      
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)