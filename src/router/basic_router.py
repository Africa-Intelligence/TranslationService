from typing import List, Dict

import pandas as pd

from src.api.translation.i_translate_api import ITranslateAPI
from src.router.i_router import IRouter


class BasicRouter(IRouter):
    def __init__(self, api: ITranslateAPI):
        self.api = api

    def execute(
        self, batch: pd.DataFrame, column_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        return self.api.translate(batch=batch, column_names=column_names)
