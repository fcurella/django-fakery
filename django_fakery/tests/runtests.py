#!/usr/bin/env python
import sys

from django.conf import settings


settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django_fakery.tests',
    ],
    SILENCED_SYSTEM_CHECKS=[
        "1_7.W001",
    ],
)


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
