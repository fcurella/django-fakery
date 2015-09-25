DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SITE_ID = 1

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django_fakery.tests',
]

SILENCED_SYSTEM_CHECKS = [
    "1_7.W001",
]

ROOT_URLCONF = 'django_fakery.tests.urls'

SECRET_KEY = "secret"
