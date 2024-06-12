import pandas as pd


class ITranslateAPI(object):
    def __init__(self, from_language: str, to_languages: [str]):
        self.from_language: str = from_language
        self.to_languages: [str] = to_languages

    def translate(self, row: pd.DataFrame, column_names: [str]) -> {str: [pd.DataFrame]}:
        pass
