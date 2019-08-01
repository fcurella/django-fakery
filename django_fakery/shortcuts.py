from datetime import date, datetime, timedelta, tzinfo
from typing import Callable, Optional, Union

from django.conf import settings
from django.utils import timezone

from faker import Faker

ParsableDate = Union[str, int, datetime, timedelta]


def get_timezone():
    # type: () -> Optional[tzinfo]
    return timezone.get_current_timezone() if settings.USE_TZ else None


def future_datetime(end="+30d"):
    # type: (ParsableDate) -> Callable[[int, Faker], datetime]
    """
    Returns a ``datetime`` object in the future (that is, 1 second from now) up
    to the specified ``end``. ``end`` can be a string, another datetime, or a
    timedelta. If it's a string, it must start with `+`, followed by and integer
    and a unit, Eg: ``'+30d'``. Defaults to `'+30d'`

    Valid units are:
    * ``'years'``, ``'y'``
    * ``'weeks'``, ``'w'``
    * ``'days'``, ``'d'``
    * ``'hours'``, ``'hours'``
    * ``'minutes'``, ``'m'``
    * ``'seconds'``, ``'s'``
    """
    return lambda n, f: f.future_datetime(end_date=end, tzinfo=get_timezone())


def future_date(end="+30d"):
    # type: (ParsableDate) -> Callable[[int, Faker], date]
    """
    Returns a ``date`` object in the future (that is, 1 day from now) up to
    the specified ``end``. ``end`` can be a string, another date, or a
    timedelta. If it's a string, it must start with `+`, followed by and integer
    and a unit, Eg: ``'+30d'``. Defaults to `'+30d'`

    Valid units are:
    * ``'years'``, ``'y'``
    * ``'weeks'``, ``'w'``
    * ``'days'``, ``'d'``
    * ``'hours'``, ``'hours'``
    * ``'minutes'``, ``'m'``
    * ``'seconds'``, ``'s'``
    """
    return lambda n, f: f.future_date(end_date=end, tzinfo=get_timezone())


def past_datetime(start="-30d"):
    # type: (ParsableDate) -> Callable[[int, Faker], datetime]
    """
    Returns a ``datetime`` object in the past between 1 second ago and the
    specified ``start``. ``start`` can be a string, another datetime, or a
    timedelta. If it's a string, it must start with `-`, followed by and integer
    and a unit, Eg: ``'-30d'``. Defaults to `'-30d'`

    Valid units are:
    * ``'years'``, ``'y'``
    * ``'weeks'``, ``'w'``
    * ``'days'``, ``'d'``
    * ``'hours'``, ``'h'``
    * ``'minutes'``, ``'m'``
    * ``'seconds'``, ``'s'``
    """
    return lambda n, f: f.past_datetime(start_date=start, tzinfo=get_timezone())


def past_date(start="-30d"):
    # type: (ParsableDate) -> Callable[[int, Faker], date]
    """
    Returns a ``date`` object in the past between 1 day ago and the
    specified ``start``. ``start`` can be a string, another date, or a
    timedelta. If it's a string, it must start with `-`, followed by and integer
    and a unit, Eg: ``'-30d'``. Defaults to `'-30d'`

    Valid units are:
    * ``'years'``, ``'y'``
    * ``'weeks'``, ``'w'``
    * ``'days'``, ``'d'``
    * ``'hours'``, ``'h'``
    * ``'minutes'``, ``'m'``
    * ``'seconds'``, ``'s'``
    """
    return lambda n, f: f.past_date(start_date=start, tzinfo=get_timezone())
