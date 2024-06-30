from src.environment.docker_environment import DockerEnvironment


class DockerEnvironmentBuilder(object):
    def __init__(self):
        self._instance = None

    def __call__(self, **kwargs):
        if not self._instance:
            self._instance = DockerEnvironment()
        return self._instance
