from src.environment.docker_environment import DockerEnvironment
from src.factory.i_builder import IBuilder


class DockerEnvironmentBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self):
        if not self._instance:
            self._instance = DockerEnvironment()
        return self._instance
