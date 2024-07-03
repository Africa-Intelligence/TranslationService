from enum import Enum
from typing import Dict, Optional


class IEnvironment(object):
    def __init__(self):
        self.config: Dict[str, Optional[str]] = {}
        self.keys = None

    def __call__(self, key, *args, **kwargs):
        self.keys = [key.value for key in EnvVar]
        return self.config[key]

    def set_config(self, config):
        self.config = config

    def get_value(self, key: str):
        value = self.config[key]
        if value == "":
            raise ValueError(key)
        return value


class EnvVar(Enum):
    AzureTranslateApiKey = "AZURE_TRANSLATE_API_KEY"
    AzureTranslateRegion = "AZURE_TRANSLATE_REGION"
    AWSRegion = "AWS_REGION"
    AWSAccessKey = "AWS_ACCESS_KEY"
    AwsSecretKey = "AWS_SECRET_KEY"
    AWSSessionToken = "AWS_SESSION_TOKEN"
    OpenAIAPIKey = "OPENAI_API_KEY"
    PoetryVirtualEnvsCreate = "POETRY_VIRTUALENVS_CREATE"
    FromLanguage = "FROM_LANGUAGE"
    ToLanguages = "TO_LANGUAGES"
    Router = "ROUTER"
    ClosedSourceAPI = "CLOSED_SOURCE_API"
    OpenSourceAPI = "OPEN_SOURCE_API"
    BatchSize = "BATCH_SIZE"
    LLM = "LLM"
    Conditions = "CONDITIONS"
    MinCharLength = "MIN_CHAR_LENGTH"
