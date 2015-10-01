class Blueprint(object):
    def __init__(self, model, fields=None, pre_save=None, post_save=None, seed=None):
        from .faker_factory import factory

        self.factory = factory

        self.model = model
        self.fields = fields
        self.seed = seed
        self.pre_save = pre_save
        self.post_save = post_save
        super(Blueprint, self).__init__()

    def make_one(self, fields=None, pre_save=None, post_save=None, seed=None, iteration=None):
        _fields = self.fields.copy()
        if fields:
            _fields.update(fields)
        if seed is None:
            seed = self.seed

        if pre_save is None:
            pre_save = self.pre_save

        if post_save is None:
            post_save = self.post_save

        return self.factory.make_one(self.model, _fields, pre_save, post_save, seed, iteration)

    def make(self, fields=None, pre_save=None, post_save=None, seed=None, quantity=None):
        _fields = self.fields.copy()
        if fields:
            _fields.update(fields)
        if seed is None:
            seed = self.seed

        if pre_save is None:
            pre_save = self.pre_save

        if post_save is None:
            post_save = self.post_save

        return self.factory.make(self.model, _fields, pre_save, post_save, seed, quantity)
