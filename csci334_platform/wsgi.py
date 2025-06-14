"""
WSGI config for csci334_platform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from csci334_platform.startup import create_admin_user
create_admin_user()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csci334_platform.settings')

application = get_wsgi_application()
