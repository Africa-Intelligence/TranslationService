#!/usr/bin/env python3
import sys
import os
import pandas as pd
from typing import Dict
from tqdm import tqdm
import logging

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

# Function to log progress
class TqdmToLogger:
    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level
        self.last_message = None

    def write(self, message):
        message = message.strip()
        if message != self.last_message:
            self.last_message = message
            self.logger.log(self.level, message)

    def flush(self):
        pass

def get_env_var(name):
    value = os.environ.get(name)
    if not value:
        logging.error(f"Error: Environment variable '{name}' is required but not set.")
        sys.exit(1)
    return value
    
def run():
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler("process.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger()

    dataset_name = "yahma/alpaca-cleaned"
    dataset = DatasetLoader(dataset_name)
    column_names = dataset.df.columns
    llm: ILLM = OllamaLLM()

    FROM_LANGUAGE = get_env_var('FROM_LANGUAGE')
    LANGUAGES_TO_TRANSLATE_TO = get_env_var('LANGUAGES_TO_TRANSLATE_TO').split(',')

    CLOSED_SOURCE_API = get_env_var('CLOSED_SOURCE_API')
    if CLOSED_SOURCE_API.lower() == "aws":
        closed_source_api: ITranslateAPI = AWSTranslateAPI(
            FROM_LANGUAGE, LANGUAGES_TO_TRANSLATE_TO
        )
    elif CLOSED_SOURCE_API.lower() == "azure":
        closed_source_api: ITranslateAPI = AzureTranslateAPI(
            FROM_LANGUAGE, LANGUAGES_TO_TRANSLATE_TO
        )

    OPEN_SOURCE_API = get_env_var('OPEN_SOURCE_API')
    if OPEN_SOURCE_API.lower() == "meta":
        open_source_api: ITranslateAPI = MetaTranslateAPI(
            FROM_LANGUAGE, LANGUAGES_TO_TRANSLATE_TO
        )
    elif OPEN_SOURCE_API.lower() == "opus":
        open_source_api: ITranslateAPI = OpusTranslateAPI(
            FROM_LANGUAGE, LANGUAGES_TO_TRANSLATE_TO
        )

    ROUTER = get_env_var('ROUTER')
    if ROUTER.lower() == "basic":
        router: IRouter = BasicRouter(
            llm=llm, open_source_api=open_source_api, closed_source_api=closed_source_api
        )
    elif ROUTER.lower() == "advanced":
        router: IRouter = AdvancedRouter(
            llm=llm, open_source_api=open_source_api, closed_source_api=closed_source_api
        )

    # Redirect tqdm output to logger
    tqdm_out = TqdmToLogger(logger)
    for i, row in tqdm(dataset.df.iterrows(), total=dataset.df.shape[0], file=tqdm_out):

        result: Dict[str, pd.DataFrame] = router.execute(
            row=row, column_names=column_names
        )
        for to_language in LANGUAGES_TO_TRANSLATE_TO:
            dataset.write_to_csv(result[to_language], to_language)

run()