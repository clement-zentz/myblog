"""
URL configuration for myblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
# media files
from django.conf import settings
from django.conf.urls.static import static
from blog.views import home
# load env var
from decouple import config

admin_custom_url = config("ADMIN_URL")

env_string = config("DJANGO_SETTINGS_MODULE")
env_splited = env_string.rsplit('.', 1)
last_part = env_splited[-1]

if last_part in ['production', 'staging']:
    admin_url = admin_custom_url
else:
    admin_url = 'admin/'

urlpatterns = [
    path(admin_url, admin.site.urls),
    # translation
    path('i18n/', include('django.conf.urls.i18n')),
    # blog app  
    path('', home, name='home'),
    path("blog/", include("blog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
