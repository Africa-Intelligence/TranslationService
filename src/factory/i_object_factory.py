class IObjectFactory(object):
    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)

    def get(self, key, **kwargs):
        return self.create(key, **kwargs)

    def get_builder(self, key):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder
