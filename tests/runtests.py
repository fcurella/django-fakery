#!/usr/bin/env python
import os, sys, warnings

warnings.simplefilter('error', RuntimeWarning)


if hasattr(sys, 'pypy_version_info'):
    from psycopg2cffi import compat
    compat.register()

from django.conf import settings
from django_fakery.compat import HAS_GEOS


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
    'USE_TZ': True,
    'TIMEZONE': 'America/Chicago',
    'INSTALLED_APPS': [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'tests',
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
    failures = test_runner.run_tests(['tests'])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
