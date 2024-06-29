from typing import List

from src.api.open_source.meta_translate_api import MetaTranslateAPI


class MetaTranslateAPIBuilder(object):
    def __init__(self):
        self._instance = None

    def __call__(self, FROM_LANGUAGE: str, TO_LANGUAGES: List[str], **kwargs):
        if not self._instance:
            self._instance = MetaTranslateAPI(FROM_LANGUAGE, TO_LANGUAGES)
        return self._instance
