"""
WSGI config for woodkirkvalleydata project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

path = '/Users/imacdonald/PycharmProjects/woodkirkvalleydata'

if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woodkirkvalleydata.settings')

application = get_wsgi_application()
