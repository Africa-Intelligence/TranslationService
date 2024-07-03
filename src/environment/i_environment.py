from enum import Enum
from typing import Dict, Optional


class IEnvironment(object):
    def __init__(self):
        self.config: Dict[str, Optional[str]] = {}
        self.keys = None

    def __call__(self, key, *args, **kwargs):
        self.keys = [key.value for key in ENVIRONMENT_VARIABLES]
        return self.config[key]

    def set_config(self, config):
        self.config = config

    def get_value(self, key):
        return self.config[key]


class ENV_VARS(Enum):
    AZURE_TRANSLATE_API_KEY = "AZURE_TRANSLATE_API_KEY"
    AZURE_TRANSLATE_REGION = "AZURE_TRANSLATE_REGION"
    AWS_REGION = "AWS_REGION"
    AWS_ACCESS_KEY = "AWS_ACCESS_KEY"
    AWS_SECRET_KEY = "AWS_SECRET_KEY"
    AWS_SESSION_TOKEN = "AWS_SESSION_TOKEN"
    OPENAI_API_KEY = "OPENAI_API_KEY"
    POETRY_VIRTUALENVS_CREATE = "POETRY_VIRTUALENVS_CREATE"
    FROM_LANGUAGE = "FROM_LANGUAGE"
    TO_LANGUAGES = "TO_LANGUAGES"
    ROUTER = "ROUTER"
    CLOSED_SOURCE_API = "CLOSED_SOURCE_API"
    OPEN_SOURCE_API = "OPEN_SOURCE_API"
    BATCH_SIZE = "BATCH_SIZE"
    CONDITIONS = "CONDITIONS"
    LLM = "LLM"
