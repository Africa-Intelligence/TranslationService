import pandas as pd

from src.api.i_translate_api import ITranslateAPI
from src.client.opus_client import OpusClient


class OpusAPI(ITranslateAPI):

    def __init__(self, from_language: str, to_languages: [str]):
        super().__init__(from_language, to_languages)
        self.models: {str: OpusClient} = {}
        for to_language in to_languages:
            self.models[to_language] = OpusClient(from_language=from_language, to_language=to_language)

    def translate(self, row: pd.DataFrame, column_names: [str]) -> {str: [pd.DataFrame]}:
        result = {str: [pd.DataFrame]}
        for to_language in self.to_languages:
            result[to_language] = pd.DataFrame()

        for to_language in self.to_languages:
            for col_index, column_name in enumerate(column_names):
                original_text = row.iloc[col_index]
                translation = self.models[to_language].translate(original_text) if original_text != '' else original_text
                result[to_language].at[0, f'{self.from_language}-{column_name}'] = original_text
                result[to_language].at[0, f'{to_language}-{column_name}'] = translation

        return result
