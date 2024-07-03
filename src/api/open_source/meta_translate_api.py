from src.api.open_source.open_source_translate_api import OpenSourceTranslateAPI
from src.client.meta_client import MetaClient
from typing import List


class MetaTranslateAPI(OpenSourceTranslateAPI):

    def __init__(self, from_language: str, to_languages: List[str]):
        super().__init__(from_language, to_languages)
        self.client: MetaClient = MetaClient()

    def _translate(self, batch: List[str], to_language: str) -> List[str]:
        result = self.client.translate(
            batch, from_language=self.from_language, to_language=to_language
        )
        return result
