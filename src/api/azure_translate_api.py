from azure.ai.translation.text.models import TranslatedTextItem

from src.api.i_translate_api import ITranslateAPI
from src.client.azure_translation_client import AzureTranslationClient
from src.api.translation_result import TranslationResult
import pandas as pd
from typing import List, Dict


class AzureTranslateAPI(ITranslateAPI):
    def __init__(self, from_language: str, to_languages: List[str], key: str, region: str):
        super().__init__(from_language, to_languages)
        self.client = AzureTranslationClient(key, region)

    def translate(
        self, batch: pd.DataFrame, column_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        result = {}
        flattened_content, positions = self._flatten_dataframe(batch, column_names)
        response: List[TranslatedTextItem] = self.client.translate(
            flattened_content, self.from_language, self.to_languages
        )

        for to_language in self.to_languages:
            translations = [item.translations[self.to_languages.index(to_language)].text for item in response]

            translation_data = TranslationResult(
                column_names=column_names,
                positions=positions,
                original_content=flattened_content,
                translated_content=translations,
                from_language=self.from_language,
                to_language=to_language
            )

            translated_df = self._reconstruct_dataframe(translation_data)
            result[to_language] = translated_df

        return result