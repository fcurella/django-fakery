from functools import partial
from typing import Any, Callable, Generic, List
from typing import Optional as Opt
from typing import overload

from .types import Built, FieldMap, SaveHooks, Seed, T


class Blueprint(Generic[T]):
    def __init__(self, model, fields=None, pre_save=None, post_save=None, seed=None):
        # type: (T, Opt[FieldMap], Opt[SaveHooks], Opt[SaveHooks], Opt[Seed]) -> None
        from .faker_factory import factory

        self.factory = factory

        self._model = model
        self._fields = fields or {}
        self.seed = seed
        self.pre_save = pre_save
        self.post_save = post_save

        self.pk = -1

    def fields(self, **kwargs):
        # type: (**Any) -> "Blueprint"
        return Blueprint(
            model=self._model,
            fields=dict(self._fields, **kwargs),
            pre_save=self.pre_save,
            post_save=self.post_save,
            seed=self.seed,
        )

    def make_one(
        self, fields=None, pre_save=None, post_save=None, seed=None, iteration=None
    ):
        # type: (Opt[FieldMap], Opt[SaveHooks], Opt[SaveHooks], Opt[Seed], Opt[int]) -> T
        _fields = self._fields.copy()
        if fields:
            _fields.update(fields)
        if seed is None:
            seed = self.seed

        if pre_save is None:
            pre_save = self.pre_save

        if post_save is None:
            post_save = self.post_save

        return self.factory.make_one(
            self._model, _fields, pre_save, post_save, seed, iteration
        )

    @overload
    def make(self, fields, pre_save, post_save, seed, quantity):  # pragma: no cover
        # type: (Opt[FieldMap], Opt[SaveHooks], Opt[SaveHooks], Opt[Seed], None) -> T
        pass

    @overload
    def make(self, fields, pre_save, post_save, seed, quantity):  # pragma: no cover
        # type: (Opt[FieldMap], Opt[SaveHooks], Opt[SaveHooks], Opt[Seed], int) -> List[T]
        pass

    def make(
        self, fields=None, pre_save=None, post_save=None, seed=None, quantity=None
    ):
        _fields = self._fields.copy()
        if fields:
            _fields.update(fields)
        if seed is None:
            seed = self.seed

        if pre_save is None:
            pre_save = self.pre_save

        if post_save is None:
            post_save = self.post_save

        return self.factory.make(
            self._model, _fields, pre_save, post_save, seed, quantity
        )

    @overload
    def build(self, fields, pre_save, seed, quantity, make_fks):  # pragma: no cover
        # type: (Opt[FieldMap], Opt[SaveHooks], Opt[Seed], None, bool) -> Built
        pass

    @overload
    def build(self, fields, pre_save, seed, quantity, make_fks):  # pragma: no cover
        # type: (Opt[FieldMap], Opt[SaveHooks], Opt[Seed], int, bool) -> List[Built]
        pass

    def build(
        self, fields=None, pre_save=None, seed=None, quantity=None, make_fks=False
    ):
        _fields = self._fields.copy()
        if fields:
            _fields.update(fields)
        if seed is None:
            seed = self.seed

        if pre_save is None:
            pre_save = self.pre_save

        return self.factory.build(
            self._model, _fields, pre_save, seed, quantity, make_fks
        )

    @overload
    def m(self, pre_save, post_save, seed, quantity):  # pragma: no cover
        # type: (Opt[SaveHooks], Opt[SaveHooks], Opt[Seed], None) -> Callable[..., T]
        pass

    @overload
    def m(self, pre_save, post_save, seed, quantity):  # pragma: no cover
        # type: (Opt[SaveHooks], Opt[SaveHooks], Opt[Seed], int) -> Callable[..., List[T]]
        pass

    def m(self, pre_save=None, post_save=None, seed=None, quantity=None):
        make = partial(
            self.make,
            pre_save=pre_save,
            post_save=post_save,
            seed=seed,
            quantity=quantity,
        )

        def fn(**kwargs):
            return make(fields=kwargs)

        return fn

    @overload
    def b(self, pre_save, seed, quantity, make_fks):  # pragma: no cover
        # type: (Opt[SaveHooks], Opt[Seed], None, bool) -> Callable[..., Built]
        pass

    @overload
    def b(self, pre_save, seed, quantity, make_fks):  # pragma: no cover
        # type: (Opt[SaveHooks], Opt[Seed], int, bool) -> Callable[..., List[Built]]
        pass

    def b(self, pre_save=None, seed=None, quantity=None, make_fks=False):
        build = partial(
            self.build,
            pre_save=pre_save,
            seed=seed,
            quantity=quantity,
            make_fks=make_fks,
        )

        def fn(**kwargs):
            return build(fields=kwargs)

        return fn
