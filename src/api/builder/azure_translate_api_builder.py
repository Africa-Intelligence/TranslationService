from typing import List

from src.api.azure_translate_api import AzureTranslateAPI


class AzureTranslateAPIBuilder(object):
    def __init__(self):
        self._instance = None

    def __call__(self, FROM_LANGUAGE: str, TO_LANGUAGES: List[str],
                 AZURE_TRANSLATE_API_KEY: str, AZURE_TRANSLATE_REGION: str, **kwargs):
        if not self._instance:
            self._instance = AzureTranslateAPI(FROM_LANGUAGE, TO_LANGUAGES,
                                               AZURE_TRANSLATE_API_KEY, AZURE_TRANSLATE_REGION)
        return self._instance
