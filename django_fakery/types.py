from typing import Any, AnyStr, Callable, Dict, List, TypeVar, Union

from django.db import models

from .compat import NoReturn

T = TypeVar("T")
Seed = Union[AnyStr, bytearray, int]
FieldMap = Dict[str, Any]
Lookup = Dict[str, Any]
SaveHooks = List[Callable[[T], NoReturn]]
LazySaveHooks = List[Callable[[models.Model], NoReturn]]
