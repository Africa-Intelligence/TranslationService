from azure.ai.translation.text.models import TranslatedTextItem

from src.api.translation.i_translate_api import ITranslateAPI
from src.client.azure_translation_client import AzureTranslationClient
from src.api.translation.translation_result import TranslationResult
import pandas as pd
from typing import List, Dict


class AzureTranslateAPI(ITranslateAPI):
    def __init__(self, from_language: str, to_languages: List[str], key: str, region: str):
        super().__init__(from_language, to_languages)
        self.client = AzureTranslationClient(key, region)
        self.MAX_CHARS = 50000

    def translate(
        self, batch: pd.DataFrame, column_names: List[str]
    ) -> Dict[str, pd.DataFrame]:
        result = {}
        flattened_content, positions = self._flatten_dataframe(batch, column_names)
        chunks = self._split_into_chunks(flattened_content)
        
        all_responses: List[TranslatedTextItem] = []
        for chunk in chunks:
            chunk_response: List[TranslatedTextItem] = self.client.translate(
                chunk, self.from_language, self.to_languages
            )
            all_responses.extend(chunk_response)
        
        language_indices = {lang: idx for idx, lang in enumerate(self.to_languages)}
        for to_language in self.to_languages:
            translations = [item.translations[language_indices[to_language]].text for item in all_responses]
            translation_data = TranslationResult(
                column_names=column_names,
                positions=positions,
                original_content=flattened_content,
                translated_content=translations,
                from_language=self.from_language,
                to_language=to_language
            )
            translated_df = self._reconstruct_dataframe(translation_data)
            result[to_language] = translated_df

        return result
    
    def _split_into_chunks(self, texts: List[str]) -> List[List[str]]:
        chunks = []
        current_chunk = []
        current_chunk_length = 0

        for text in texts:
            will_exceed_limit = current_chunk_length + len(text) > self.MAX_CHARS
            if will_exceed_limit:
                if current_chunk:  # Only append non-empty chunks
                    chunks.append(current_chunk)
                current_chunk = []
                current_chunk_length = 0
            current_chunk.append(text)
            current_chunk_length += len(text)

        if current_chunk:
            chunks.append(current_chunk)

        return chunks