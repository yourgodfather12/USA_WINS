"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Setting the default Django settings module for WSGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# WSGI application for serving the project
application = get_wsgi_application()
