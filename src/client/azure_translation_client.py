from azure.ai.translation.text.models import InputTextItem, TranslatedTextItem
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from typing import List
import logging
from src.log.logger import logging_manager

class AzureTranslationClient(object):
    def __init__(self, key: str, region: str):
        endpoint = "https://api.cognitive.microsofttranslator.com"
        self.client = TextTranslationClient(
            endpoint=endpoint, credential=AzureKeyCredential(key), region=region
        )
        logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING) #decrease azure verbosity
        self.logger = logging_manager.get_logger()  # Get our custom logger

    def translate(
        self, batch: List[str], from_language: str, to_languages: List[str]
    ) -> List[TranslatedTextItem]:
        try:
            # Supported langauges - https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support
            content: List[InputTextItem] = [InputTextItem(text=value) for value in batch]
            response: List[TranslatedTextItem] = self.client.translate(
                body=content, to_language=to_languages, from_language=from_language
            )
            self.logger.info(f"Azure translated {len(batch)} items")
            return response
        
        except HttpResponseError as exception:
            if exception.error is not None:
                # Log the error instead of printing
                self.logger.log(f"Translation Error - Code: {exception.error.code}, Message: {exception.error.message}")
            else:
                self.logger.log(f"Translation Error: {str(exception)}")
            raise