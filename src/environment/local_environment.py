from typing import Dict, Optional
import os
from dotenv import dotenv_values

from src.environment.i_environment import IEnvironment


class LocalEnvironment(IEnvironment):
    def __init__(self):
        super().__init__()
        env_vars: Dict[str, Optional[str]] = self._load_env_vars()
        env_vars['TO_LANGUAGES'] = env_vars['TO_LANGUAGES'].split(',')
        self.set_config(config=env_vars)

    @staticmethod
    def _load_env_vars() -> Dict[str, Optional[str]]:
        possible_paths = [
            ".env",
            "../.env",
            "../../.env",
            os.path.join(os.path.dirname(__file__), ".env"),
            os.path.join(os.path.dirname(__file__), "../.env"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return dotenv_values(path)
        raise FileNotFoundError("Could not find .env file in any of the expected locations.")
