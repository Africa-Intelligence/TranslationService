from src.environment.i_environment import IEnvironment


class IObjectFactory(object):
    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, environment: IEnvironment):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(environment)

    def get(self, key, environment: IEnvironment):
        return self.create(key, environment)

    def get_builder(self, key):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder
