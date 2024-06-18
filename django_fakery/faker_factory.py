import random

from functools import partial
from typing import Any, Callable, Dict, Generic, List
from typing import Optional as Opt
from typing import Tuple, Union, overload

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.forms.models import model_to_dict

from faker import Factory as FakerFactory

from . import field_mappings, rels
from .blueprint import Blueprint
from .exceptions import ForeignKeyError
from .lazy import Lazy
from .types import Built, FieldMap, LazyBuilt, LazySaveHooks, Lookup, SaveHooks, Seed, T
from .utils import get_model, get_model_fields, language_to_locale, set_related
from .values import Evaluator

user_model = get_user_model()

locale = language_to_locale(settings.LANGUAGE_CODE)


class Empty(object):
    pass


fks_cache: Dict[str, Any] = {}


class Factory(Generic[T]):
    def __init__(self, fake: Opt[FakerFactory] = None):
        self.fake = fake or FakerFactory.create(locale)
        self.field_types = field_mappings.mappings_types
        self.field_names = field_mappings.mappings_names

    def _serialize_instance(self, instance: models.Model) -> FieldMap:
        model_fields = dict(get_model_fields(instance))
        attrs: FieldMap = {}
        for k, v in model_to_dict(instance).items():
            if k == instance._meta.pk.name:  # type: ignore
                continue

            if isinstance(v, (list, models.QuerySet)):
                continue

            if isinstance(model_fields[k], models.ForeignKey) and not isinstance(
                v, models.Model
            ):
                attrs[k + "_id"] = v
                continue

            attrs[k] = v

        return attrs

    def seed(self, seed: Seed, set_global: bool = False) -> None:
        self.fake.seed(seed)
        if set_global:
            random.seed(seed)

    def blueprint(self, model: Union[str, models.Model], *args, **kwargs) -> Blueprint:
        return Blueprint(get_model(model), *args, **kwargs)

    @overload
    def build_one(
        self,
        model: str,
        fields: Opt[FieldMap],
        pre_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
        make_fks: bool,
        iteration: Opt[int],
    ) -> LazyBuilt:  # pragma: no cover
        pass

    @overload
    def build_one(
        self,
        model: T,
        fields: Opt[FieldMap],
        pre_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
        make_fks: bool,
        iteration: Opt[int],
    ) -> Built:  # pragma: no cover
        pass

    def build_one(
        self,
        model,
        fields=None,
        pre_save=None,
        seed=None,
        make_fks=False,
        iteration=None,
    ):
        if fields is None:
            fields = {}

        if pre_save is None:
            pre_save = []

        if seed:
            fake = FakerFactory.create(locale)
            fake.seed(seed)
        else:
            fake = self.fake

        evaluator = Evaluator(
            fake,
            factory=self,
            iteration=iteration,
            mappings_types=self.field_types,
            mappings_names=self.field_names,
        )

        model = get_model(model)
        instance = model()
        m2ms = {}
        lazies = []

        model_fields = get_model_fields(model)
        for _field_name, model_field in model_fields:
            value = Empty
            field_name = _field_name

            if _field_name.endswith("_id") and model_field.is_relation:
                continue

            if isinstance(model_field, models.AutoField):
                continue

            if isinstance(model_field, (GenericForeignKey, GenericRelation)):
                continue

            if field_name not in fields and (
                model_field.null or model_field.default != NOT_PROVIDED
            ):
                continue

            if field_name not in fields and isinstance(
                model_field, models.ManyToManyField
            ):
                continue

            value = fields.get(field_name, Empty)
            if isinstance(model_field, models.ForeignKey):
                if value is Empty:
                    value = fields.get(field_name + "_id", Empty)

                if value == rels.SELECT:
                    model = model_field.related_model
                    qs = model.objects.all()
                    cache_key = model

                    value = fks_cache.get(cache_key, Empty)

                    if value is Empty:
                        try:
                            value = qs[0]
                        except IndexError:
                            value = evaluator.fake_value(model, model_field)

                        fks_cache[cache_key] = value

                if not make_fks and ((value is Empty) or (value and value.pk is None)):
                    raise ForeignKeyError(
                        "Field {} is a required ForeignKey, but the related {}.{} model"
                        " doesn't have the necessary primary key.".format(
                            field_name,
                            model_field.related_model._meta.app_label,
                            model_field.related_model._meta.model_name,
                        )
                    )

                field_name += "_id"

            if value is not Empty:
                value = evaluator.evaluate(value)
            else:
                if model_field.choices:
                    value = fake.random_element(model_field.choices)[0]
                else:
                    value = evaluator.fake_value(model, model_field)

            if isinstance(value, Lazy):
                lazies.append((field_name, value))
                continue

            if isinstance(model_field, models.ForeignKey):
                value = value.pk if hasattr(value, "pk") else value

            if isinstance(model_field, models.ManyToManyField):
                m2ms[field_name] = value
            # special case for user passwords
            if model == user_model and field_name == "password":
                instance.set_password(value)
            else:
                if field_name not in m2ms:
                    setattr(instance, field_name, value)

        for field_name, lazy in lazies:
            value = getattr(instance, lazy.name)
            if callable(value):
                value = value(*lazy.args, **lazy.kwargs)
            setattr(instance, field_name, value)

        for func in pre_save:
            func(instance)

        return instance, m2ms

    @overload
    def build(
        self,
        model: str,
        fields: Opt[FieldMap],
        pre_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
        quantity: None,
        make_fks: bool,
    ) -> LazyBuilt:  # pragma: no cover
        pass

    @overload
    def build(
        self,
        model: T,
        fields: Opt[FieldMap],
        pre_save: Opt[SaveHooks[T]],
        seed: Opt[SaveHooks[T]],
        quantity: None,
        make_fks: bool,
    ) -> Built:  # pragma: no cover
        pass

    @overload
    def build(
        self,
        model: str,
        fields: Opt[FieldMap],
        pre_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
        quantity: int,
        make_fks: bool,
    ) -> List[LazyBuilt]:  # pragma: no cover
        pass

    @overload
    def build(
        self,
        model: T,
        fields: Opt[FieldMap],
        pre_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
        quantity: Opt[int],
        make_fks: bool,
    ) -> List[Built]:  # pragma: no cover
        pass

    def build(
        self,
        model,
        fields=None,
        pre_save=None,
        seed=None,
        quantity=None,
        make_fks=False,
    ):
        if fields is None:
            fields = {}

        if quantity is None:
            return self.build_one(model, fields, pre_save, seed, make_fks)[0]
        else:
            return [
                self.build_one(model, fields, pre_save, seed, make_fks, i)[0]
                for i in range(quantity)
            ]

    @overload
    def make_one(
        self,
        model: str,
        fields: Opt[FieldMap],
        pre_save: Opt[LazySaveHooks],
        post_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
        iteration: Opt[int],
    ) -> models.Model:  # pragma: no cover
        pass

    @overload
    def make_one(
        self,
        model: T,
        fields: Opt[FieldMap],
        pre_save: Opt[SaveHooks[T]],
        post_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
        iteration: Opt[int],
    ) -> T:  # pragma: no cover
        pass

    def make_one(
        self,
        model,
        fields=None,
        pre_save=None,
        post_save=None,
        seed=None,
        iteration=None,
    ):
        if fields is None:
            fields = {}

        if post_save is None:
            post_save = []

        instance, m2ms = self.build_one(
            model, fields, pre_save, seed, make_fks=True, iteration=iteration
        )

        # Sometimes the model's field for the primary key as a default, which
        # means ``instance.pk`` is already set. We pass ``force_insert`` as a
        # way to tell downstream code that this is a new model.
        instance.save(force_insert=True)

        for field, relateds in m2ms.items():
            set_related(instance, field, relateds)

        for func in post_save:
            func(instance)
        return instance

    @overload
    def get_or_make(
        self,
        model: str,
        lookup: Opt[Lookup],
        fields: Opt[FieldMap],
        pre_save: Opt[LazySaveHooks],
        post_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
    ) -> Tuple[models.Model, bool]:  # pragma: no cover
        pass

    @overload
    def get_or_make(
        self,
        model: T,
        lookup: Opt[Lookup],
        fields: Opt[FieldMap],
        pre_save: Opt[SaveHooks[T]],
        post_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
    ) -> Tuple[T, bool]:  # pragma: no cover
        pass

    def get_or_make(
        self, model, lookup=None, fields=None, pre_save=None, post_save=None, seed=None
    ):
        if lookup is None:
            lookup = {}
        if fields is None:
            fields = {}
        if post_save is None:
            post_save = []

        instance, m2ms = self.build_one(model, fields, pre_save, seed, make_fks=True)

        attrs = self._serialize_instance(instance)
        for k in lookup:
            attrs.pop(k, None)
        instance, created = get_model(model).objects.get_or_create(
            defaults=attrs, **lookup
        )

        for field, relateds in m2ms.items():
            set_related(instance, field, relateds)

        for func in post_save:
            func(instance)
        return instance, created

    @overload
    def g_m(
        self,
        model: str,
        lookup: Opt[Lookup],
        pre_save: Opt[LazySaveHooks],
        post_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
    ) -> Callable[..., models.Model]:  # pragma: no cover
        pass

    @overload
    def g_m(
        self,
        model: T,
        lookup: Opt[Lookup],
        pre_save: Opt[SaveHooks[T]],
        post_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
    ) -> Callable[..., T]:  # pragma: no cover
        pass

    def g_m(self, model, lookup=None, pre_save=None, post_save=None, seed=None):
        build = partial(
            self.get_or_make,
            model=model,
            lookup=lookup,
            pre_save=pre_save,
            post_save=post_save,
            seed=seed,
        )

        def fn(**kwargs):
            return build(fields=kwargs)

        return fn

    @overload
    def update_or_make(
        self,
        model: str,
        lookup: Opt[Lookup],
        fields: Opt[FieldMap],
        pre_save: Opt[LazySaveHooks],
        post_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
    ) -> Tuple[models.Model, bool]:  # pragma: no cover
        pass

    @overload
    def update_or_make(
        self,
        model: T,
        lookup: Opt[Lookup],
        fields: Opt[FieldMap],
        pre_save: Opt[SaveHooks[T]],
        post_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
    ) -> Tuple[T, bool]:  # pragma: no cover
        pass

    def update_or_make(
        self, model, lookup=None, fields=None, pre_save=None, post_save=None, seed=None
    ):
        if lookup is None:
            lookup = {}
        if fields is None:
            fields = {}
        if post_save is None:
            post_save = []

        model_class = get_model(model)

        try:
            instance = model_class.objects.get(**lookup)
        except model_class.DoesNotExist:
            created = True
            params = {k: v for k, v in lookup.items() if "__" not in k}
            params.update(fields)
            instance = self.make(model, params, pre_save, post_save, seed)
        else:
            created = False
            for k, v in fields.items():
                # special case for user passwords
                if model_class == user_model and k == "password":
                    instance.set_password(v)
                else:
                    setattr(instance, k, v)
            instance.save()

            for func in post_save:
                func(instance)

        return instance, created

    @overload
    def u_m(
        self,
        model: str,
        lookup: Opt[Lookup],
        pre_save: Opt[LazySaveHooks],
        post_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
    ) -> Callable[..., models.Model]:  # pragma: no cover
        pass

    @overload
    def u_m(
        self,
        model: T,
        lookup: Opt[Lookup],
        pre_save: Opt[SaveHooks[T]],
        post_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
    ) -> Callable[..., T]:  # pragma: no cover
        pass

    def u_m(self, model, lookup=None, pre_save=None, post_save=None, seed=None):
        build = partial(
            self.update_or_make,
            model=model,
            lookup=lookup,
            pre_save=pre_save,
            post_save=post_save,
            seed=seed,
        )

        def fn(**kwargs):
            return build(fields=kwargs)

        return fn

    @overload
    def make(
        self,
        model: str,
        fields: Opt[FieldMap],
        pre_save: Opt[LazySaveHooks],
        post_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
        quantity: None,
    ) -> models.Model:  # pragma: no cover
        pass

    @overload
    def make(
        self,
        model: T,
        fields: Opt[FieldMap],
        pre_save: Opt[SaveHooks[T]],
        post_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
        quantity: None,
    ) -> T:  # pragma: no cover
        pass

    @overload
    def make(
        self,
        model: str,
        fields: Opt[FieldMap],
        pre_save: Opt[LazySaveHooks],
        post_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
        quantity: Opt[int],
    ) -> List[models.Model]:  # pragma: no cover
        pass

    @overload
    def make(
        self,
        model: T,
        fields: Opt[FieldMap],
        pre_save: Opt[SaveHooks[T]],
        post_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
        quantity: Opt[int],
    ) -> List[T]:  # pragma: no cover
        pass

    def make(
        self,
        model,
        fields=None,
        pre_save=None,
        post_save=None,
        seed=None,
        quantity=None,
    ):
        if fields is None:
            fields = {}
        if quantity is None:
            return self.make_one(model, fields, pre_save, post_save, seed)
        else:
            return [
                self.make_one(model, fields, pre_save, post_save, seed, i)
                for i in range(quantity)
            ]

    @overload
    def m(
        self,
        model: str,
        pre_save: Opt[LazySaveHooks],
        post_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
        quantity: None,
    ) -> Callable[..., models.Model]:  # pragma: no cover
        pass

    @overload
    def m(
        self,
        model: T,
        pre_save: Opt[SaveHooks[T]],
        post_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
        quantity: None,
    ) -> Callable[..., T]:  # pragma: no cover
        pass

    @overload
    def m(
        self,
        model: str,
        pre_save: Opt[LazySaveHooks],
        post_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
        quantity: Opt[int],
    ) -> Callable[..., List[models.Model]]:  # pragma: no cover
        pass

    @overload
    def m(
        self,
        model: T,
        pre_save: Opt[SaveHooks[T]],
        post_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
        quantity: Opt[int],
    ) -> Callable[..., List[T]]:  # pragma: no cover
        pass

    def m(self, model, pre_save=None, post_save=None, seed=None, quantity=None):
        make = partial(
            self.make,
            model=model,
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
        self,
        model: str,
        pre_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
        quantity: None,
        make_fks: bool,
    ) -> Callable[..., LazyBuilt]:  # pragma: no cover
        pass

    @overload
    def b(
        self,
        model: T,
        pre_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
        quantity: None,
        make_fks: bool,
    ) -> Callable[..., Built]:  # pragma: no cover
        pass

    @overload
    def b(
        self,
        model: str,
        pre_save: Opt[LazySaveHooks],
        seed: Opt[Seed],
        quantity: Opt[int],
        make_fks: bool,
    ) -> Callable[..., List[LazyBuilt]]:  # pragma: no cover
        pass

    @overload
    def b(
        self,
        model: T,
        pre_save: Opt[SaveHooks[T]],
        seed: Opt[Seed],
        quantity: Opt[int],
        make_fks: bool,
    ) -> Callable[..., List[Built]]:  # pragma: no cover
        pass

    def b(self, model, pre_save=None, seed=None, quantity=None, make_fks=False):
        build = partial(
            self.build,
            model=model,
            pre_save=pre_save,
            seed=seed,
            quantity=quantity,
            make_fks=make_fks,
        )

        def fn(**kwargs):
            return build(fields=kwargs)

        return fn


factory: Factory = Factory()
