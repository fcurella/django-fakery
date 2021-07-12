#!/usr/bin/env python
import os
import sys
import warnings

from django.conf import settings

from django_fakery.compat import HAS_GEOS

warnings.simplefilter("error", RuntimeWarning)


if hasattr(sys, "pypy_version_info"):
    from psycopg2cffi import compat

    compat.register()


DISABLE_SERVER_SIDE_CURSORS = False
if os.environ.get("PYTHON_VERSION", "").startswith("pypy"):
    DISABLE_SERVER_SIDE_CURSORS = True


SETTINGS = {
    "DATABASES": {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis"
            if HAS_GEOS
            else "django.db.backends.postgresql_psycopg2",
            "NAME": "django_fakery",
            "USER": "postgres",
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", None),
            "DISABLE_SERVER_SIDE_CURSORS": DISABLE_SERVER_SIDE_CURSORS,
            "HOST": os.environ.get("POSTGRES_HOST", None),
        }
    },
    "USE_TZ": True,
    "TIMEZONE": "America/Chicago",
    "INSTALLED_APPS": ["django.contrib.auth", "django.contrib.contenttypes", "tests"],
    "SILENCED_SYSTEM_CHECKS": ["1_7.W001"],
}


def runtests(*test_args):
    import django.test.utils

    settings.configure(**SETTINGS)

    django.setup()

    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(["tests"])
    sys.exit(failures)


if __name__ == "__main__":
    runtests()
