from typing import List

from src.api.aws_translate_api import AWSTranslateAPI


class AWSTranslateAPIBuilder(object):
    def __init__(self):
        self._instance = None

    def __call__(self, FROM_LANGUAGE: str, TO_LANGUAGES: List[str], AWS_ACCESS_KEY_ID: str,
                 AWS_SECRET_KEY: str, AWS_SESSION_TOKEN: str, REGION_NAME: str, **_ignored):
        if not self._instance:
            self._instance = AWSTranslateAPI(
                FROM_LANGUAGE, TO_LANGUAGES, AWS_ACCESS_KEY_ID, AWS_SECRET_KEY, AWS_SESSION_TOKEN, REGION_NAME)
        return self._instance
