from django.core.exceptions import ImproperlyConfigured

try:
    import psycopg2

    HAS_PSYCOPG2 = True
except ImportError:
    psycopg2 = None
    HAS_PSYCOPG2 = False

try:
    from django.contrib.gis.geos.libgeos import geos_version_info

    HAS_GEOS = geos_version_info()["version"] >= "3.3.0"
except (ImportError, OSError, ImproperlyConfigured):
    HAS_GEOS = False
