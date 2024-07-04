from src.api.translation.i_translate_api import ITranslateAPI
import pandas as pd
from typing import List, Dict

from src.client.aws_translation_client import AwsTranslateClient
from src.api.translation.translation_result import TranslationResult


class AWSTranslateAPI(ITranslateAPI):
    def __init__(self, from_language: str, to_languages: List[str], aws_access_key_id: str, aws_secret_access_key: str,
                 aws_session_token: str, region_name: str):
        super().__init__(from_language, to_languages)
        self.client = AwsTranslateClient(aws_access_key_id, aws_secret_access_key, aws_session_token, region_name)

    def translate(
        self, batch: pd.DataFrame, column_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        result = {}
        flattened_content, positions = self._flatten_dataframe(batch, column_names)

        for to_language in self.to_languages:
            translations = [
                self.client.translate(
                    text,
                    from_language=self.from_language,
                    to_language=to_language,
                )
                for text in flattened_content
            ]

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