from functools import partial
from typing import Callable, Generic, List
from typing import Optional as Opt
from typing import Union, overload

from django.db import models

from .types import FieldMap, LazySaveHooks, Lookup, SaveHooks, Seed, T


class Blueprint(Generic[T]):
    def __init__(
        self,
        model: T,
        fields: Opt[FieldMap] = None,
        pre_save: Opt[SaveHooks] = None,
        post_save: Opt[SaveHooks] = None,
        seed: Opt[Seed] = None
    ):
        from .faker_factory import factory

        self.factory = factory

        self._model = model
        self._fields = fields or {}
        self.seed = seed
        self.pre_save = pre_save
        self.post_save = post_save

        self.pk = -1

    def fields(self, **kwargs: FieldMap) -> "Blueprint":
        self._fields = kwargs
        return self

    def make_one(
        self,
        fields: Opt[FieldMap] = None,
        pre_save: Opt[SaveHooks] = None,
        post_save: Opt[SaveHooks] = None,
        seed: Opt[Seed] = None,
        iteration: Opt[int] = None
    ) -> T:
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
    def make(
        self,
        fields: Opt[FieldMap],
        pre_save: Opt[SaveHooks],
        post_save: Opt[SaveHooks],
        seed: Opt[Seed],
        quantity: None
    ) -> T:
        pass

    @overload
    def make(
        self,
        fields: Opt[FieldMap],
        pre_save: Opt[SaveHooks],
        post_save: Opt[SaveHooks],
        seed: Opt[Seed],
        quantity: int,
    ) -> List[T]:
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
    def build(
        self,
        fields: Opt[FieldMap],
        pre_save: Opt[SaveHooks],
        seed: Opt[Seed],
        quantity: None,
        make_fks: bool
    ) -> T:
        pass

    @overload
    def build(
        self,
        fields: Opt[FieldMap],
        pre_save: Opt[SaveHooks],
        seed: Opt[Seed],
        quantity: int,
        make_fks: bool
    ) -> List[T]:
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
    def m(
        self,
        pre_save: Opt[SaveHooks],
        post_save: Opt[SaveHooks],
        seed: Opt[Seed],
        quantity: None
    ) -> Callable[..., T]:
        pass

    @overload
    def m(
        self,
        pre_save: Opt[SaveHooks],
        post_save: Opt[SaveHooks],
        seed: Opt[Seed],
        quantity: int
    ) -> Callable[..., List[T]]:
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
    def b(
        self, pre_save: Opt[SaveHooks], seed: Opt[Seed], quantity: None, make_fks: bool
    ) -> Callable[..., T]:
        pass

    @overload
    def b(
        self, pre_save: Opt[SaveHooks], seed: Opt[Seed], quantity: int, make_fks: bool
    ) -> Callable[..., List[T]]:
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
