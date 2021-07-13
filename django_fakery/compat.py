from django.core.exceptions import ImproperlyConfigured

try:
    import psycopg2

    HAS_PSYCOPG2 = True

    try:
        from django.contrib.postgres.fields import DecimalRangeField
    except ImportError:
        from django.contrib.postgres.fields import FloatRangeField as DecimalRangeField
except ImportError:
    psycopg2 = None
    HAS_PSYCOPG2 = False

try:
    from django.contrib.gis.geos.libgeos import geos_version_tuple

    HAS_GEOS = geos_version_tuple() >= (3, 3, 0)
except (ImportError, OSError, ImproperlyConfigured):
    HAS_GEOS = False
