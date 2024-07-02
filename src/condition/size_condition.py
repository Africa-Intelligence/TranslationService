import pandas as pd

from src.condition.i_condition import ICondition

class SizeCondition(ICondition):
    def __init__(self, num_chars: int):
        self.num_chars = num_chars
        
    def execute(self, row: pd.DataFrame) -> bool:
        lengths = row.apply(len)
        return (lengths > self.num_chars).any()
