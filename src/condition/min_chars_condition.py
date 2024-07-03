import pandas as pd

from src.condition.i_condition import ICondition


class MinCharsCondition(ICondition):
    def __init__(self, min_char_length: int):
        self.min_chars = min_char_length

    def execute(self, row: pd.DataFrame) -> bool:
        lengths = row.apply(len)
        return (lengths > self.min_chars).any()
