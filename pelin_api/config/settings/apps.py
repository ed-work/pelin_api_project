DEFAULT_DJANGO_APPS = [
    'material',
    'material.admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_extensions',
    'rest_framework.authtoken',
    'versatileimagefield',
    'corsheaders',
    'notifications',
    'taggit'
]

PROJECT_APPS = [
    'apps.core',
    'apps.group',
    'apps.post',
    'apps.lesson',
    'apps.assignment',
    'apps.message',
    'apps.notif',
    'apps.video'
]

INSTALLED_APPS = DEFAULT_DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS
