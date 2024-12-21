# settings/production.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = config(
    'PROD_ALLOWED_HOSTS', default='', \
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Activer le redirection HTTPS
SECURE_SSL_REDIRECT = True
# Configurer HSTS
SECURE_HSTS_SECONDS = 3600  # 1 heure (vous pouvez augmenter cette valeur une fois que vous êtes sûr que tout fonctionne correctement)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# Autres paramètres de sécurité
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSP_DEFAULT_SRC = ("'self'",)
# Limiter les informations de référent 
# envoyées par le navigateur
SECURE_REFERRER_POLICY = 'same-origin'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PROD_DATABASE_NAME'),
        'USER': config('PROD_DATABASE_USER'),
        'PASSWORD': config('PROD_DATABASE_PASSWORD'),
        'HOST': config('PROD_DATABASE_HOST'),
        'PORT': config('PROD_DATABASE_PORT'),
    }
}

STATIC_ROOT = BASE_DIR / 'productionfiles'

