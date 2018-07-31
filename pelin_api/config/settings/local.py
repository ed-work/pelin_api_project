from .base import *
from .apps import INSTALLED_APPS

# LOCAL_APPS = [
#     'debug_toolbar',
# ]

# INSTALLED_APPS += LOCAL_APPS

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pelin_api',
        'USER': 'pelin_api',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': ''
    }
}
