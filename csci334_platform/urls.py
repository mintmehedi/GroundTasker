from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),       # Handles home, login, register, etc.
    path('tasks/', include('tasks.urls')),    # Handles task posting
]
