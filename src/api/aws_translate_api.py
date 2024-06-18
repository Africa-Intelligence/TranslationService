from .i_translate_api import ITranslateAPI
import pandas as pd
from typing import List, Dict

from src.client.aws_translation_client import AwsTranslateClient


class AWSTranslateAPI(ITranslateAPI):
    def __init__(self, from_language: str, to_languages: List[str]):
        super().__init__(from_language, to_languages)
        self.client = AwsTranslateClient()

    def translate(self, row: pd.DataFrame, column_names: List[str]) -> Dict[str, pd.DataFrame]:
        result = {str: [pd.DataFrame]}
        for to_language in self.to_languages:
            result[to_language] = pd.DataFrame()

        for to_language in self.to_languages:
            for col_index, column_name in enumerate(column_names):
                original_text = row.iloc[col_index]
                translation = self.client.translate(
                    original_text,
                    from_language=self.from_language,
                    to_language=to_language
                ) if original_text != '' else original_text
                result[to_language].at[0, f'{self.from_language}-{column_name}'] = original_text
                result[to_language].at[0, f'{to_language}-{column_name}'] = translation

        return result
