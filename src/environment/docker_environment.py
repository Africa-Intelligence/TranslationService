import os
from typing import Dict, Optional

from src.environment.i_environment import IEnvironment, ENV_VARS


class DockerEnvironment(IEnvironment):
    def __init__(self):
        super().__init__()
        env_vars: Dict[str, Optional[str]] = {}
        for value in ENV_VARS:
            env_vars[value.value] = os.getenv(value.value)
        self.set_config(config=env_vars)
