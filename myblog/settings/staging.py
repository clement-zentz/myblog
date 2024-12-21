# settings/staging.py
from .base import *

DEBUG = True

ALLOWED_HOSTS = config(
    'STAGE_ALLOWED_HOSTS', default='', \
    cast=lambda v: [s.strip() for s in v.split(',')]
) 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('STAGE_DATABASE_NAME'),
        'USER': config('STAGE_DATABASE_USER'),
        'PASSWORD': config('STAGE_DATABASE_PASSWORD'),
        'HOST': config('STAGE_DATABASE_HOST'),
        'PORT': config('STAGE_DATABASE_PORT'),
    }
}

STATIC_ROOT = BASE_DIR / 'productionfiles'