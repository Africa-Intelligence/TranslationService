#!/usr/bin/env python3
import sys
import os
import pandas as pd
from typing import Dict, Optional

from tqdm import tqdm
import logging

from src.condition.code_condition import CodeCondition
from src.condition.size_condition import SizeCondition
from src.condition.i_condition import ICondition
from src.environment.docker_environment import DockerEnvironment
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

    dataset_loader = DatasetLoader("yahma/alpaca-cleaned")
    api_provider = TranslateAPIProvider()
    router: IRouter
    config: Dict[str, Optional[str]]

    try:
        environment = LocalEnvironment()
        config = environment.config
    except FileNotFoundError:
        environment = DockerEnvironment()
        config = environment.config

    if config['ROUTER'].lower() == "basic":
        api = api_provider.get(config.get("OPEN_SOURCE_API"), **config)
        router = BasicRouter(api)
    else:
        llm: ILLM = OllamaLLM()
        code_condition: ICondition = CodeCondition(llm)
        size_condition: ICondition = SizeCondition(num_chars=500)
        open_source_api = api_provider.get(config.get("OPEN_SOURCE_API"), **config)
        closed_source_api = api_provider.get(config.get("CLOSED_SOURCE_API"), **config)
        router = AdvancedRouter([code_condition, size_condition], open_source_api, closed_source_api)

    batch_size = int(config["BATCH_SIZE"])
    total_batches = (len(dataset_loader.dataset) + batch_size - 1) // batch_size
    tqdm_out = TqdmToLogger(logger)

    for i, batch in enumerate(tqdm(dataset_loader.dataset.iter(batch_size=batch_size), total=total_batches, file=tqdm_out)):
        batch_df = pd.DataFrame(batch)
        batch_df.index = range(i * batch_size, i * batch_size + len(batch_df))
        result: Dict[str, pd.DataFrame] = router.execute(
            batch=batch_df, column_names=dataset_loader.df.columns
        )
        for to_language in config["TO_LANGUAGES"]:
            dataset_loader.write_to_csv(result[to_language], to_language)

run()
