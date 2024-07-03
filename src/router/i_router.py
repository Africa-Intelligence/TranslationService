from typing import List, Dict

import pandas as pd


class IRouter(object):

    def execute(
        self, batch: pd.DataFrame, column_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        raise NotImplementedError
