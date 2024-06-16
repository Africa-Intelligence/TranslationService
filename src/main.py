import sys
import os

# Add the parent directory of `src` to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, parent_dir)

from tqdm import tqdm

from src.api.aws_translate_api import AWSTranslateAPI
from src.api.opus_translate_api import OpusTranslateAPI
from src.api.meta_translate_api import MetaTranslateAPI
from src.api.i_translate_api import ITranslateAPI
from src.data.dataset_loader import DatasetLoader
import pandas as pd
from typing import Dict

def run():
    dataset_name = "tatsu-lab/alpaca"
    dataset = DatasetLoader(dataset_name)
    FROM_LANGUAGE = 'en'
    LANGUAGES_TO_TRANSLATE_TO = ['af']
    api: ITranslateAPI = MetaTranslateAPI(FROM_LANGUAGE, LANGUAGES_TO_TRANSLATE_TO)
    column_names = dataset.df.columns

    for _, row in tqdm(dataset.df.iterrows(), colour='GREEN', total=dataset.df.shape[0]):
        result: Dict[str, pd.DataFrame] = api.translate(row=row, column_names=column_names)
        for to_language in LANGUAGES_TO_TRANSLATE_TO:
            dataset.write_to_csv(result[to_language], to_language)

run()
