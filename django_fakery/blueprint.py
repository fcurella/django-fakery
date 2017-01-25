from functools import partial


class Blueprint(object):
    def __init__(self, model, fields=None, pre_save=None, post_save=None, seed=None):
        from .faker_factory import factory

        self.factory = factory

        self._model = model
        self._fields = fields or {}
        self.seed = seed
        self.pre_save = pre_save
        self.post_save = post_save

        self.pk = -1
        super(Blueprint, self).__init__()

    def fields(self, **kwargs):
        self._fields = kwargs
        return self

    def make_one(self, fields=None, pre_save=None, post_save=None, seed=None, iteration=None):
        _fields = self._fields.copy()
        if fields:
            _fields.update(fields)
        if seed is None:
            seed = self.seed

        if pre_save is None:
            pre_save = self.pre_save

        if post_save is None:
            post_save = self.post_save

        return self.factory.make_one(self._model, _fields, pre_save, post_save, seed, iteration)

    def make(self, fields=None, pre_save=None, post_save=None, seed=None, quantity=None):
        _fields = self._fields.copy()
        if fields:
            _fields.update(fields)
        if seed is None:
            seed = self.seed

        if pre_save is None:
            pre_save = self.pre_save

        if post_save is None:
            post_save = self.post_save

        return self.factory.make(self._model, _fields, pre_save, post_save, seed, quantity)

    def build(self, fields=None, pre_save=None, seed=None, quantity=None, make_fks=False):
        _fields = self._fields.copy()
        if fields:
            _fields.update(fields)
        if seed is None:
            seed = self.seed

        if pre_save is None:
            pre_save = self.pre_save

        return self.factory.build(self._model, _fields, pre_save, seed, quantity, make_fks)

    def m(self, pre_save=None, post_save=None, seed=None, quantity=None):
        make = partial(self.make, pre_save=pre_save, post_save=post_save, seed=seed, quantity=quantity)

        def fn(**kwargs):
            return make(fields=kwargs)

        return fn

    def b(self, pre_save=None, seed=None, quantity=None, make_fks=False):
        build = partial(self.build, pre_save=pre_save, seed=seed, quantity=quantity, make_fks=make_fks)

        def fn(**kwargs):
            return build(fields=kwargs)

        return fn
