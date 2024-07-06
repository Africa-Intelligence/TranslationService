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
from src.log.logger import logging_manager

def run():
    logging_manager.setup_logging()
    logger = logging_manager.get_logger()
    logger.info("Starting the application")
    environment: IEnvironment = EnvironmentProvider().get()
    router: IRouter = RouterProvider().get(environment.get_value(EnvVar.Router.value), environment)
    result_uploader: IResultUploaderAPI = (ResultUploaderAPIProvider()
                                           .get(environment.get_value(EnvVar.ResultUploaderAPI.value), environment))
    dataset_loader = DatasetLoader("yahma/alpaca-cleaned")

    batch_size = int(environment.get_value(EnvVar.BatchSize.value))
    total_batches = (len(dataset_loader.dataset) + batch_size - 1) // batch_size
    progress_iter = logging_manager.get_progress_logger(
            dataset_loader.dataset.iter(batch_size=batch_size),
            total=total_batches
    )
    for i, batch in enumerate(progress_iter):
        batch_df = pd.DataFrame(batch)
        offset = i * batch_size
        batch_df.index = range(offset, offset + len(batch_df))
        result: Dict[str, pd.DataFrame] = router.execute(
            batch=batch_df, column_names=dataset_loader.df.columns
        )
        for to_language in environment.get_value(EnvVar.ToLanguages.value):
            dataset_loader.write_to_csv(result[to_language], to_language)
    result_uploader.upload_result_file(dataset_loader.result_folder)
    logger.info("Application completed successfully")

def sleep_indefinitely():
    logger = logging_manager.get_logger()
    logger.info("Main process completed. Sleeping indefinitely to keep container alive.")
    def signal_handler(signum, frame):
        logger.info("Received shutdown signal. Exiting.")
        sys.exit(0)
    signal.signal(signal.SIGTERM, signal_handler)
    while True:
        time.sleep(3600) 
    
if __name__ == "__main__":
    run()
    sleep_indefinitely() #sleep indefinitely to keep the container alive
