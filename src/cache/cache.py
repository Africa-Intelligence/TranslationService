import pandas as pd

class Cache(object):
    def __init__(self):
        self.cache = {}

    def contains(self, row: pd.DataFrame, field: str) -> bool:
        #hard code for now since it has been run for all rows
        return True

    def get(self, row: pd.DataFrame, field: str) -> str:
        return row[field]

    def set(self, key, value):
        pass

    def clear(self):
        pass