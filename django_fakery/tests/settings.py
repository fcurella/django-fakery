DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'travis_postgis',
        'USER': 'postgres',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_fakery.tests',
]

SECRET_KEY = 'secret'

SILENCED_SYSTEM_CHECKS = [
    "1_7.W001",
]
