import os

from src.environment.builder.docker_environment_builder import DockerEnvironmentBuilder
from src.environment.builder.local_environment_builder import LocalEnvironmentBuilder
from src.factory.i_object_factory import IObjectFactory


class EnvironmentProvider(IObjectFactory):

    def __init__(self):
        super().__init__()
        self.register_builder("docker", DockerEnvironmentBuilder())
        self.register_builder("local", LocalEnvironmentBuilder())

    def get(self, **kwargs):
        if is_local_env_file_exist():
            builder = self.get_builder("local")
        else:
            builder = self.get_builder("docker")
        return builder()


def is_local_env_file_exist():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir != os.path.dirname(current_dir):  # Stop at the root directory
        if os.path.exists(os.path.join(current_dir, 'README.md')):
            env_file = os.path.join(current_dir, '.env')
            if os.path.exists(env_file):
                return True
            else:
                return False
        current_dir = os.path.dirname(current_dir)
