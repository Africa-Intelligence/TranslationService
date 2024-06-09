import pandas as pd


class ITranslateAPI(object):
    def translate(self, row: pd.DataFrame, column_names: [str], from_language: str, to_languages: [str]) -> {str: [pd.DataFrame]}:
        pass
