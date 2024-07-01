from typing import List, Dict, Tuple
import pandas as pd

from src.api.i_translate_api import ITranslateAPI
from src.api.open_source.translation_data import TranslationData

class OpenSourceTranslateAPI(ITranslateAPI):
    def __init__(self, from_language: str, to_languages: List[str]):
        super().__init__(from_language, to_languages)

    def translate(
        self, batch: pd.DataFrame, column_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        if batch.empty:
            return {to_language: pd.DataFrame() for to_language in self.to_languages}
        
        result = {}
        flattened_content, positions = self._flatten_dataframe(batch, column_names)

        for to_language in self.to_languages:
            translations = self._translate(flattened_content, to_language)
            translation_data = TranslationData(
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

    def _flatten_dataframe(self, df: pd.DataFrame, column_names: List[str]
    ) -> Tuple[List[str], List[Tuple[int, str]]]:
        flattened_non_empty_content = []
        positions = []

        for col in column_names:
            for row_index, text in enumerate(df[col]):
                if text != "":
                    flattened_non_empty_content.append(text)
                    positions.append((row_index, col))

        return flattened_non_empty_content, positions

    def _reconstruct_dataframe(self, data: TranslationData) -> pd.DataFrame:
        new_columns = []
        for col in data.column_names:
            new_columns.append(f"{data.from_language}-{col}")
            new_columns.append(f"{data.to_language}-{col}")
        df = pd.DataFrame(columns=new_columns)

        combined_data = zip(data.positions, data.original_content, data.translated_content)
        for position, original_text, translated_text in combined_data:
            row_index, column_name = position

            original_column_name = f"{data.from_language}-{column_name}"
            translated_column_name = f"{data.to_language}-{column_name}"
            df.at[row_index, original_column_name] = original_text
            df.at[row_index, translated_column_name] = translated_text

        return df