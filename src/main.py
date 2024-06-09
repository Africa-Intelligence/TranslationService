from tqdm import tqdm
from src.api.azure_translate_api import AzureTranslateAPI
from src.api.i_translate_api import ITranslateAPI
from src.data.dataset_loader import DatasetLoader
import pandas as pd


def run():
    dataset_name = "tatsu-lab/alpaca"
    dataset = DatasetLoader(dataset_name)
    FROM_LANGUAGE = 'en'
    LANGUAGES_TO_TRANSLATE_TO = ['zu']
    api: ITranslateAPI = AzureTranslateAPI()
    column_names = dataset.df.columns

    for index, row in tqdm(dataset.df.iterrows(), colour='GREEN', total=dataset.df.shape[0]):
        result: {str: [pd.DataFrame]} = api.translate(
            row=row,
            column_names=column_names,
            from_language=FROM_LANGUAGE,
            to_languages=LANGUAGES_TO_TRANSLATE_TO
        )
        for to_language in LANGUAGES_TO_TRANSLATE_TO:
            dataset.write_to_csv(result[to_language], to_language)


run()
