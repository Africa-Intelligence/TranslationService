from src.api.translation.open_source.open_source_translate_api import OpenSourceTranslateAPI
from src.client.opus_client import OpusClient
from typing import Dict, List


class OpusTranslateAPI(OpenSourceTranslateAPI):

    def __init__(self, from_language: str, to_languages: List[str]):
        super().__init__(from_language, to_languages)
        self.models: Dict[str, OpusClient] = {}
        for to_language in to_languages:
            self.models[to_language] = OpusClient(
                from_language=from_language, to_language=to_language
            )

    def _translate(self, batch: List[str], to_language: str) -> List[str]:
        result = self.models[to_language].translate(batch)
        return result

