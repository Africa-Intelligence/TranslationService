from src.environment.local_environment import LocalEnvironment
from src.factory.i_builder import IBuilder


class LocalEnvironmentBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self):
        if not self._instance:
            self._instance = LocalEnvironment()
        return self._instance
