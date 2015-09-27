class Lazy(object):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        super(Lazy, self).__init__()
