from tqdm import tqdm
from src.api.azure_translate_api import AzureTranslateAPI
from src.api.i_translate_api import ITranslateAPI
from src.api.opus_api import OpusAPI
from src.data.dataset_loader import DatasetLoader
import pandas as pd


def run():
    dataset_name = "tatsu-lab/alpaca"
    dataset = DatasetLoader(dataset_name)
    FROM_LANGUAGE = 'en'
    LANGUAGES_TO_TRANSLATE_TO = ['crs', 'fr']
    api: ITranslateAPI = OpusAPI(FROM_LANGUAGE, LANGUAGES_TO_TRANSLATE_TO)
    column_names = dataset.df.columns

    for index, row in tqdm(dataset.df.iterrows(), colour='GREEN', total=dataset.df.shape[0]):
        result: {str: [pd.DataFrame]} = api.translate(row=row, column_names=column_names)
        for to_language in LANGUAGES_TO_TRANSLATE_TO:
            dataset.write_to_csv(result[to_language], to_language)


run()
