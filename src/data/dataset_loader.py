from datasets import load_dataset
import pandas as pd
import os


class DatasetLoader(object):
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self.dataset = load_dataset(dataset_name, split="train")

        # Apply dataset-specific transformations
        if dataset_name == "yahma/alpaca-cleaned":
            self.dataset = self.dataset.map(self.reorder_columns_alpaca_cleaned)
        elif dataset_name == "yahma/alpaca":
            self.dataset = self.dataset.remove_columns(["text"])
        elif dataset_name == "africa-intelligence/alpaca-cleaned-annotated":
            self.dataset = self.dataset.map(self.replace_none_with_empty_string) 
        self.df = pd.DataFrame(self.dataset)

    def write_to_csv(self, result: pd.DataFrame, to_language: str):
        filename = f"{self.dataset_name.replace('/', '-')}-{to_language}.csv"
        file_exists = os.path.exists(filename)
        mode = "a" if file_exists else "w"
        result.to_csv(
            path_or_buf=filename, mode=mode, index=False, header=not file_exists
        )

    @staticmethod
    def reorder_columns_alpaca_cleaned(row):
        return {
            "instruction": row["instruction"],
            "input": row["input"],
            "output": row["output"]
        }

    @staticmethod
    def replace_none_with_empty_string(row):
        return {key: value or '' for key, value in row.items()}
