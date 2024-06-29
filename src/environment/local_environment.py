from typing import Dict, Optional

from dotenv import dotenv_values

from src.environment.i_environment import IEnvironment


class LocalEnvironment(IEnvironment):
    def __init__(self):
        super().__init__()
        env_vars: Dict[str, Optional[str]] = dotenv_values("../.env")
        env_vars['TO_LANGUAGES'] = env_vars['TO_LANGUAGES'].split(',')
        self.set_config(config=env_vars)
