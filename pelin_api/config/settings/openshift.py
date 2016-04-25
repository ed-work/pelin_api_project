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
        'NAME': os.environ.get('OPENSHIFT_DB_NAME'),
        'USER': os.environ.get('OPENSHIFT_DB_USERNAME'),
        'PASSWORD': os.environ.get('OPENSHIFT_DB_PASS'),
        'HOST': os.environ.get('OPENSHIFT_POSTGRESQL_DB_HOST'),
        'PORT': os.environ.get('OPENSHIFT_POSTGRESQL_DB_PORT')
    }
}

STATIC_ROOT = os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'static')
