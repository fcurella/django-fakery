#!/usr/bin/env python
import os
import sys


if hasattr(sys, 'pypy_version_info'):
    from psycopg2cffi import compat
    compat.register()

from django.conf import settings


SETTINGS = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'travis_postgis',
            'USER': 'postgres',
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

if os.path.exists('/usr/local/lib/mod_spatialite.dylib'):
    SETTINGS['SPATIALITE_LIBRARY_PATH'] = '/usr/local/lib/mod_spatialite.dylib'

settings.configure(**SETTINGS)


def runtests(*test_args):
    import django.test.utils

    if django.VERSION[0:2] >= (1, 7):
        django.setup()

    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['django_fakery'])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
