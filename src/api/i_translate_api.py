import pandas as pd
from typing import List, Dict, Tuple
from api.translation_result import TranslationResult

class ITranslateAPI(object):
    def __init__(self, from_language: str, to_languages: List[str]):
        self.from_language: str = from_language
        self.to_languages: List[str] = to_languages

    def translate(
        self, batch: pd.DataFrame, column_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        pass

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

    def _reconstruct_dataframe(self, data: TranslationResult) -> pd.DataFrame:
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
