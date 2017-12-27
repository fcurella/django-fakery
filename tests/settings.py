DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'travis',
        'USER': 'postgres',
    }
}
USE_TZ = True

TIMEZONE = 'America/Chicago'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_fakery.tests',
]

SILENCED_SYSTEM_CHECKS = [
    "1_7.W001",
]

SECRET_KEY = 'itsasecret'
