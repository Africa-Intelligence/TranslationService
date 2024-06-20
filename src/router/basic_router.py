from typing import List, Dict

import pandas as pd

from src.api.i_translate_api import ITranslateAPI
from src.router.i_router import IRouter


class BasicRouter(IRouter):
    def __init__(self, api: ITranslateAPI):
        self.api = api

    def execute(
        self, row: pd.DataFrame, column_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        return self.api.translate(row=row, column_names=column_names)
