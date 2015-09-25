from .factory import factory


class Blueprint(object):
    def __init__(self, model, fields=None, seed=None):
        self.model = model
        self.fields = fields
        self.seed = seed
        super(Blueprint, self).__init__()

    def make_one(self, fields=None, seed=None, iteration=None):
        _fields = self.fields.copy()
        if fields:
            _fields.update(fields)
        if seed is None:
            seed = self.seed
        return factory.make_one(self.model, _fields, seed, iteration)

    def make(self, fields=None, seed=None, quantity=None):
        _fields = self.fields.copy()
        if fields:
            _fields.update(fields)
        if seed is None:
            seed = self.seed
        return factory.make(self.model, _fields, seed, quantity)
