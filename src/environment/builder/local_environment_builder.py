from src.environment.local_environment import LocalEnvironment


class LocalEnvironmentBuilder(object):
    def __init__(self):
        self._instance = None

    def __call__(self, **kwargs):
        if not self._instance:
            self._instance = LocalEnvironment()
        return self._instance
