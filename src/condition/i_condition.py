import pandas as pd

class ICondition(object):
    def execute(self, row: pd.DataFrame) -> bool:
        pass
