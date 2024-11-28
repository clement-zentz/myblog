import os
from django.core.exceptions import ImproperlyConfigured

DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')

if not DJANGO_SETTINGS_MODULE:
    raise ImproperlyConfigured('DJANGO_SETTINGS_MODULE environment variable is not set.')

if DJANGO_SETTINGS_MODULE == 'myblog.settings.development':
    from .development import *
elif DJANGO_SETTINGS_MODULE == 'myblog.settings.staging':
    from .staging import *
elif DJANGO_SETTINGS_MODULE == 'myblog.settings.production':
    from .production import *
else:
    raise ImproperlyConfigured(f'Unknown settings module: {DJANGO_SETTINGS_MODULE}')