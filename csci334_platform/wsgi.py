"""
WSGI config for csci334_platform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csci334_platform.settings')

application = get_wsgi_application()

# ✅ Import and run after Django app is ready
try:
    from csci334_platform.startup import create_admin_user
    create_admin_user()
except Exception as e:
    print("⚠️ Superuser creation failed:", e)
