import sys
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import ExitStack
from typing import Dict
from tqdm import tqdm

# Add the parent directory of `src` to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, parent_dir)

from src.api.azure_translate_api import AzureTranslateAPI
from src.api.open_source.opus_translate_api import OpusTranslateAPI
from src.llm.i_llm import ILLM
from src.router.advanced_router import AdvancedRouter
from src.router.basic_router import BasicRouter
from src.router.i_router import IRouter
from src.api.open_source.meta_translate_api import MetaTranslateAPI
from src.api.i_translate_api import ITranslateAPI
from src.data.dataset_loader import DatasetLoader
from src.llm.ollama_llm import OllamaLLM


def run():
    dataset_name = "yahma/alpaca-cleaned"
    dataset = DatasetLoader(dataset_name)
    column_names = dataset.df.columns
    llm: ILLM = OllamaLLM()
    FROM_LANGUAGE = "en"
    LANGUAGES_TO_TRANSLATE_TO = ["af"]
    closed_source_api: ITranslateAPI = AzureTranslateAPI(
        FROM_LANGUAGE, LANGUAGES_TO_TRANSLATE_TO
    )
    open_source_api: ITranslateAPI = MetaTranslateAPI(
        FROM_LANGUAGE, LANGUAGES_TO_TRANSLATE_TO
    )
    router: IRouter = AdvancedRouter(
        llm=llm, open_source_api=open_source_api, closed_source_api=closed_source_api
    )
    num_threads = 10
    for result in get_translations(dataset, router, num_threads):
        for to_language in LANGUAGES_TO_TRANSLATE_TO:
            dataset.write_to_csv(result[to_language], to_language)


def get_translations(
    dataset: DatasetLoader, router: IRouter, num_threads
) -> [Dict[str, pd.DataFrame]]:
    with ExitStack() as stack:
        pbar = stack.enter_context(tqdm(total=dataset.df.shape[0]))
        executor: ThreadPoolExecutor = stack.enter_context(
            ThreadPoolExecutor(max_workers=num_threads)
        )
        futures = []
        try:
            for index, row in dataset.df.iterrows():
                futures.append(
                    executor.submit(
                        router.execute, row=row, column_names=dataset.df.columns
                    )
                )
            for future in as_completed(futures):
                pbar.update(1)
                yield future.result()
        except Exception as ex:
            print(ex)
            raise ex


run()
