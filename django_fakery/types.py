from typing import Any, AnyStr, Callable, Dict, List, Tuple, Type, TypeVar, Union

from django.db import models

T = TypeVar("T", bound=models.Model)
Seed = Union[AnyStr, bytearray, int]
FieldMap = Dict[str, Any]
Lookup = Dict[str, Any]
SaveHooks = List[Callable[[T], None]]
LazySaveHooks = List[Callable[[models.Model], None]]
Built = Tuple[T, Dict[str, List[models.Model]]]
LazyBuilt = Tuple[models.Model, Dict[str, List[models.Model]]]
