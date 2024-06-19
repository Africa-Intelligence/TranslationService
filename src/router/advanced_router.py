from typing import List, Dict

import pandas as pd

from src.api.i_translate_api import ITranslateAPI
from src.condition.code_condition import CodeCondition
from src.condition.i_condition import ICondition
from src.llm.i_llm import ILLM
from src.router.i_router import IRouter


class AdvancedRouter(IRouter):

    def __init__(
        self,
        llm: ILLM,
        open_source_api: ITranslateAPI,
        closed_source_api: ITranslateAPI,
    ):
        self.code_condition: ICondition = CodeCondition(llm=llm)
        self.open_source_api = open_source_api
        self.closed_source_api = closed_source_api

    def execute(
        self, row: pd.DataFrame, column_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        if self.code_condition.execute(row):
            return self.closed_source_api.translate(row=row, column_names=column_names)
        else:
            return self.open_source_api.translate(row=row, column_names=column_names)
