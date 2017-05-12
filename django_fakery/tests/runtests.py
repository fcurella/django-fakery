#!/usr/bin/env python
import os, sys


if hasattr(sys, 'pypy_version_info'):
    from psycopg2cffi import compat
    compat.register()

from django.conf import settings

try:
    from django.contrib.gis.geos.libgeos import geos_version_info
    HAS_GEOS = geos_version_info()['version'] >= '3.3.0'
except (ImportError, OSError):
    HAS_GEOS = False


DISABLE_SERVER_SIDE_CURSORS = False
if os.environ.get('TRAVIS_PYTHON_VERSION') == 'pypy':
    DISABLE_SERVER_SIDE_CURSORS = True


SETTINGS = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis' if HAS_GEOS else 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travis_postgis',
            'USER': 'postgres',
            'DISABLE_SERVER_SIDE_CURSORS': DISABLE_SERVER_SIDE_CURSORS,
        }
    },
    'INSTALLED_APPS': [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django_fakery.tests',
    ],
    'SILENCED_SYSTEM_CHECKS': [
        "1_7.W001",
    ],
}


def runtests(*test_args):
    import django.test.utils

    settings.configure(**SETTINGS)

    if django.VERSION[0:2] >= (1, 7):
        django.setup()

    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['django_fakery'])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
