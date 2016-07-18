import os
from .base import *
from .apps import INSTALLED_APPS

DEBUG = False
INSTALLED_APPS = INSTALLED_APPS
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PELIn_DB_NAME'),
        'USER': os.environ.get('PELIN_DB_USERNAME'),
        'PASSWORD': os.environ.get('PELIN_DB_PASS'),
        'HOST': os.environ.get('PELIN_DB_HOST'),
        'PORT': os.environ.get('PELIN_DB_PORT')
    }
}

# STATIC_ROOT = os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'static')
# MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
# MEDIA_URL = '/static/media/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.environ.get('OPENSHIFT_LOG_DIR'),
                                     'django.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
