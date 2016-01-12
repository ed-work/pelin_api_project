import os
from .apps import INSTALLED_APPS

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

