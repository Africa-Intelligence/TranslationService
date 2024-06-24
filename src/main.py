#!/usr/bin/env python3
import sys
import os
import pandas as pd
from typing import Dict
from tqdm import tqdm

# Add the parent directory of `src` to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, parent_dir)

from src.api.azure_translate_api import AzureTranslateAPI
from src.api.aws_translate_api import AWSTranslateAPI
from src.api.open_source.opus_translate_api import OpusTranslateAPI
from src.llm.i_llm import ILLM
from src.router.basic_router import BasicRouter
from src.router.advanced_router import AdvancedRouter
from src.router.i_router import IRouter
from src.api.open_source.meta_translate_api import MetaTranslateAPI
from src.api.i_translate_api import ITranslateAPI
from src.data.dataset_loader import DatasetLoader
from src.llm.ollama_llm import OllamaLLM

from src.api.aws_translate_api import AWSTranslateAPI

def get_args():
    llm: ILLM = OllamaLLM() #only 1 option right now

    FROM_LANGUAGE = input("Enter ISO 639-1 code of the language to translate from: ")
    LANGUAGES_TO_TRANSLATE_TO = [input("Enter ISO 639-1 code of the language to translate to: ")]

    closed_source_api: ITranslateAPI = None
    closed_source_api_str = ""
    while closed_source_api_str.lower() not in ["aws", "azure"]:
        closed_source_api_str = input("Closed source API to use (AWS or Azure): ")
        if closed_source_api_str.lower() == "aws":
            closed_source_api: ITranslateAPI = AWSTranslateAPI(
                FROM_LANGUAGE, LANGUAGES_TO_TRANSLATE_TO
            )
        elif closed_source_api_str.lower() == "azure":
            closed_source_api: ITranslateAPI = AzureTranslateAPI(
                FROM_LANGUAGE, LANGUAGES_TO_TRANSLATE_TO
            )

    open_source_api: ITranslateAPI = None
    open_source_api_str = ""
    while open_source_api_str.lower() not in ["meta", "opus"]:
        open_source_api_str = input("Open source api to use (Meta or Opus): ")
        if open_source_api_str.lower() == "meta":
            open_source_api: ITranslateAPI = MetaTranslateAPI(
                FROM_LANGUAGE, LANGUAGES_TO_TRANSLATE_TO
            )
        elif open_source_api_str.lower() == "opus":
            open_source_api: ITranslateAPI = OpusTranslateAPI(
                FROM_LANGUAGE, LANGUAGES_TO_TRANSLATE_TO
            )

    router_str = ""
    while router_str.lower() not in ["basic", "advanced"]:
        router_str = input("Router to use (Basic or Advanced): ")
        if router_str.lower() == "basic":
            router: IRouter = BasicRouter(
                llm=llm, open_source_api=open_source_api, closed_source_api=closed_source_api
            )
        elif router_str.lower() == "advanced":
            router: IRouter = AdvancedRouter(
                llm=llm, open_source_api=open_source_api, closed_source_api=closed_source_api
            )

    return (LANGUAGES_TO_TRANSLATE_TO, router)
    
    
def run():
    dataset_name = "yahma/alpaca-cleaned"
    dataset = DatasetLoader(dataset_name)
    column_names = dataset.df.columns
    LANGUAGES_TO_TRANSLATE_TO, router = get_args()

    for i, row in tqdm(dataset.df.iterrows(), total=dataset.df.shape[0]):

        result: Dict[str, pd.DataFrame] = router.execute(
            row=row, column_names=column_names
        )
        for to_language in LANGUAGES_TO_TRANSLATE_TO:
            dataset.write_to_csv(result[to_language], to_language)


run()
