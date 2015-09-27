from .factory import factory


class Blueprint(object):
    def __init__(self, model, fields=None, pre_save=None, post_save=None, seed=None):
        self.model = model
        self.fields = fields
        self.seed = seed
        super(Blueprint, self).__init__()

    def make_one(self, fields=None, pre_save=None, post_save=None, seed=None, iteration=None):
        _fields = self.fields.copy()
        if fields:
            _fields.update(fields)
        if seed is None:
            seed = self.seed
        return factory.make_one(self.model, _fields, pre_save, post_save, seed, iteration)

    def make(self, fields=None, pre_save=None, post_save=None, seed=None, quantity=None):
        _fields = self.fields.copy()
        if fields:
            _fields.update(fields)
        if seed is None:
            seed = self.seed
        return factory.make(self.model, _fields, pre_save, post_save, seed, quantity)
