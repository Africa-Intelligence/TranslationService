import os

from azure.ai.translation.text.models import InputTextItem, TranslatedTextItem
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
import pandas as pd
from azure.core.exceptions import HttpResponseError
from typing import List


class AzureTranslationClient(object):
    def __init__(self, key: str, region: str):
        endpoint = "https://api.cognitive.microsofttranslator.com"
        self.client = TextTranslationClient(
            endpoint=endpoint, credential=AzureKeyCredential(key), region=region
        )

    def translate(
        self, batch: List[str], from_language: str, to_languages: List[str]
    ) -> List[TranslatedTextItem]:
        try:
            # Supported langauges - https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support
            content: List[InputTextItem] = [InputTextItem(text=value) for value in batch]
            response: List[TranslatedTextItem] = self.client.translate(
                body=content, to_language=to_languages, from_language=from_language
            )

            return response

        except HttpResponseError as exception:
            if exception.error is not None:
                print(f"Error Code: {exception.error.code}")
                print(f"Message: {exception.error.message}")
            raise
