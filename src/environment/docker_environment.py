import os
from typing import Dict, Optional

from src.environment.i_environment import IEnvironment, EnvVar


class DockerEnvironment(IEnvironment):
    def __init__(self):
        super().__init__()
        env_vars: Dict[str, Optional[str]] = {}
        to_language_key = EnvVar.ToLanguages.value
        for value in EnvVar:
            if value == to_language_key:
                env_vars[to_language_key] = env_vars[to_language_key].split(',')
            else:
                env_vars[value.value] = os.getenv(value.value)
        self.set_config(config=env_vars)
