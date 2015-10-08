#!/usr/bin/env python
import sys


if hasattr(sys, 'pypy_version_info'):
    from psycopg2cffi import compat
    compat.register()

from django.conf import settings
from django.contrib.gis.geos import HAS_GEOS

SETTINGS = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis' if HAS_GEOS else 'django.db.backends.postgresql_psycopg2',
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
