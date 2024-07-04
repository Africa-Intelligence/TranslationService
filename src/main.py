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

from src.api.result_uploader.i_result_uploader import IResultUploaderAPI
from src.factory.result_uploader_api_provider import ResultUploaderAPIProvider
from src.environment.i_environment import IEnvironment, EnvVar
from src.factory.environment_provider import EnvironmentProvider
from src.factory.router_provider import RouterProvider
from src.router.i_router import IRouter
from src.data.dataset_loader import DatasetLoader


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
    environment: IEnvironment = EnvironmentProvider().get()
    router: IRouter = RouterProvider().get(environment.get_value(EnvVar.Router.value), environment)
    result_uploader: IResultUploaderAPI = (ResultUploaderAPIProvider()
                                           .get(environment.get_value(EnvVar.ResultUploaderAPI.value), environment))

    dataset_loader = DatasetLoader("yahma/alpaca-cleaned")
    batch_size = int(environment.get_value(EnvVar.BatchSize.value))
    total_batches = (len(dataset_loader.dataset) + batch_size - 1) // batch_size
    tqdm_out = TqdmToLogger(logger)

    for i, batch in enumerate(
            tqdm(dataset_loader.dataset.iter(batch_size=batch_size), total=total_batches, file=tqdm_out)):
        batch_df = pd.DataFrame(batch)
        offset = i * batch_size
        batch_df.index = range(offset, offset + len(batch_df))
        result: Dict[str, pd.DataFrame] = router.execute(
            batch=batch_df, column_names=dataset_loader.df.columns
        )
        for to_language in environment.get_value(EnvVar.ToLanguages.value):
            dataset_loader.write_to_csv(result[to_language], to_language)

    result_uploader.upload_result_file(dataset_loader.result_folder)


run()
