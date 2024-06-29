from typing import List

from src.api.open_source.opus_translate_api import OpusTranslateAPI


class OpusTranslateAPIBuilder(object):
    def __init__(self):
        self._instance = None

    def __call__(self, FROM_LANGUAGE: str, TO_LANGUAGES: List[str], **kwargs):
        if not self._instance:
            self._instance = OpusTranslateAPI(FROM_LANGUAGE, TO_LANGUAGES)
        return self._instance
