import sys


try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    psycopg2 = None
    HAS_PSYCOPG2 = False


if sys.version < '3':
    text_type = unicode
    binary_type = str
    string_types = basestring
else:
    text_type = str
    binary_type = bytes
    string_types = str
