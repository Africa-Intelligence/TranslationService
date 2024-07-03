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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        while current_dir != os.path.dirname(current_dir):  # Stop at the root directory
            if os.path.exists(os.path.join(current_dir, 'README.md')):
                env_file = os.path.join(current_dir, '.env')
                if os.path.exists(env_file):
                    return dotenv_values(env_file)
                else:
                    raise FileNotFoundError(f".env file not found in the project root: {current_dir}")
            current_dir = os.path.dirname(current_dir)
        raise FileNotFoundError("Could not find project root")
