import pandas as pd

from src.condition.i_condition import ICondition

class MinCharsCondition(ICondition):
    def __init__(self, min_chars: int):
        self.min_chars = min_chars
        
    def execute(self, row: pd.DataFrame) -> bool:
        lengths = row.apply(len)
        return (lengths > self.min_chars).any()
