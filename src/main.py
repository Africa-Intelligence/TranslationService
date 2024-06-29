#!/usr/bin/env python3
import sys
import os
import pandas as pd
from typing import Dict, Optional

from tqdm import tqdm
import logging

from src.condition.code_condition import CodeCondition
from src.condition.i_condition import ICondition
from src.environment.docker_environment import DockerEnvironment
from src.environment.i_environment import IEnvironment
from src.environment.local_environment import LocalEnvironment
from src.factory.translate_api_provider import TranslateAPIProvider

# Add the parent directory of `src` to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, parent_dir)

from src.llm.i_llm import ILLM
from src.router.basic_router import BasicRouter
from src.router.advanced_router import AdvancedRouter
from src.router.i_router import IRouter
from src.data.dataset_loader import DatasetLoader
from src.llm.ollama_llm import OllamaLLM

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


def run():
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler("process.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger()

    dataset = DatasetLoader("yahma/alpaca-cleaned")
    api_provider = TranslateAPIProvider()

    router: IRouter
    config: Dict[str, Optional[str]]

    if os.path.exists("../.env"):
        environment = LocalEnvironment()
        config = environment.config
    else:
        environment = DockerEnvironment()
        config = environment.config

    if config['ROUTER'].lower() == "basic":
        api = api_provider.get(config.get("OPEN_SOURCE_API"), **config)
        router = BasicRouter(api)
    else:
        llm: ILLM = OllamaLLM()
        code_condition: ICondition = CodeCondition(llm)
        open_source_api = api_provider.get(config.get("OPEN_SOURCE_API"), **config)
        closed_source_api = api_provider.get(config.get("CLOSED_SOURCE_API"), **config)
        router = AdvancedRouter(code_condition, open_source_api, closed_source_api)

    # Redirect tqdm output to logger
    tqdm_out = TqdmToLogger(logger)
    for i, row in tqdm(dataset.df.iterrows(), total=dataset.df.shape[0], file=tqdm_out):

        result: Dict[str, pd.DataFrame] = router.execute(
            row=row, column_names=dataset.df.columns
        )
        for to_language in config["TO_LANGUAGES"]:
            dataset.write_to_csv(result[to_language], to_language)


run()
