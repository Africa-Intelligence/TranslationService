import pandas as pd
from typing import List, Dict


class ITranslateAPI(object):
    def __init__(self, from_language: str, to_languages: List[str]):
        self.from_language: str = from_language
        self.to_languages: List[str] = to_languages

    def translate(self, row: pd.DataFrame, column_names: List[str]) -> Dict[str, pd.DataFrame]:
        pass
