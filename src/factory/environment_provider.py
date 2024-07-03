import os

from src.environment.docker_environment import DockerEnvironment
from src.environment.local_environment import LocalEnvironment
from src.factory.i_object_factory import IObjectFactory


class EnvironmentProvider(IObjectFactory):

    def __init__(self):
        super().__init__()
        self.register_builder("docker", DockerEnvironment())
        self.register_builder("local", LocalEnvironment())

    def get(self, **kwargs):
        if os.path.exists("../.env"):
            builder = self.get_builder("local")
        else:
            builder = self.get_builder("docker")
        return builder()
