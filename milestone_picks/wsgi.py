"""
WSGI config for milestone_picks project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


# os.environ["DJANGO_SETTINGS_MODULE"] = "milestone_picks.settings"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'milestone_picks.settings')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', environment)
application = get_wsgi_application()

