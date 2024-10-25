# settings/development.py
from .base import *

ALLOWED_HOSTS = config(
    'DEV_ALLOWED_HOSTS', default='', \
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# ALLOWED_HOSTS=[]

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DEV_DATABASE_NAME'),
        'USER': config('DEV_DATABASE_USER'),
        'PASSWORD': config('DEV_DATABASE_PASSWORD'),
        'HOST': config('DEV_DATABASE_HOST'),
        'PORT': config('DEV_DATABASE_PORT'),
    }
}