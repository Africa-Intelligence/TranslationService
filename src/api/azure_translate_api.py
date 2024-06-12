from azure.ai.translation.text.models import TranslatedTextItem

from src.api.i_translate_api import ITranslateAPI
from src.client.azure_translation_client import AzureTranslationClient
import pandas as pd


class AzureTranslateAPI(ITranslateAPI):
    def __init__(self, from_language: str, to_languages: [str]):
        super().__init__(from_language, to_languages)
        self.client = AzureTranslationClient()

    def translate(self, row: pd.DataFrame, column_names: [str]) -> {str: [pd.DataFrame]}:
        response: [TranslatedTextItem] = self.client.translate(row, self.from_language, self.to_languages)
        result = {str: [pd.DataFrame]}
        for to_language in self.to_languages:
            result[to_language] = pd.DataFrame()
        for col_index, colum_result in enumerate(response):
            for translation_index, translation in enumerate(colum_result.translations):
                column_value = column_names[col_index]
                result[translation.to].at[0, f'{self.from_language}-{column_value}'] = row.iloc[col_index]
                result[translation.to].at[0, f'{translation.to}-{column_value}'] = translation.text

        return result
