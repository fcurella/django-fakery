import os, sys

from django_fakery.compat import HAS_GEOS

if hasattr(sys, 'pypy_version_info'):
    from psycopg2cffi import compat
    compat.register()



DISABLE_SERVER_SIDE_CURSORS = False
if os.environ.get('TRAVIS_PYTHON_VERSION') == 'pypy':
    DISABLE_SERVER_SIDE_CURSORS = True


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis' if HAS_GEOS else 'django.db.backends.postgresql_psycopg2',
        'NAME': 'travis_postgis',
        'USER': 'postgres',
        'DISABLE_SERVER_SIDE_CURSORS': DISABLE_SERVER_SIDE_CURSORS,
    }
}
USE_TZ = True

TIMEZONE = 'America/Chicago'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'tests',
]

SILENCED_SYSTEM_CHECKS = [
    "1_7.W001",
]

SECRET_KEY = 'itsasecret'
