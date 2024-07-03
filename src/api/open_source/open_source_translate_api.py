from typing import List, Dict
import pandas as pd

from src.api.i_translate_api import ITranslateAPI
from api.translation_result import TranslationResult

class OpenSourceTranslateAPI(ITranslateAPI):
    def __init__(self, from_language: str, to_languages: List[str]):
        super().__init__(from_language, to_languages)

    def translate(
        self, batch: pd.DataFrame, column_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        result = {}
        flattened_content, positions = self._flatten_dataframe(batch, column_names)

        for to_language in self.to_languages:
            translations = self._translate(flattened_content, to_language)
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

    def _translate(self, batch: List[str], to_language: str) -> List[str]:
        raise NotImplementedError