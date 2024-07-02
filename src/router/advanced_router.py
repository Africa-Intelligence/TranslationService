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
        conditions: List[ICondition],
        open_source_api: ITranslateAPI,
        closed_source_api: ITranslateAPI,
    ):
        self.conditions = conditions
        self.open_source_api = open_source_api
        self.closed_source_api = closed_source_api

    def execute(
        self, batch: pd.DataFrame, column_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        use_closed_source = batch.apply(self.use_closed_source, axis=1)

        closed_source_results = self.closed_source_api.translate(
            batch[use_closed_source], column_names=column_names)
        open_source_results = self.open_source_api.translate(
            batch[~use_closed_source], column_names=column_names)

        translated_batch = {}
        all_languages = set(closed_source_results.keys()) | set(open_source_results.keys())
        for lang in all_languages:
            closed_lang_df = closed_source_results.get(lang, pd.DataFrame())
            open_lang_df = open_source_results.get(lang, pd.DataFrame())
            
            # Ensure the index of the result DataFrames match the input batch
            if not closed_lang_df.empty:
                closed_lang_df.index = batch[use_closed_source].index
            if not open_lang_df.empty:
                open_lang_df.index = batch[~use_closed_source].index

            combined_df = pd.concat([closed_lang_df, open_lang_df])
            translated_batch[lang] = combined_df.sort_index()
        
        return translated_batch

    def use_closed_source(self, row: pd.Series) -> bool:
        return any(condition.execute(row) for condition in self.conditions)

