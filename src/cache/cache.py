import pandas as pd
from src.data.dataset_loader import DatasetLoader

class Cache(object):
    def __init__(self, cache_dataset_name):
        self.cache_dataset_name = cache_dataset_name
        self.cache_dataset = DatasetLoader(cache_dataset_name)

    def get(self, row: pd.DataFrame, field: str) -> str:
        instruction =  row["instruction"]
        match = self.cache_dataset.df.loc[self.cache_dataset.df['instruction'] == instruction, 'code']
        if not match.empty:
            return match.values[0]
        else:
            return ""

    def set(self, key, value):
        pass

    def clear(self):
        pass