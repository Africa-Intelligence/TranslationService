from datasets import load_dataset
import pandas as pd
import os


class DatasetLoader(object):
    def __init__(self, dataset_name: str):
        dataset = load_dataset(dataset_name)
        df = pd.DataFrame(dataset["train"])
        # Drop text column
        if dataset_name == "yahma/alpaca-cleaned":
            new_order = ["instruction", "input", "output"]
            df = df[new_order]
        elif dataset_name == "yahma/alpaca":
            df = df.drop(columns=["text"])
        elif dataset_name == "africa-intelligence/alpaca-cleaned-annotated":
            df = df.map(lambda x: '' if x is None else x)
        self.dataset_name = dataset_name
        self.df = df

    def write_to_csv(self, result: pd.DataFrame, to_language: str):
        filename = f"{self.dataset_name.replace('/', '-')}-{to_language}.csv"
        file_exists = os.path.exists(filename)
        mode = "a" if file_exists else "w"
        result.to_csv(
            path_or_buf=filename, mode=mode, index=False, header=not file_exists
        )
