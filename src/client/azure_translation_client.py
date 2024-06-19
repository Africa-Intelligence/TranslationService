import os

from azure.ai.translation.text.models import InputTextItem, TranslatedTextItem
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
import pandas as pd
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv
from typing import List, Dict


class AzureTranslationClient(object):
    def __init__(self):
        load_dotenv()
        key = os.getenv("AZURE_TRANSLATE_API_KEY")
        region = os.getenv("AZURE_TRANSLATE_REGION")
        endpoint = "https://api.cognitive.microsofttranslator.com"
        self.client = TextTranslationClient(
            endpoint=endpoint, credential=AzureKeyCredential(key), region=region
        )

    def translate(
        self, row: pd.DataFrame, from_language: str, to_languages: List[str]
    ) -> List[TranslatedTextItem]:
        try:
            # Supported langauges - https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support
            content: List[InputTextItem] = []
            for value in row.values:
                text = InputTextItem(text=value)
                content.append(text)
            response: List[TranslatedTextItem] = self.client.translate(
                body=content, to_language=to_languages, from_language=from_language
            )

            return response

        except HttpResponseError as exception:
            if exception.error is not None:
                print(f"Error Code: {exception.error.code}")
                print(f"Message: {exception.error.message}")
            raise
